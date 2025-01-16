class Detector:
    def __init__(self, frame_rate, distance_per_pixel):
        self.frame_rate = frame_rate
        self.distance_per_pixel = distance_per_pixel

    def detect_vehicles(self, frame):
        # Implement vehicle detection logic here
        # This could use a pre-trained model or a simple color/shape detection
        detected_vehicles = []  # Placeholder for detected vehicles
        return detected_vehicles

    def calculate_speed(self, vehicle, time_elapsed):
        # Calculate speed in km/h
        distance = vehicle['width'] * self.distance_per_pixel  # Example calculation
        speed = (distance / time_elapsed) * 3.6  # Convert m/s to km/h
        return speed

    def process_frame(self, frame):
        vehicles = self.detect_vehicles(frame)
        speeds = []
        for vehicle in vehicles:
            # Assuming vehicle has a timestamp for when it was detected
            time_elapsed = 1 / self.frame_rate  # Time between frames
            speed = self.calculate_speed(vehicle, time_elapsed)
            speeds.append(speed)
        return speeds