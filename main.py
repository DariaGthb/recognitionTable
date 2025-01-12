import OcrToTableTool as ottt
import TableLinesRemover as tlr
import correctImage as ci


def main(image, coordinates):

    answer_arrays = []
    cropped_image = ci.cropImg(image, coordinates)
    pieces = ci.hough_lines(cropped_image)
    iter_list = [100, 50, 10]
    for i, piece in enumerate(pieces):
        answer_array = []

        lines_remover = tlr.TableLinesRemover(piece, iter_list[i])
        image_without_lines = lines_remover.execute()

        ocr_tool = ottt.OcrToTableTool(image_without_lines, piece)
        reconition_ans = ocr_tool.execute()

        answer_array.append(reconition_ans)
        answer_arrays.append(answer_array[0])

    return answer_arrays
