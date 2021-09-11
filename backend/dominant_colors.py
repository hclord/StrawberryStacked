import os
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = './strawberrystacked-8c57b210dc16.json'

from google.cloud import vision
import io
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

# Converts 'rgb' pixel to colorblind 'type'
def simulate_colorblind(rgb, type):
  blindType = BLIND_TYPES[type]
  output = rgb
  rgb['blindR'] = blindType["R"][0] * rgb[0]/100 + blindType["R"][1] * rgb[1]/100 + blindType["R"][2] * rgb[2]/100
  rgb['blindG'] = blindType["G"][0] * rgb[0]/100 + blindType["G"][1] * rgb[1]/100 + blindType["G"][2] * rgb[2]/100
  rgb['blindB'] = blindType["B"][0] * rgb[0]/100 + blindType["B"][1] * rgb[1]/100 + blindType["B"][2] * rgb[2]/100
  return output

# helper function
def parse_google_color_data(color_data):
    output = {
        'R': color_data.color.red,
        'G': color_data.color.green,
        'B': color_data.color.blue,
        'fraction': color_data.pixel_fraction
    }
    return simulate_colorblind(output, 'Protanopia')