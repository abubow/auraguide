# src/face_recognition/face_recognition.py

import cv2
import os
import pickle
import pyttsx3
import sounddevice as sd
import numpy as np
import uuid
import wave
import time
import face_recognition
import keyboard
from imutils import paths

def record_audio(filename, key='r'):
    sample_rate = 44100  # Sample rate
    channels = 2  # Stereo

    recording = []
    recording_active = False

    print(f"Press and hold the '{key}' key to start recording...")
    print(f"Release the '{key}' key to stop recording and save the file.")

    while True:
        event = keyboard.read_event()
        if event.name == key:
            if event.event_type == 'down' and not recording_active:
                print("Recording started...")
                recording_active = True
                recording = []

                def callback(indata, frames, time, status):
                    recording.append(indata.copy())

                stream = sd.InputStream(samplerate=sample_rate, channels=channels, dtype='int16', callback=callback)
                stream.start()

            elif event.event_type == 'up' and recording_active:
                print("Recording stopped.")
                recording_active = False
                stream.stop()
                stream.close()

                audio_data = np.concatenate(recording)
                with wave.open(filename, 'wb') as wf:
                    wf.setnchannels(channels)
                    wf.setsampwidth(2)  # 16-bit PCM
                    wf.setframerate(sample_rate)
                    wf.writeframes(audio_data.tobytes())
                
                print(f"Audio saved as {filename}")
                break

def play_audio(filename):
    # Open the WAV file
    with wave.open(filename, 'rb') as wf:
        # Extract audio data
        sample_rate = wf.getframerate()
        channels = wf.getnchannels()
        frames = wf.readframes(wf.getnframes())
        audio_data = np.frombuffer(frames, dtype=np.int16)
    
    # Reshape audio data to match the number of channels
    audio_data = audio_data.reshape(-1, channels)
    
    # Play the audio
    sd.play(audio_data, samplerate=sample_rate)
    sd.wait()  # Wait until the file is done playing

def recognize_faces(cap, lock, stop_event):
    print("Face recognition started.")
    if not os.path.exists("Images"):
        os.makedirs("Images")
    imagePaths = list(paths.list_images('./Images'))
    knownEncodings = []
    knownNames = []
    last_detected = [None]
    for (i, imagePath) in enumerate(imagePaths):
        image = cv2.imread(imagePath)
        rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        boxes = face_recognition.face_locations(rgb, model='hog')
        encodings = face_recognition.face_encodings(rgb, boxes)
        for encoding in encodings:
            knownEncodings.append(encoding)
            name = imagePath.split("/")
            name = name[-1]
            name = name.replace(".png", "")
            knownNames.append(name)
    data = {"encodings": knownEncodings, "names": knownNames}
    f = open("face_enc", "wb")
    f.write(pickle.dumps(data))
    f.close()
    data = pickle.loads(open('face_enc', "rb").read())
    print("Streaming started")

    window_name = "Face Recognition"
    cv2.namedWindow(window_name)

    while not stop_event.is_set():
        with lock:
            ret, frame = cap.read()
            if not ret:
                break
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        encodings = face_recognition.face_encodings(rgb)
        names = []
        for encoding in encodings:
            matches = face_recognition.compare_faces(data["encodings"], encoding)
            name = "Unknown"
            if True in matches:
                matchedIdxs = [i for (i, b) in enumerate(matches) if b]
                counts = {}
                for i in matchedIdxs:
                    name = data["names"][i]
                    counts[name] = counts.get(name, 0) + 1
                name = max(counts, key=counts.get)
                name = os.path.basename(name)
            names.append(name)
        if last_detected != names:
            if len(names) == 1 and names[0] == "Unknown":
                pyttsx3.speak("Unknown Person Detected. Press 1 if you want to save this person.")
                timeout = 5
                start_time = time.time()
                while True:
                    if keyboard.is_pressed('1'):
                        pyttsx3.speak("Please tell the name of the person")
                        # get unique id using uuid
                        name = str(uuid.uuid1())
                        record_audio("./Audio/" + name + ".wav")
                        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                        box = face_recognition.face_locations(rgb_frame, model='hog')
                        top, right, bottom, left = box[0]
                        face = frame[top:bottom, left:right]
                        cv2.imwrite("./Images/" + name + ".png", face)
                        pyttsx3.speak("Person added")
                        return
                    if time.time() - start_time > timeout:
                        pyttsx3.speak("Timeout, person ignored")
                        break
            elif len(names) > 0:
                print(names)
                # Calculate the number of unknown persons and remove them after finding the number
                count = 0
                for i in names:
                    if i == "Unknown":
                        count += 1
                if count < len(names):
                    pyttsx3.speak("Persons detected are ")
                    for i in range(0, len(names)):
                        if names[i] != "Unknown":
                            play_audio("./Audio/" + names[i] + ".wav")
                        if i != len(names) - 1 and names[i + 1] != "Unknown":
                            pyttsx3.speak("and")
                if count > 1:
                    pyttsx3.speak(f"{count} unknown persons detected")
            else:
                pyttsx3.speak("No person detected")
        last_detected = names
        names = []

        if frame is not None:
            cv2.imshow(window_name, frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            stop_event.set()
            break
        time.sleep(0.1)  # Simulate some processing time

    cv2.destroyWindow(window_name)
    print("Face Recognition Stopped.")

def store_unknown_faces(cap, lock, stop_event):
    window_name = "Face Store"
    cv2.namedWindow(window_name)
    while not stop_event.is_set():
        with lock:
            ret, frame = cap.read()
            if not ret:
                break
        if frame is not None:
            cv2.imshow(window_name, frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            stop_event.set()
            break
        time.sleep(0.1)  # Simulate some processing time
    cv2.destroyWindow(window_name)
    print("Face Store Stopped.")
