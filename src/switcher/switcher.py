# src/switcher/switcher.py

from threading import Thread, Event
from face_recognition.face_recognition import recognize_faces
from object_detection.object_detection import detect_objects
from depth_sense.depth_sense import sense_depth
from ocr.ocr import perform_ocr

class ModuleSwitcher:
    def __init__(self):
        self.current_thread = None
        self.stop_event = Event()

    def run_face_recognition(self, image):
        result = recognize_faces(image, self.stop_event)
        if result:
            print(f"Face Recognition Result: {result}")

    def run_object_detection(self, image):
        result = detect_objects(image, self.stop_event)
        if result:
            print(f"Object Detection Result: {result}")

    def run_depth_sense(self, image):
        result = sense_depth(image, self.stop_event)
        if result:
            print(f"Depth Sense Result: {result}")

    def run_ocr(self, image):
        result = perform_ocr(image, self.stop_event)
        if result:
            print(f"OCR Result: {result}")

    def switch_module(self, module_number, image):
        # Stop the current thread if it's running
        if self.current_thread and self.current_thread.is_alive():
            self.stop_event.set()
            self.current_thread.join()

        # Clear the stop event for the new thread
        self.stop_event.clear()

        if module_number == 1:
            self.current_thread = Thread(target=self.run_face_recognition, args=(image,))
        elif module_number == 2:
            self.current_thread = Thread(target=self.run_object_detection, args=(image,))
        elif module_number == 3:
            self.current_thread = Thread(target=self.run_depth_sense, args=(image,))
        elif module_number == 4:
            self.current_thread = Thread(target=self.run_ocr, args=(image,))
        else:
            print("Invalid module number.")
            return

        # Start the new thread
        self.current_thread.start()
