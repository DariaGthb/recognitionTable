import OcrToTableTool as ottt
import TableExtractor as te
import TableLinesRemover as tlr
import cv2
from PIL import Image
import correctImage as ci
import numpy as np

def main(cropped_image):
    tableArray = []
    imgArray = []
    answerArrays = []
    pieces = ci.hough_lines(cropped_image)
    for piece in pieces:
        answerArray = []
        table_extractor = te.TableExtractor(piece)
        perspective_corrected_image = table_extractor.execute()

        lines_remover = tlr.TableLinesRemover(perspective_corrected_image)
        image_without_lines = lines_remover.execute()


        ocr_tool = ottt.OcrToTableTool(image_without_lines, perspective_corrected_image)
        answerArray.append(ocr_tool.execute())
        answerArrays.append(answerArray[0])

        #tableArray.append()

    return answerArrays
    ottt.OcrToTableTool.generate_csv_file(tableArray)

    cv2.waitKey(0)
    cv2.destroyAllWindows()
