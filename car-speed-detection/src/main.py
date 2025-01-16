output_frames = []

    # Process each frame
    while video_capture.isOpened():
        ret, frame = video_capture.read()
        if not ret:
            break

        # Detect vehicles and calculate speed
        vehicles = detector.detect_vehicles(frame)
        for vehicle in vehicles:
            speed = detector.calculate_speed(vehicle)
            # Draw bounding box and speed on the frame
            cv2.rectangle(frame, (vehicle.x, vehicle.y), (vehicle.x + vehicle.width, vehicle.y + vehicle.height), (0, 255, 0), 2)
            cv2.putText(frame, f'Speed: {speed:.2f} km/h', (vehicle.x, vehicle.y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

        output_frames.append(frame)

    # Save the output video
    save_output(output_frames, 'output_video.avi')

    # Release the video capture object
    video_capture.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    video_path = 'data/raw/cctv_footage.mp4'  # Path to the raw video footage
    main(video_path)