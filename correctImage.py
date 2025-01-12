import cv2
import numpy as np


def cropImg(image, pointsArray):
    reserve = 10
    sorted_points = sort_points_clockwise(pointsArray)
    x1, y1 = sorted_points[0][0] - reserve, sorted_points[0][1] - reserve
    x2, y2 = sorted_points[2][0] + reserve, sorted_points[2][1] + reserve

    cropped = image[max(y1, 0):min(y2, image.shape[0]), max(x1, 0):min(x2, image.shape[1])]

    return cropped


def hough_lines(image):
    # Блок определения вертикальных линий
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    edges = cv2.Canny(gray, 50, 150, apertureSize=3)

    minLineLength = 100
    lines = cv2.HoughLinesP(image=edges, rho=1, theta=np.pi / 180, threshold=100, lines=np.array([]),
                            minLineLength=minLineLength, maxLineGap=80)

    pieces = []
    if lines is not None:
        # Сортируем координаты по X (если вертикальные линии)
        lines = sorted(lines, key=lambda x: x[0][0])

        # Получаем высоту и ширину изображения
        height, width = image.shape[:2]

        # Список для хранения разрезанных частей
        pieces = []

        # Начальная координата для разрезания
        prev_x = 0

        # Разрезаем по вертикальным линиям
        for line in lines:
            x1, y1, x2, y2 = line[0]
            # Только вертикальные линии
            if abs(x1 - x2) < 10:  # Разница между x1 и x2 меньше порога (10 пикселей)
                cv2.line(gray, (x1, y1), (x2, y2), (0, 255, 0), 2)
            else:
                continue
            # Вырезаем часть изображения от prev_x до текущей линии
            piece = image[:, prev_x:x1]

            if piece.shape[1] > 100:
                pieces.append(piece)
                prev_x = x1

        cv2.imwrite('image/temp/houghlines5.jpg', gray)

        # Вырезаем последнюю часть, если есть
        if prev_x < width and image[:, prev_x:].shape[1] > 100:
            piece = image[:, prev_x:]
            pieces.append(piece)

        for i, piece in enumerate(pieces):
            try:
                path = "./process_images/pieces/" + f'piece_{i}.jpg'
                cv2.imwrite(path, piece)
            except:
                print("Error")

    return pieces


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