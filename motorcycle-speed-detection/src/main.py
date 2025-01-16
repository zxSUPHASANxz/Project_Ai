# FILE: motorcycle-speed-detection/motorcycle-speed-detection/src/main.py

import cv2
from detection.detector import SpeedDetector
from tracking.tracker import Tracker
from utils.video_utils import load_video, save_output

def main(video_path):
    # Initialize the speed detector and tracker
    speed_detector = SpeedDetector()
    tracker = Tracker()

    # Load the video
    video_capture = load_video(video_path)
    output_frames = []

    while video_capture.isOpened():
        ret, frame = video_capture.read()
        if not ret:
            break

        # Preprocess the frame
        processed_frame = speed_detector.preprocess_frame(frame)

        # Detect motorcycles and calculate speed
        motorcycles = speed_detector.detect_motorcycles(processed_frame)
        speeds = speed_detector.calculate_speed(motorcycles)

        # Track the detected motorcycles
        tracker.track_objects(motorcycles)

        # Draw the results on the frame
        for motorcycle, speed in zip(motorcycles, speeds):
            # Draw bounding box and speed on the frame
            cv2.rectangle(frame, motorcycle['bbox'], (0, 255, 0), 2)
            cv2.putText(frame, f'Speed: {speed:.2f} km/h', (motorcycle['bbox'][0], motorcycle['bbox'][1] - 10), 
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

        output_frames.append(frame)

    # Save the output video
    save_output(output_frames, 'output_video.avi')

    # Release the video capture object
    video_capture.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    video_path = 'data/raw/cctv_footage.mp4'  # Path to the raw video footage
    main(video_path)