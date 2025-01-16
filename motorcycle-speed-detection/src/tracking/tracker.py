class Tracker:
    def __init__(self):
        self.tracks = {}

    def track_objects(self, detections):
        for detection in detections:
            object_id = detection['id']
            if object_id not in self.tracks:
                self.tracks[object_id] = detection
            else:
                self.update_tracks(object_id, detection)

    def update_tracks(self, object_id, detection):
        self.tracks[object_id]['position'] = detection['position']
        self.tracks[object_id]['timestamp'] = detection['timestamp']