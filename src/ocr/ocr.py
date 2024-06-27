# src/ocr/ocr.py

import cv2
from paddleocr import PaddleOCR, draw_ocr

ocr = PaddleOCR(det_model_dir=None, rec_model_dir='PaddleOCR/ocr_rec/en_PP-OCRv3_rec', use_angle_cls=True, lang='en')
def perform_ocr(cap, lock, stop_event):
    while True:
        ret, frame = cap.read()
        cv2.imshow('OCR Video Feed', frame)

            # If frame is read correctly, ret is True
        if not ret:
            print("Error: Can't receive frame (stream end?). Exiting ...")

        # Perform OCR on the frame
        result = ocr.ocr(frame, cls=True)

        # Extract and print OCR text
        if len(result) != 0:
            for line in result:
                if line is not None:
                    for word_info in line:
                        word = word_info[1][0]
                        print(f"OCR Text: {word}")
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
