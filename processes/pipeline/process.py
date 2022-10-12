from podder_task_foundation import Context, Payload
from podder_task_foundation import Process as ProcessBase
from podder_task_foundation.pipeline import Pipeline

class Process(ProcessBase):
    def initialize(self, context: Context) -> None:
        pass
    
    def execute(self, input_payload: Payload, output_payload: Payload,
                context: Context):
        self.context.logger.info("Start ...")
        ocr_output = Pipeline.execute_process(
            "ocr", input_payload=input_payload, context=context)
        ocr_output_data = ocr_output.get_data()
        output_payload.add_array(ocr_output_data)
