import cv2
import numpy as np


def cropImg(image, pointsArray):
    coordinates = (pointsArray[0], pointsArray[1], image.width - pointsArray[2], image.height - pointsArray[3])
    cropped = image.crop(coordinates)
    cropped.save("image/temp/rotated.jpg")
    return "image/temp/rotated.jpg"

def apply_perspective_transform(image, array):
    pts1 = np.float32(array)
    pts2 = np.float32(
        [[0, 0], [image.shape[1], 0], [image.shape[1], image.shape[0]], [0, image.shape[0]]])
    matrix = cv2.getPerspectiveTransform(pts1, pts2)
    perspective_corrected_image = cv2.warpPerspective(image, matrix,
                                                           (image.shape[1], image.shape[0]))
    cv2.imwrite("image/temp/perspective_corrected_image.jpg", perspective_corrected_image)


image =  cv2.imread("image/fullImg2.png")
arr = []
nparr1 = np.array([86,124])
nparr2 = np.array([1132, 32])
nparr3 = np.array([1202, 760])
nparr4 = np.array([162, 864])
arr = [nparr1, nparr2, nparr3, nparr4]
arr = np.asarray(arr)
apply_perspective_transform(image, arr)

