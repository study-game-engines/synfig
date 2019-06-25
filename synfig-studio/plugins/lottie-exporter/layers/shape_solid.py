"""
Will store all the functions corresponding to shapes which will be masked as
shapes in lottie
"""

import sys
import settings
from helpers.transform import gen_helpers_transform
from helpers.blendMode import get_blend
from helpers.mask import gen_mask
from misc import Count, get_color_hex, is_animated
from effects.fill import gen_effects_fill
sys.path.append("..")


def gen_layer_shape_solid(lottie, layer, idx):
    """
    Generates the dictionary corresponding to layers/shapes.json

    Args:
        lottie (dict)               : Lottie generated solid layer stored here
        layer  (lxml.etree._Element): Synfig format solid layer
        idx    (int)                : Stores the index(number of) of solid layer

    Returns:
        (None)
    """
    # Setting the solid layer which will be masked
    index = Count()
    lottie["ddd"] = settings.DEFAULT_3D
    lottie["ind"] = idx
    lottie["ty"] = settings.LAYER_SOLID_TYPE
    lottie["nm"] = settings.LAYER_SOLID_NAME + str(idx)
    lottie["sr"] = settings.LAYER_DEFAULT_STRETCH
    lottie["ks"] = {}   # Transform properties to be filled
    lottie["ef"] = []   # Stores the effects

    pos = [settings.lottie_format["w"]/2, settings.lottie_format["h"]/2]
    anchor = pos
    gen_helpers_transform(lottie["ks"], layer, pos, anchor)

    lottie["ef"].append({})
    gen_effects_fill(lottie["ef"][-1], layer, index.inc())

    lottie["ao"] = settings.LAYER_DEFAULT_AUTO_ORIENT
    lottie["sw"] = settings.lottie_format["w"]  # Solid Width
    lottie["sh"] = settings.lottie_format["h"]  # Solid Height

    invert = False
    for chld in layer:
        if chld.tag == "param":
            if chld.attrib["name"] == "color":
                lottie["sc"] = get_color_hex(chld[0])   # Solid Color
            elif chld.attrib["name"] == "invert":
                is_animate = is_animated(chld[0])
                if is_animate == 0:
                    val = chld[0].attrib["value"]
                elif is_animate == 1:
                    val = chld[0][0][0].attrib["value"]
                else:
                    # If animated, always set invert to false
                    val = "false"
                if val == "true":
                    invert = True
            elif chld.attrib["name"] in {"bline", "vector_list"}:
                bline_point = chld[0]
            elif chld.attrib["name"] == "origin":
                origin = chld

    lottie["ip"] = settings.lottie_format["ip"]
    lottie["op"] = settings.lottie_format["op"]
    lottie["st"] = 0            # Don't know yet
    get_blend(lottie, layer)
    lottie["markers"] = []      # Markers to be filled yet

    hasMask = True

    lottie["hasMask"] = hasMask
    lottie["masksProperties"] = []
    lottie["masksProperties"].append({})

    gen_mask(lottie["masksProperties"][0], invert, bline_point, index)
