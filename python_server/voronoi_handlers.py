"""
Author: colorsky
Date: 2020/01/15
"""

from scipy.spatial import Voronoi
from scipy.spatial.qhull import QhullError
from shapely.geometry import Polygon
from polygon_handlers import random_points_inside_polygon, cut_corner, polygon_erode
from multiprocessing import Pool, cpu_count
import numpy as np


def get_clipped_voronoi(polygon: list, points: list):
    """
    Generate regions of voronoi diagram clipped by the polygon.

    :param polygon: Vertices of the polygon.
    :param points: Coordinates of points to construct a convex hull from
    :return: A list of voronoi diagram region's vertices
    """
    minx, miny, maxx, maxy = Polygon(polygon).bounds  # Add mask's boundary
    points += [[minx - 1000, miny - 1000], [maxx + 1000, miny - 1000],
               [maxx + 1000, maxy + 1000], [minx - 1000, maxy + 1000]]
    try:
        voronoi = Voronoi(points)
    except QhullError:
        return []

    regions = [voronoi.vertices[region_idxes] for region_idxes in voronoi.regions if
               -1 not in region_idxes and len(region_idxes) > 2]

    # Clip regions
    clipped_regions = []
    for region in regions:
        clipped_region = None
        if Polygon(polygon).contains(Polygon(region)):
            clipped_region = region.tolist()
        else:
            intersection = Polygon(region).intersection(Polygon(polygon))
            if type(intersection) is not Polygon:
                continue
            intersection = (np.array(intersection.exterior.coords)).tolist()
            if len(intersection) > 2:
                clipped_region = intersection
        if clipped_region:
            clipped_regions.append(clipped_region)
    return clipped_regions


def clipped_voronoi_wrapper(args):
    polygon, n, seed = args
    points = random_points_inside_polygon(polygon, n, seed)
    return get_clipped_voronoi(polygon, points)


def get_clipped_voronoi_multiple_masks(polygons, n: int, seed: int = -1):
    with Pool(cpu_count() - 1) as pool:
        args = [[polygon, n, seed] for polygon in polygons]
        regions = pool.map(clipped_voronoi_wrapper, args)
    pool.close()
    result = []
    for region in regions:
        result += region
    return result


def generate_recursive_voronoi(polygon: list, n: int, d: int = 0, seed: int = -1, round_corner: bool = False,
                               erode: int = 0):
    cur_depth = 0
    output = {cur_depth: [polygon]}
    while cur_depth < d:
        cur_depth += 1
        polygons = get_clipped_voronoi_multiple_masks(output[cur_depth - 1], n, seed)
        if round_corner:
            polygons = [cut_corner(polygon) for polygon in polygons]
        if erode != 0:
            polygons = [polygon_erode(polygon, erode) for polygon in polygons]
            polygons = [polygon for polygon in polygons if polygon]
        output[cur_depth] = polygons
    return output
