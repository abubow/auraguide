import cv2
from paddleocr import PaddleOCR, draw_ocr

# Initialize PaddleOCR with the specified model
ocr = PaddleOCR(det_model_dir=None, rec_model_dir='PaddleOCR/ocr_rec/en_PP-OCRv3_rec', use_angle_cls=True, lang='en')

# Open the video capture
cap = cv2.VideoCapture(1)  # 0 is usually the default camera

# Check if the camera opened successfully
if not cap.isOpened():
    print("Error: Could not open video stream.")
    exit()

while True:
    # Capture frame-by-frame
    ret, frame = cap.read()

    # If frame is read correctly, ret is True
    if not ret:
        print("Error: Can't receive frame (stream end?). Exiting ...")
        break

    # Perform OCR on the frame
    result = ocr.ocr(frame, cls=True)

    # Extract and print OCR text
    for line in result:
        for word_info in line:
            word = word_info[1][0]
            print(f"OCR Text: {word}")

    # Display the resulting frame
    cv2.imshow('OCR Video Feed', frame)

    # Break the loop on 'q' key press
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the capture
cap.release()
cv2.destroyAllWindows()
