def load_video(video_path):
    import cv2
    video_capture = cv2.VideoCapture(video_path)
    return video_capture

def save_output(frames, output_path):
    if not frames:
        return
    
    height, width, _ = frames[0].shape
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    out = cv2.VideoWriter(output_path, fourcc, 30.0, (width, height))

    for frame in frames:
        out.write(frame)

    out.release()