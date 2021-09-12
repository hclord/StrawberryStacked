from backend.dominant_colors import *
from backend.analyzer import analyze
import logging

def compute_bad_colors(path):
    color_list = get_dominant_colors(path)
    return analyze(color_list)

def create_colorblind_image(image):
    return simulate_entire_image(image)
    
    
    