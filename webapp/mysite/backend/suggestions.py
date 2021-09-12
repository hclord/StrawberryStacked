import numpy as np
import logging

# This code was used from Daltonize, a library that simulates the three types of 
# dichromatic color blindness and images and matplotlib figures. We use part of the
# functionality to transform pixels to RGB color codes.
# https://github.com/joergdietrich/daltonize/blob/master/daltonize/daltonize.py
def transform_colorspace(img, mat):
    """Transform image to a different color space.
    Arguments:
    ----------
    img : array of shape (M, N, 3)
    mat : array of shape (3, 3)
        conversion matrix to different color space
    Returns:
    --------
    out : array of shape (M, N, 3)
    """
    # Fast element (=pixel) wise matrix multiplication
    # print(img)
    return np.einsum("ij, ...j", mat, img, dtype=np.float16, casting="same_kind")

def simulate_colorblind(rgb, color_deficit="p"):
    """Simulate the effect of color blindness on an image.
    Arguments:
    ----------
    rgb : array of shape (M, N, 3)
        original image in RGB format
    color_deficit : {"d", "p", "t"}, optional
        type of colorblindness, d for deuteronopia (default),
        p for protonapia,
        t for tritanopia
    Returns:
    --------
    sim_rgb : array of shape (M, N, 3)
        simulated image in RGB format
    """
    # Colorspace transformation matrices
    cb_matrices = {
        "d": np.array([[1, 0, 0], [1.10104433,  0, -0.00901975], [0, 0, 1]], dtype=np.float16),
        "p": np.array([[0, 0.90822864, 0.008192], [0, 1, 0], [0, 0, 1]], dtype=np.float16),
        "t": np.array([[1, 0, 0], [0, 1, 0], [-0.15773032,  1.19465634, 0]], dtype=np.float16),
    }
    rgb2lms = np.array([[0.3904725 , 0.54990437, 0.00890159],
       [0.07092586, 0.96310739, 0.00135809],
       [0.02314268, 0.12801221, 0.93605194]], dtype=np.float16)
    # Precomputed inverse
    lms2rgb = np.array([[ 2.85831110e+00, -1.62870796e+00, -2.48186967e-02],
       [-2.10434776e-01,  1.15841493e+00,  3.20463334e-04],
       [-4.18895045e-02, -1.18154333e-01,  1.06888657e+00]], dtype=np.float16)
    # first go from RBG to LMS space
    lms = transform_colorspace(rgb, rgb2lms)
    # Calculate image as seen by the color blind
    sim_lms = transform_colorspace(lms, cb_matrices[color_deficit])
    # Transform back to RBG
    sim_rgb = transform_colorspace(sim_lms, lms2rgb)
    return sim_rgb

def daltonize(rgb, color_deficit='p'):
    """
    Adjust color palette of an image to compensate color blindness.
    Arguments:
    ----------
    rgb : array of shape (M, N, 3)
        original image in RGB format
    color_deficit : {"d", "p", "t"}, optional
        type of colorblindness, d for deuteronopia (default),
        p for protonapia,
        t for tritanopia
    Returns:
    --------
    dtpn : array of shape (M, N, 3)
        image in RGB format with colors adjusted
    """
    sim_rgb = simulate_colorblind(rgb, color_deficit)
    err2mod = np.array([[0, 0, 0], [0.7, 1, 0], [0.7, 0, 1]])
    # rgb - sim_rgb contains the color information that dichromats
    # cannot see. err2mod rotates this to a part of the spectrum that
    # they can see.
    err = transform_colorspace(rgb - sim_rgb, err2mod)
    dtpn = err + rgb
    return dtpn

def rgb_to_hex(r, g, b):
  return ('#{:02X}{:02X}{:02X}').format(int(r), int(g), int(b))

def provideSuggestion(bad_pair):
  if len(bad_pair) < 2:
      return
  mat = np.array([[[bad_pair[0]['R'], bad_pair[0]['G'], bad_pair[0]['B']], \
                   [bad_pair[1]['R'], bad_pair[1]['G'], bad_pair[1]['B']]]])
  corrected = daltonize(mat)
  corrected1 = corrected[0][0]
  corrected2 = corrected[0][1]
  return rgb_to_hex(corrected1[0],corrected1[1],corrected1[2]), rgb_to_hex(corrected2[0],corrected2[1],corrected2[2])
  

def provideSuggestions(bad_pairs):
  logging.debug(bad_pairs)
  corrections = []
  for bad_pair in bad_pairs:
    corrections.append(provideSuggestion(bad_pair))
  return corrections