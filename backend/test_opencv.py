import cv2

VIDEO_PATH = "/mnt/d/focus-peaking-project/exploreHD-Focus.mp4"

cap = cv2.VideoCapture(VIDEO_PATH)

if not cap.isOpened():
    print("❌ ERROR: Cannot open video file.")
else:
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    fps = cap.get(cv2.CAP_PROP_FPS)
    duration = total_frames / fps if fps else "Unknown"

    print(f"✅ Total Frames in Video: {total_frames}")
    print(f"🎥 FPS: {fps}")
    print(f"⏳ Duration: {duration} seconds")

cap.release()
