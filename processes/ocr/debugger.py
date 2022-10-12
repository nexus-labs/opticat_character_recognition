import json
import os
from pathlib import Path

import cv2
import numpy
from podder_task_foundation import Context, Payload


class Debugger:
    def __init__(self, context: Context) -> None:
        self.context = context
        self.image_with_words_directory_name = "images_with_words"
        self.is_debug_mode = bool(
            context.shared_config.get("debug.debug_mode"))

    def execute(self, input_payload: Payload, output_payload: Payload) -> None:
        if self.is_debug_mode:
            tmp_directory = self._create_debug_directory()
            self._put_output_data_for_debug(tmp_directory, output_payload)
            self._put_images_with_words_for_debug(tmp_directory, input_payload,
                                                  output_payload)

    def _create_debug_directory(self) -> Path:
        debug_root_path = str(
            self.context.shared_config.get("debug.debug_directory_name"))
        debug_directory_name = os.path.join(debug_root_path,
                                            self.context.job_id,
                                            self.context.process_name)
        if not os.path.isdir(debug_directory_name):
            os.makedirs(debug_directory_name)

        return Path(debug_directory_name)

    @staticmethod
    def _put_output_data_for_debug(tmp_directory: Path,
                                   output_payload: Payload) -> None:
        ocr_results = output_payload.get_data()
        file_name = ""
        if len(ocr_results) > 0:
            file_name = ocr_results[0]["file_name"]
        output_file_path = os.path.join(str(tmp_directory), f'{file_name}_output.json')
        with open(output_file_path, mode='w') as output_file:
            output_file.write(json.dumps(output_payload.get_data(), indent=4))

    @staticmethod
    def _put_images_with_words_for_debug(tmp_directory, input_payload,
                                         output_payload):

        ocr_results = output_payload.get_data()
        image_objects = input_payload.all(object_type="image")
        for ocr_result, image_object in zip(ocr_results, image_objects):
            image = numpy.array(image_object.data).copy()
            if len(image.shape) == 2:
                image = cv2.cvtColor(image, cv2.COLOR_GRAY2RGB)
            if image.shape[2] == 4:
                image = image[:, :, :3].astype(numpy.uint8)
            words = ocr_result["words"]
            file_name = ocr_result["file_name"]
            for word in words:
                bbox = word["bbox"]
                x1, y1, x2, y2 = bbox["left"], bbox["top"], bbox[
                    "right"], bbox["bottom"]
                cv2.rectangle(image, (x1, y1), (x2, y2), (0, 0, 255), 5)
            file_path = f'{str(tmp_directory)}/{file_name}'
            file_path = file_path.replace(".pdf", ".png")
            cv2.imwrite(file_path, image)
