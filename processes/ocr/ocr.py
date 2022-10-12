import numpy
import torch
import easyocr
from paddleocr import PaddleOCR
import os
import logging

class OCR:
    def __init__(self, selected_ocr, params):

        self.params = params
        if selected_ocr == "easyocr":
            self.ocr = easyocr.Reader(
                [self.params['ocr_language']],
                gpu = self.params['use_gpu'],
                quantize = self.params['quantize'])

        if selected_ocr == "paddleocr":
            self.ocr = PaddleOCR(use_angle_cls = self.params['use_angle_cls'], lang = self.params['ocr_language'])

        if selected_ocr == "doctr":
            os.environ['USE_TORCH'] = '1'
            from doctr.models import ocr_predictor
            self.ocr = ocr_predictor(pretrained = self.params['pretrained'])

        self.selected_ocr = selected_ocr

    @staticmethod
    def reorganize_output(word, points_numpy, confidence_score_decimal, image_height, image_width):
        x_min = int(max([points_numpy[:, 0].min() * image_width, 0]))
        y_min = int(max([points_numpy[:, 1].min() * image_height, 0]))
        x_max = int(min([points_numpy[:, 0].max() * image_width, image_width]))
        y_max = int(min([points_numpy[:, 1].max() * image_height, image_height]))
        return {
            "value": word,
            "confidence_score": confidence_score_decimal * 100,
            "bbox": {
                "left": x_min,
                "top": y_min,
                "right": x_max,
                "bottom": y_max
            }
        }

    @staticmethod
    def get_mean_confidence(words):
        return numpy.mean([word["confidence_score"] for word in words])

    def extract_text(self, image_object):
        mean_confidence_score = 0
        words = []
        file_name = image_object.name
        image_numpy = numpy.array(image_object.data)
        image_height, image_width = image_numpy.shape[:2]

        if self.selected_ocr == "easyocr":
            ocr_results = self.ocr.readtext(image_numpy)
            for points, word, confidence_score_decimal in ocr_results:
                if word == "":
                    continue
                points_numpy = numpy.array(points)
                words.append(self.reorganize_output(word, points_numpy, confidence_score_decimal, image_height, image_width))

        if self.selected_ocr == "doctr":
            ocr_results = self.ocr([image_numpy]).export()
            for page in ocr_results['pages']:
                for block in page['blocks']:
                    for line in block['lines']:
                        for word_info in line['words']:
                            points = word_info['geometry']
                            word = word_info['value']
                            confidence_score_decimal = word_info['confidence']
                            if word == "":
                                continue
                            points_numpy = numpy.array(points)
                            words.append(self.reorganize_output(word, points_numpy, confidence_score_decimal, image_height, image_width))

        if self.selected_ocr == "paddleocr":
            result = self.ocr.ocr(image_numpy.copy(), cls=False)
            for i in range(len(result)):
                points = result[i][0]
                word = result[i][1][0]
                confidence_score_decimal = result[i][1][1]
                if word == "":
                    continue
                points_numpy = numpy.array(points)
                words.append(self.reorganize_output(word, points_numpy, confidence_score_decimal, image_height, image_width))
        if len(words) > 0:
            mean_confidence_score = self.get_mean_confidence(words)

        return {
                "file_name": file_name,
                "image_width": image_width,
                "image_height": image_height,
                "mean_confidence_score": mean_confidence_score,
                "words": words
            }