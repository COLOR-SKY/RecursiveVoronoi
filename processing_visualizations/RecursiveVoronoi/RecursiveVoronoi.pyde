"""
Author: colorsky
Date: 2020/02/19
"""

import sys
import math
# Replace with your environment dir
sys.path.append('/Python Project/venv_2.7/lib/python2.7/site-packages/')
import requests

add_library("SVG")

global n, d, seed
n = 15
d = 3
seed = -1

def circle_points(r, n, xoff=0, yoff=0):
    return [(math.cos(2 * math.pi / n * x) * r + xoff, math.sin(2 * math.pi / n * x) * r + yoff) for x in range(0, n)]

def setup():
    size(960, 540)

def draw():
    # beginRecord(SVG, "./output/" + str(int(random(0, 9999))) + ".svg")
    background(255)
    polygon_mask = circle_points(200, 100, width / 2, height / 2)
    polygon_mask = [[10, 10], [width - 10, 10],
                    [width - 10, height - 10], [10, height - 10]]
    api = "http://127.0.0.1:5699/RecursiveVoronoi"
    data = {
        "polygon": polygon_mask,
        "n": n,
        "d": d,
        "seed": seed,
        "round_corner": False,
        "erode": 0
    }

    noStroke()
    fill(0)
    # ellipse(width / 2, height / 2, 400, 400)
    voronoi_regions = requests.post(api, json=data).json()
    voronoi_regions = [voronoi_regions[depth] for depth in voronoi_regions]
    voronoi_regions.reverse()
    for depth, polygons in enumerate(voronoi_regions):
        if depth == d:
            continue
        strokeWeight(map(depth, 0, d, 0.3, 2))
        noFill()
        # stroke(0)
        for polygon in polygons:
            p = createShape()
            p.beginShape()
            for x, y in polygon:
                p.vertex(x, y)
            p.endShape(CLOSE)
            stroke(random(55) + (d - depth) * 30, random(55) +
                   (d - depth) * 30, random(55) + (d - depth) * 30)
            shape(p)

    # endRecord()
    noLoop()
