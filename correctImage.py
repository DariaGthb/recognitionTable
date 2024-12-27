import cv2
import numpy as np


def cropImg(image, pointsArray):

    sorted_points = sort_points_clockwise(pointsArray)
    x1, y1 = sorted_points[0][0], sorted_points[0][1]
    x2, y2 = sorted_points[2][0], sorted_points[2][1]
    cropped = image[y1:y2, x1:x2]

    cv2.imwrite("image/temp/rotated.jpg", cropped)
    return "image/temp/rotated.jpg"


def sort_points_clockwise(points):

    vectorized_func = np.vectorize(int)
    points_int = vectorized_func(points)

    top_left = points_int[np.argmin(points_int[:, 0] + points_int[:, 1])]  # точка с минимальными X и Y
    bottom_right = points_int[np.argmax(points_int[:, 0] + points_int[:, 1])]  # точка с максимальными X и Y

    # Остальные две точки
    remaining_coords = [p for p in points_int if not np.array_equal(p, top_left) and not np.array_equal(p, bottom_right)]

    # Верхняя правая и нижняя левая
    if remaining_coords[0][1] < remaining_coords[1][1]:
        top_right = remaining_coords[0]
        bottom_left = remaining_coords[1]
    else:
        top_right = remaining_coords[1]
        bottom_left = remaining_coords[0]

    return [top_left, top_right, bottom_right, bottom_left]