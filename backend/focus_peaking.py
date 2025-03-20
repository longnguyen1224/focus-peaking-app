import cv2
import numpy as np
import os
import platform
from flask import Flask, Response, request, jsonify
from flask_cors import CORS
import threading

app = Flask(__name__)
CORS(app)

if platform.system() == "Windows":
    VIDEO_PATH = "D:\\focus-peaking-project\\exploreHD-Focus.mp4"
else:
    VIDEO_PATH = "/mnt/d/focus-peaking-project/exploreHD-Focus.mp4"
is_paused = False
lock = threading.Lock()

def focus_peaking(frame):
    """ Apply focus peaking effect by detecting edges in the frame """
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    edges = cv2.Canny(gray, 100, 200)
    edges_colored = np.zeros_like(frame)
    edges_colored[:, :, 2] = edges  # Apply red overlay
    highlighted = cv2.addWeighted(frame, 0.7, edges_colored, 1.0, 0)
    return highlighted

def generate_frames(apply_focus_peaking=True):
    """ Stream video frames from file or webcam with optional focus peaking effect """
    global is_paused

    # ✅ Close any previous video source and open new one
    cap = cv2.VideoCapture(VIDEO_PATH)
    if not cap.isOpened():
        print("ERROR: Cannot open video source.")
        return

    while True:
        with lock:
            if is_paused:
                continue  # Skip frame processing when paused

        success, frame = cap.read()
        if not success:
            print("Restarting video...")
            cap.set(cv2.CAP_PROP_POS_FRAMES, 0)  # Restart video if it's a file
            continue

        if apply_focus_peaking:
            frame = focus_peaking(frame)

        _, buffer = cv2.imencode('.jpg', frame)
        frame_bytes = buffer.tobytes()

        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')

    cap.release()

@app.route('/video_feed')
def video_feed():
    """ Serve the video feed (either webcam or video) with focus peaking """
    return Response(generate_frames(apply_focus_peaking=True), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/video_original')
def video_original():
    """ Serve the video feed (either webcam or video) without focus peaking """
    return Response(generate_frames(apply_focus_peaking=False), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/toggle_pause', methods=['POST'])
def toggle_pause():
    """ Toggle the pause state """
    global is_paused
    with lock:
        is_paused = not is_paused
    return jsonify({"paused": is_paused})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True, threaded=True)
