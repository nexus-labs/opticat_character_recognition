import os
import logging

# Prevent multiple level parallel issue of
# huggingface/tokenizers: The current process just got forked, after parallelism has already been used
os.environ['TOKENIZERS_PARALLELISM'] = 'false'

# Prevent Keep getting CUDA OOM error with Pytorch failing to allocate all free memory
os.environ['PYTORCH_CUDA_ALLOC_CONF'] = 'max_split_size_mb:128'

# Prevent multiple level parallel issue of
# huggingface/tokenizers: The current process just got forked, after parallelism has already been used
os.environ['TOKENIZERS_PARALLELISM'] = 'false'

# Set global log level for 3rd party packages
# EasyOCR, Yolov5 are using a global logger so override log level here
logging.basicConfig(level=logging.ERROR)

from podder_task_foundation import CLI


if __name__ == '__main__':
    CLI().execute()
