def load_video(video_path):
    import cv2
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        raise ValueError("Error opening video file")
    return cap

def save_output(output_path, frame):
    import cv2
    cv2.imwrite(output_path, frame)

def preprocess_frame(frame):
    import cv2
    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    resized_frame = cv2.resize(gray_frame, (640, 480))
    return resized_frame