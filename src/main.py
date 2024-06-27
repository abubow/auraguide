import cv2
import threading
import time
import keyboard
import sounddevice as sd

def get_default_audio_device():
    default_device_index = sd.default.device
    if isinstance(default_device_index, (tuple, list)):
        input_device_index, output_device_index = default_device_index
    else:
        input_device_index = output_device_index = default_device_index

    input_device = sd.query_devices(input_device_index)
    output_device = sd.query_devices(output_device_index)

    print(f"Default Input Device: {input_device['name']}")
    print(f"Default Output Device: {output_device['name']}")

# Check the current default audio device

def list_audio_devices():
    devices = sd.query_devices()
    for idx, device in enumerate(devices):
        print(f"{idx}: {device['name']} (Input channels: {device['max_input_channels']}, Output channels: {device['max_output_channels']})")
    return devices

def set_default_audio_device(device_name):
    devices = list_audio_devices()
    for idx, device in enumerate(devices):
        if device_name in device['name']:
            sd.default.device = idx
            print(f"Default audio device set to: {device['name']}")
            time.sleep(1)
            return
    print(f"Audio device '{device_name}' not found.")

# List all audio devices
# list_audio_devices()

# Set the default audio device to "USB Audio Device"
get_default_audio_device()
set_default_audio_device("USB Audio Device")
get_default_audio_device()

from switcher.switcher import switch_module, switch_sub_mode, audio_handler
from speaker.tts import start_audio_thread
current_mode = 0
modes = [1, 2, 3, 4, 5]  # Corresponds to the modes: Face Recognition, Object Detection, Depth Sense, OCR, Sleep Mode

def main(debug=False):
    global cap, lock, stop_event, current_mode, modes

    # Initialize the camera
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Error: Could not open camera.")
        return

    lock = threading.Lock()
    stop_event = threading.Event()
    audio_handler.add_audio_task("Starting-Aurasense")
    print("Starting Aurasense")
    # Start the audio thread
    audio_thread = start_audio_thread(audio_handler)

    try:
        while True:
            if keyboard.is_pressed('page down'):
                current_mode = (current_mode + 1) % len(modes)
                print(f'Switching to mode {current_mode + 1}')
                switch_module(modes[current_mode], cap, lock, stop_event, debug)
                time.sleep(0.1)  # Add a short delay
            elif keyboard.is_pressed('page up'):
                current_mode = (current_mode - 1) % len(modes)
                print(f'Switching to mode {current_mode + 1}')
                switch_module(modes[current_mode], cap, lock, stop_event, debug)
            elif keyboard.is_pressed('tab'):
                print(f'Switching to submode')
                if current_mode in [1, 2]:  # Face Recognition and Object Detection modes have sub-modes
                    switch_sub_mode(1, current_mode, cap, lock, stop_event, debug)
            elif keyboard.is_pressed('enter'):
                print(f'Switching to submode')
                if current_mode in [1, 2]:  # Face Recognition and Object Detection modes have sub-modes
                    switch_sub_mode(-1, current_mode, cap, lock, stop_event, debug)
            time.sleep(1)  # Short delay to reduce CPU usage
    except KeyboardInterrupt:
        print("Exiting...")
    finally:
        stop_event.set()
        cap.release()
        # cv2.destroyAllWindows()
        audio_handler.stop()
        audio_thread.join()

if __name__ == "__main__":
    main(debug=True)  # Set debug to True or False as needed
