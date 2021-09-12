
from colormath.color_objects import LabColor, sRGBColor
from colormath.color_conversions import convert_color
from colormath.color_diff import delta_e_cie1976

# TODO: test out different color combos
COLOR_PERCENT_CHANGE = 0.1  # experimentally found
COLOR_TOTAL_CHANGE = 50  # experimentally found


# takes in two color dicts
# determines if the distance between color1 and distance between color2 changes significantly for colorblind
def determine_inaccessible_color_combo(color1, color2):
    # converts colors into sRGBColor
    color1_rgb = sRGBColor(color1['R'], color1['G'], color1['B'], True)
    color2_rgb = sRGBColor(color2['R'], color2['G'], color2['B'], True)
    color1_blind_rgb = sRGBColor(color1['blindR'], color1['blindG'], color1['blindB'], True)
    color2_blind_rgb = sRGBColor(color2['blindR'], color2['blindG'], color2['blindB'], True)
    
    # usual colors to convert to LAB representation
    color1_lab = convert_color(color1_rgb, LabColor)
    color2_lab = convert_color(color2_rgb, LabColor)
    delta_e = delta_e_cie1976(color1_lab, color2_lab)

    # colorblind colors to convert LAB representation
    color1_blind_lab = convert_color(color1_blind_rgb, LabColor)
    color2_blind_lab = convert_color(color2_blind_rgb, LabColor)
    delta_e_blind = delta_e_cie1976(color1_blind_lab, color2_blind_lab)

    delta_of_deltas = abs(delta_e - delta_e_blind)
    percentage_change = delta_of_deltas / delta_e if delta_e else 1
    # we want delta of delta to be smaller than some general value
    # but also we want the delta of deltas to have significantly changed from the original
    return delta_of_deltas < COLOR_TOTAL_CHANGE and percentage_change < COLOR_PERCENT_CHANGE


def find_color_distance(color1, color2):
  # converts colors into sRGBColor
  color1_rgb = sRGBColor(color1['R'], color1['G'], color1['B'], True)
  color2_rgb = sRGBColor(color2['R'], color2['G'], color2['B'], True)

  # usual colors to convert to LAB representation
  color1_lab = convert_color(color1_rgb, LabColor)
  color2_lab = convert_color(color2_rgb, LabColor)
  return delta_e_cie1976(color1_lab, color2_lab)




# input should be props.dominant_colors.colors
# output is a list of bad color combos (if n colors, then n^2 tuples)
def analyze(color_list):
    output = []
    for i, color1 in enumerate(color_list):
      for color2 in color_list[i:]:
        if color1 != color2 and determine_inaccessible_color_combo(color1, color2):
            output.append((color1, color2))
    return output

