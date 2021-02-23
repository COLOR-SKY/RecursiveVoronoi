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
n = 10
d = 3
seed = 897989

def circle_points(r, n, xoff=0, yoff=0):
    return [(math.cos(2 * math.pi / n * x) * r + xoff, math.sin(2 * math.pi / n * x) * r + yoff) for x in range(0, n)]

def setup():
    size(1700, 500)

def draw():
    beginRecord(SVG, "depth.svg")
    background(255)
    polygon_mask = circle_points(200, 100, 0, 0)
    api = "http://127.0.0.1:5699/RecursiveVoronoi"
    data = {
        "polygon": polygon_mask,
        "n": n,
        "d": d,
        "seed": seed,
        "round_corner": False
    }

    translate(220, height / 2 + 30)
    voronoi_regions = requests.post(api, json=data).json()
    color_map = {
        0: color(0, 0, 0),
        1: color(0, 0, 255),
        2: color(255, 0, 0),
        3: color(0, 255, 0)
    }
    for depth in voronoi_regions:
        for depth_ in range(int(depth), -1, -1):
            polygons = voronoi_regions[str(depth_)]
            noFill()
            stroke(color_map[depth_])
            strokeWeight(map(depth_, 0, d, 5, 1))
            for polygon in polygons:
                p = createShape()
                p.beginShape()
                for x, y in polygon:
                    p.vertex(x, y)
                p.endShape(CLOSE)
                shape(p)
        title = "Depth = " + depth
        fill(color_map[int(depth)])
        noStroke()
        textSize(20)
        textAlign(CENTER)
        text(title, 0, -220)
        translate(410, 0)
    
    endRecord()
    noLoop()
