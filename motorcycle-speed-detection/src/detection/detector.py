class SpeedDetector:
    def __init__(self, frame_rate, distance_per_pixel):
        self.frame_rate = frame_rate
        self.distance_per_pixel = distance_per_pixel

    def detect_motorcycles(self, frame):
        # Implement motorcycle detection logic here
        # This should return a list of detected motorcycles with their bounding boxes
        pass

    def calculate_speed(self, bounding_box, time_elapsed):
        # Calculate the speed of the detected motorcycle
        # bounding_box: (x1, y1, x2, y2)
        # time_elapsed: time in seconds since the last frame
        distance_moved = (bounding_box[2] - bounding_box[0]) * self.distance_per_pixel
        speed = distance_moved / time_elapsed  # speed in meters per second
        return speed