
from colormath.color_objects import LabColor, sRGBColor
from colormath.color_conversions import convert_color
from colormath.color_diff import delta_e_cie1976

# TODO: test out different color combos
COLOR_MIN_DELTA = 0.1  # experimentally found
COLOR_MIN_VAL = 1 # experimentally found



# takes in two color dicts, outputs % bad or something
# determines if the distance between color1 and distance between color2 changes significantly for colorblind
def determine_inaccessible_color_combo(color1, color2):
    color1_rgb = sRGBColor(color1['R'], color1['G'], color1['B'], True)
    color2_rgb = sRGBColor(color2['R'], color2['G'], color2['B'], True)
    color1_blind_rgb = sRGBColor(color1['blindR'], color1['blindG'], color1['blindB'], True)
    color2_blind_rgb = sRGBColor(color2['blindR'], color2['blindG'], color2['blindB'], True)
    
    # usual colors to convert
    color1_lab = convert_color(color1_rgb, LabColor)
    color2_lab = convert_color(color2_rgb, LabColor)
    delta_e = delta_e_cie1976(color1_lab, color2_lab)

    # usual colors to convert
    color1_blind_lab = convert_color(color1_blind_rgb, LabColor)
    color2_blind_lab = convert_color(color2_blind_rgb, LabColor)
    delta_e_blind = delta_e_cie1976(color1_blind_lab, color2_blind_lab)

    delta_of_deltas = abs(delta_e - delta_e_blind)
    percentage_change = delta_of_deltas / delta_e if delta_e else 1
    # we want delta of delta to be smaller than some general value
    # but also we want the delta of deltas to have significantly changed from the original
    if delta_of_deltas > COLOR_MIN_VAL and percentage_change < COLOR_MIN_DELTA:
        return (color1, color2, delta_of_deltas, percentage_change, delta_e, delta_e_blind)
    return None


# input should be props.dominant_colors.colors
# output is a list of bad color combos (if n colors, then n^2 tuples)
def analyze(google_output):
    colors = []
    for color in google_output:
        colors.append(parse_google_color_data(color))
    # TODO: make this faster by not repeating color combos (this would include (red, green) and (green, red))
    output = []
    for color1, color2 in zip(colors, colors):
        if color1 != color2:
            diff = determine_inaccessible_color_combo(color1, color2)
            if diff:
                output.append(diff)
    return output

