from skimage import io
import matplotlib.pyplot as plt
import skimage.segmentation as seg
import skimage.color as color

def cluster_colors(path):
  image = io.imread('ocean.gif') 

  image_slic = seg.slic(image,n_segments=3000)

  # label2rgb replaces each discrete label with the average interior color
  # image_show(color.label2rgb(image_slic, image, kind='avg'));