class Tracker:
    def __init__(self):
        self.tracks = {}

    def track_vehicles(self, detections, frame_id):
        for detection in detections:
            vehicle_id = detection['id']
            if vehicle_id not in self.tracks:
                self.tracks[vehicle_id] = {'positions': [], 'last_frame': frame_id}
            self.tracks[vehicle_id]['positions'].append(detection['position'])
            self.tracks[vehicle_id]['last_frame'] = frame_id

    def update_tracks(self, frame_id):
        for vehicle_id in list(self.tracks.keys()):
            if self.tracks[vehicle_id]['last_frame'] < frame_id - 1:
                del self.tracks[vehicle_id]