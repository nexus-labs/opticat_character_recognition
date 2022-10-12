# Opticat_Character_Recognition
This repository include a simple pipline for 3 different OCRs (EasyOCR, PaddleOCR and DocTr).
##Quick access:
* <a href="https://github.com/nexus-labs/opticat_character_recognition/main/README.md#how-to-install">HOW TO INSTALL</a>
* <a href="https://github.com/nexus-labs/opticat_character_recognition/main/README.md#how-to-run">HOW TO RUN</a>
* <a href="https://github.com/nexus-labs/opticat_character_recognition/main/README.md#how-to-specify-the-ocr">HOW TO SPECIFY THE OCR</a>
* <a href="https://github.com/nexus-labs/opticat_character_recognition/main/README.md#io-info">I/O INFO</a>

## Summary
### how to install:
```
1. git clone git@github.com:nexus-labs/opticat_character_recognition.git
2. cd directry
3. pip install poetry==1.1.8 poetry-core==1.0.4
4. poetry install 
```
### how to run:
put your images on the input folder then run:
```
poetry run python manage.py pipeline --input=input/"" --output=output/
```
you can find the output file inside the output folder.

### how to specify the ocr:
Go to <a href="https://github.com/nexus-labs/opticat_character_recognition/blob/main/config/ocr_settings.yml">ocr_setting</a> and change the value of the Selected_OCR to one of the following (easyocr, paddleocr or doctr).
In the config directory you can find a file for each ocr in case you want to adjust the ocr parameters for example (gpu_usage, language .. etc).

### I/O info
The input of the pipeline is an image. theouput is a dict that includes information about the file, extracted text and the location of each word and it is unified for all supported OCRs. Take a look for the next image for better understanding. 
#### Input
![Alt Text](https://github.com/nexus-labs/opticat_character_recognition/blob/main/input/test.png)
#### output
![Alt Text](https://github.com/nexus-labs/opticat_character_recognition/blob/main/figs/fig1.PNG)
