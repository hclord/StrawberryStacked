from skimage import io
import skimage.segmentation as seg
import skimage.color as color
from PIL import Image
import numpy as np

# Returns a PIL.Image of the clustered colors from image at 'path' 
def cluster_colors(path):
  image = io.imread(path) 
  image_slic = seg.slic(image,n_segments=3000)
  clustered = color.label2rgb(image_slic, image, kind='avg')
  return Image.fromarray(np.uint8(clustered)).convert('RGB')