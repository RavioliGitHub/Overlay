import math


def in_range(x1, y1, x2, y2, margin=0.0):
    distance = math.sqrt(math.pow(float(x1) - float(x2), 2) + math.pow(float(y1) - float(y2), 2))
    print(distance)
    return distance < margin
