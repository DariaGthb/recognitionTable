import cv2
import numpy as np


def cropImg(image, pointsArray):

    x1, y1 = int(pointsArray[0][0]), int(pointsArray[0][1])
    x2, y2 = int(pointsArray[2][0]), int(pointsArray[2][1])
    cropped = image[y1:y2, x1:x2]

    cv2.imwrite("image/temp/rotated.jpg", cropped)
    return "image/temp/rotated.jpg"


def apply_perspective_transform(image, array):
    pts1 = np.float32(array)
    pts2 = np.float32(
        [[0, 0], [image.shape[1], 0], [image.shape[1], image.shape[0]], [0, image.shape[0]]])
    matrix = cv2.getPerspectiveTransform(pts1, pts2)
    perspective_corrected_image = cv2.warpPerspective(image, matrix,
                                                           (image.shape[1], image.shape[0]))
    cv2.imwrite("image/temp/perspective_corrected_image.jpg", perspective_corrected_image)

