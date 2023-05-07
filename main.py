#!/usr/bin/env python3

"""
This code creates images inspired by the works of Nathaniel Price, you can check out his
https://www.artsy.net/artist/nathaniel-price
"""

from PIL import Image, ImageDraw

import numpy as np

def to_int_pair(v: np.array) -> (int, int):
    return (int(v[0]), int(v[1]))

def to_bbox(c: np.array, r: int) -> [(int,int), (int,int)]:
    return [to_int_pair(c - r), to_int_pair(c + r)]

def main():
    # Originally I'll start with a 2000x2000 image, then I'll downsample to get the circles anti-aliased.
    c_width = 2000.0
    c_extent = (c_width / 2.0) * 0.8

    c_size = np.array([c_width, c_width])
    c_origin = c_size / 2.0

    im = Image.new('RGB', to_int_pair(c_size),  "WHITE")
    draw = ImageDraw.Draw(im)

    # IDK I just went to https://color.adobe.com/create/color-wheel
    colors = ["#5C3B1E", "#F55734", "#DB8D48", "#D46300", "#A86B37"]

    # I want a thick outer ring, with a low prob. of things showing up in the middle.
    # Instead of tuning a fancy distribution, I just opted for a uniform distribution to create the
    # thick ring, and a power distribution to do a random sparse fill of other areas.
    rs = []
    rs += list(np.random.uniform(0.7, 1.0, 200))
    rs += list(1.0 - r for r in np.random.power(0.2, 10))

    for r in rs:
        if r > 0.2:
            draw.ellipse(to_bbox(c_origin, r * c_extent), outline=np.random.choice(colors))

    # We're doing a resize here to achieve antialiasing
    im = im.resize(to_int_pair(c_size / 2.0), resample=Image.LANCZOS)
    im.save('img.png')


if __name__ == '__main__':
    main()
