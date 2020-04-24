from geo_analysis.county_coordinates import *
from geo_analysis.county_geo_codes import *
import ast


def pnpoly(point, area):
    nvert = len(area)
    i = 0
    j = nvert - 1
    c = False
    while i < nvert:
        if (area[i][1] > point[1]) != (area[j][1] > point[1]) and point[0] < ((area[j][0] - area[i][0]) * (point[1] - area[i][1]) / (area[j][1] - area[i][1]) + area[i][0]):
            c = not c
        j = i
        i += 1
    return c


def county_of(point):
    for geo_id in county_coordinates:
        if pnpoly(point, county_coordinates[geo_id]):
            return geo_id, geo_county[geo_id]
    return "", ""


def area_to_point(bounding_box):
    bounding_box = ast.literal_eval(bounding_box)["coordinates"][0]
    x = 0
    y = 0
    count = 0
    for coordinate in bounding_box:
        count += 1
        x += float(coordinate[0])
        y += float(coordinate[1])
    return x / count, y / count
