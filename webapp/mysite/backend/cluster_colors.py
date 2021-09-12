from skimage import io
import skimage.segmentation as seg
import skimage.color as color
from PIL import Image
import numpy as np
import matplotlib.pyplot as plt
from dominant_colors import *
from analyzer import determine_inaccessible_color_combo

class Node:
  rgb = "" # hex
  neighbors = {}
  
  def __init__(self, rgb):
      self.rgb = rgb

  def add_neighbor(self, node):
      if node.rgb not in self.neighbors:
        self.neighbors[node.rgb] = node
    

# Returns a PIL.Image of the clustered colors from image at 'path' 
def cluster_colors(path, n_segments):
  image = io.imread(path) 
  image_slic = seg.slic(image, n_segments)
  clustered = color.label2rgb(image_slic, image, kind='avg')
  return Image.fromarray(np.uint8(clustered)).convert('RGB')

# Converts 'color' to hex
def hex(color):
  colour = (color[0], color[1], color[2])
  return str('#%02x%02x%02x' % colour)

# Returns graph of colors in 'img' as nodes
def create_graph(img):
  graph = {}
  prev_color = None
  for x in range(img.size[0]):
    for y in range(img.size[1]):
      if prev_color is None:
        prev_color = hex(img.getpixel((x, y)))
      cur_color = hex(img.getpixel((x, y)))
      #If changing to new row, switch prev_color to above pixel
      if x is 0 and y is not 0:
        prev_color = hex(img.getpixel((x, y-1)))
      #change in node
      if not prev_color == cur_color:
        #Checks if node of this color already exists
        if prev_color not in graph:
          graph[prev_color] = Node(prev_color)
        if cur_color not in graph:
          graph[cur_color] = Node(cur_color)
        graph[prev_color].add_neighbor(graph[cur_color])
        graph[cur_color].add_neighbor(graph[prev_color])
  return graph

          
def bfs(graph, blindType):
  visited = {}
  starting_key = None
  for key in graph:
    visited[key] = False
    if starting_key is None:
      starting_key = key
  q = []
  q.append(starting_key)
  visited[starting_key] = True
  bad_colors = []
  while q:
    hex = q.pop(0)
    node = graph[hex]
    for i in graph[hex].neighbors:
      if visited[i] == False:
        q.append(i)
        visited[i] = True
        color = convert_hex_to_rgb(node.rgb, blindType)
        neighbor = convert_hex_to_rgb(graph[i].rgb, blindType)
        if determine_inaccessible_color_combo(color, neighbor):
          bad_colors.append((color, neighbor))
  return bad_colors
  
def getBadColors(path, n_segments, blindType, pixelate=True):
  if pixelate:
    img = cluster_colors(path, n_segments)
    print(type(img))
  else:
    img = io.imread(path) 
    img = Image.fromarray(img)
  graph = create_graph(img)
  bad_colors = bfs(graph, blindType)
  return bad_colors, img
  




      


