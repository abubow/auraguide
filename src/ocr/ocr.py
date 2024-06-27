import cv2
from paddleocr import PaddleOCR, draw_ocr

ocr = PaddleOCR(det_model_dir=None, rec_model_dir='PaddleOCR/ocr_rec/en_PP-OCRv3_rec', use_angle_cls=True, lang='en')
print("Loaded OCR model")
def perform_ocr(cap, lock, stop_event, debug=False):
    # if debug:
    #     cv2.namedWindow('OCR Video Feed')

    while not stop_event.is_set():
        with lock:
            ret, frame = cap.read()
            if not ret:
                print("Error: Can't receive frame (stream end?). Exiting ...")
                break

        # if debug:
        #     cv2.imshow('OCR Video Feed', frame)

        # Perform OCR on the frame
        result = ocr.ocr(frame, cls=True)

        # Extract and print OCR text
        if len(result) != 0:
            for line in result:
                if line is not None:
                    for word_info in line:
                        word = word_info[1][0]
                        print(f"OCR Text: {word}")

    #     if debug and cv2.waitKey(1) & 0xFF == ord('q'):
    #         stop_event.set()
    #         break

    # if debug:
    #     cv2.destroyWindow('OCR Video Feed')