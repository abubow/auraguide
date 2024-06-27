import time
import cv2

def sense_depth(cap, lock, stop_event, debug=False):
    window_name = "Depth Sensing"
    # if debug:
    #     cv2.namedWindow(window_name)
    
    while not stop_event.is_set():
        with lock:
            ret, image = cap.read()
            if not ret:
                break
        
        # if debug and image is not None:
        #     cv2.imshow(window_name, image)
        
        # if debug and cv2.waitKey(1) & 0xFF == ord('q'):
        #     stop_event.set()
        #     break
        
        time.sleep(0.1)  # Simulate some processing time
    
    # if debug:
    #     cv2.destroyWindow(window_name)
    
    print("Depth Sensing Stopped.")
