import cv2
import numpy as np


def cropImg(image, pointsArray):

    sorted_points = sort_points_clockwise(pointsArray)
    x1, y1 = sorted_points[0][0], sorted_points[0][1]
    x2, y2 = sorted_points[2][0], sorted_points[2][1]
    cropped = image[y1:y2, x1:x2]

    return cropped

def hough_lines(image):
    # Блок определения вертикальных линий
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    edges = cv2.Canny(gray, 50, 150, apertureSize=3)

    minLineLength = 100
    lines = cv2.HoughLinesP(image=edges, rho=1, theta=np.pi / 180, threshold=100, lines=np.array([]),
                            minLineLength=minLineLength, maxLineGap=80)

    vertical_lines = []
    for line in lines:
        x1, y1, x2, y2 = line[0]
        # Проверяем, является ли линия вертикальной
        if abs(x1 - x2) < 10:  # Разница между x1 и x2 меньше порога (10 пикселей)
            vertical_lines.append(line[0])

    vertical_lines = sorted(vertical_lines)

    # Получаем высоту и ширину исходного изображения
    height, width = image.shape[:2]

    # Список для хранения разрезанных частей
    pieces = []

    # Начальная координата для разрезания
    prev_x = 0

    # Проходим по каждой вертикальной линии
    for x in vertical_lines:
        # Вырезаем часть изображения от prev_x до x
        piece = image[:, prev_x:x]
        pieces.append(piece)
        prev_x = x

    # Вырезаем последнюю часть до конца изображения, если есть пространство
    if prev_x < width:
        piece = image[:, prev_x:]
        pieces.append(piece)

    for i, piece in enumerate(pieces):
        cv2.imwrite(f'piece_{i}.jpg', piece)

    return pieces

    # Конец блока определения вертикальных линий

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