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
#imgArray = ['image/first_column.png',"image/second_column_2.png"]
#imgArray.append(path)
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


ottt.OcrToTableTool.generate_csv_file(tableArray)

cv2.waitKey(0)
cv2.destroyAllWindows()
