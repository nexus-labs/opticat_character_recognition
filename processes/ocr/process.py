import numpy
from podder_task_foundation import Context, Payload
from podder_task_foundation import Process as ProcessBase

from .debugger import Debugger
from .ocr import OCR

class Process(ProcessBase):
    def initialize(self, context: Context) -> None:
        selected_ocr = context.shared_config.get('ocr_settings.Selected_OCR')
        self._mean_ocr_threshold =  context.config.get("parameters.mean_ocr_threshold")
        params = context.shared_config.get(f'{selected_ocr}_setting')
        self.reader = OCR(selected_ocr, params)
        self.debugger = Debugger(context)
        self.selected_ocr = selected_ocr


    def execute(self, input_payload: Payload, output_payload: Payload,
                context: Context) -> None:
        context.logger.info(f"Start executing {self.selected_ocr.upper()}.")

        image_objects = input_payload.all(object_type="image")
        ocr_texts = []
        for image_object in image_objects:
            ocr_texts.append(self.reader.extract_text(image_object))
        output_payload.add_array(ocr_texts, name="result")

        # for debug
        self.debugger.execute(input_payload, output_payload)
        context.logger.info(f"Completed {self.selected_ocr.upper()}.")
