import OcrToTableTool as ottt
import TableExtractor as te
import TableLinesRemover as tlr
import cv2
from PIL import Image
import correctImage as ci
import numpy as np


tableArray = []
imgArray = []

image = Image.open("image/FullDoc.jpg")
path = ci.cropImg(image, [14, 300, 10, 70])
#imgArray = ['image/first_column.png',"image/second_column_2.png"]
imgArray.append(path)
for i in range(1):
    path_to_image = "image/first_column.png"#imgArray[i]
    table_extractor = te.TableExtractor(path_to_image)
    perspective_corrected_image = table_extractor.execute()
    cv2.imshow("perspective_corrected_image", perspective_corrected_image)

    lines_remover = tlr.TableLinesRemover(perspective_corrected_image)
    image_without_lines = lines_remover.execute()
    cv2.imshow("image_without_lines", image_without_lines)

    ocr_tool = ottt.OcrToTableTool(image_without_lines, perspective_corrected_image)
    tableArray.append(ocr_tool.execute())

    # Блок определения вертикальных линий
    gray = cv2.imread(path_to_image)
    edges = cv2.Canny(gray, 50, 150, apertureSize=3)

    minLineLength = 100
    lines = cv2.HoughLinesP(image=edges, rho=1, theta=np.pi / 180, threshold=100, lines=np.array([]),
                            minLineLength=minLineLength, maxLineGap=80)

    for line in lines:
        x1, y1, x2, y2 = line[0]
        # Проверяем, является ли линия вертикальной
        if abs(x1 - x2) < 10:  # Разница между x1 и x2 меньше порога (10 пикселей)
            cv2.line(gray, (x1, y1), (x2, y2), (0, 255, 0), 2)

    cv2.imwrite('image/temp/houghlines5.jpg', gray)

    # Конец блока определения вертикальных линий

ottt.OcrToTableTool.generate_csv_file(tableArray)

cv2.waitKey(0)
cv2.destroyAllWindows()
