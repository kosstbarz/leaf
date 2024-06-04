import math


def rotate_point(x, y, degrees):
    rads = math.radians(degrees)
    return x * math.cos(rads) - y * math.sin(rads), x * math.sin(rads) + y * math.cos(rads)

def rotate_point_relative(x, y, rel_x, rel_y, degrees):
    rotated_x, rotated_y = rotate_point(x - rel_x,y - rel_y, degrees)
    return rotated_x + rel_x, rotated_y + rel_y
