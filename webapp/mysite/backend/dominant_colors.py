import os
import io
from PIL import ImageColor, Image
import numpy as np
from google.cloud import vision
import logging
import matplotlib.image as mpimg

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = '/Users/hlord/Desktop/StrawberryStacked/webapp/mysite/backend/strawberrystacked-8c57b210dc16.json'

client = vision.ImageAnnotatorClient()

BLIND_TYPES = {"Protanopia":   {
                "R":[56.667, 43.333,  0],
                "G":[55.833, 44.167,  0],
                "B": [0, 24.167, 75.833]}}

# Returns list of dominant colors in the image at 'path'
def get_dominant_colors(path):
  with io.open(path, 'rb') as image_file:
    content = image_file.read()
  image = vision.Image(content=content)
  response = client.image_properties(image=image)
  props = response.image_properties_annotation
  
  output = []
  for color in props.dominant_colors.colors:
    output.append(parse_google_color_data(color))

  if response.error.message:
    print(response.error.message)

  return output


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



# helper function that converts hex to dictionary
def convert_hex_to_rgb(hex, type):    
    colors = ImageColor.getcolor(hex, "RGB")
    sim_rgb = simulate_colorblind(np.array(colors))
    return {
        'R': colors[0],
        'G': colors[1],
        'B': colors[2],
        'blindR': sim_rgb[0],
        'blindG': sim_rgb[1],
        'blindB': sim_rgb[2],
    }

def rgb_to_hex(r, g, b):
  return ('#{:02X}{:02X}{:02X}').format(int(r), int(g), int(b))

# helper function that converts google output to dictionary
def parse_google_color_data(color_data, type='p'):
    colors = (color_data.color.red, color_data.color.green, color_data.color.blue)
    sim_rgb = simulate_colorblind(np.array(colors), type)
    return {
        'R': colors[0],
        'G': colors[1],
        'B': colors[2],
        'blindR': sim_rgb[0],
        'blindG': sim_rgb[1],
        'blindB': sim_rgb[2],
        'fraction': color_data.pixel_fraction,
        'hex': rgb_to_hex(colors[0], colors[1], colors[2]),
        'blindHex':rgb_to_hex(sim_rgb[0], sim_rgb[1], sim_rgb[2]),
    }

def simulate_entire_image(path):
    # img = np.asarray(img.convert("RGB"), dtype=np.float16)
    # img = img / 255
    fig = mpimg.imread(path)[:,:,:3]
    #print(fig)
    sim_fig = simulate_colorblind(fig, color_deficit='p')
    #print(sim_fig)
    sim_fig = sim_fig * 255
    return Image.fromarray(np.uint8(sim_fig)).convert('RGB')