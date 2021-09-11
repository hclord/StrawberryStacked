class Node:
  rgb = (0, 0, 0)
  neighbors = []
  
  def __init__(self, rgb):
    self.rgb = rgb

  def add_neighbor(self, node):
    self.neighbors.append(node)