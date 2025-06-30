
import cv2
import pandas as pd
from ultralytics import YOLO
import os
import time
from datetime import datetime

# Load YOLOv8 model
model = YOLO('yolov8n.pt')

# List of input video files
video_files = ['lane1.mp4', 'lane2.mp4', 'lane3.mp4', 'lane4.mp4']

# Define the output CSV file path
output_csv_path = r'C:\Users\solai prakash\Music\traffic4\vehicle_counts.csv'

# Ensure the output directory exists
if not os.path.exists(os.path.dirname(output_csv_path)):
    os.makedirs(os.path.dirname(output_csv_path))

# Initialize vehicle counters
total_counts = {'car': 0, 'truck': 0, 'bus': 0, 'motorcycle': 0}
video_counts = [{'car': 0, 'truck': 0, 'bus': 0, 'motorcycle': 0} for _ in video_files]

# Process each video
current_video_index = 0
last_update_time = time.time()  # Track the last update time
video_duration = 20  # Duration to process each video in seconds

while True:
    video_file = video_files[current_video_index]
    cap = cv2.VideoCapture(video_file)
    vehicle_counts = {'car': 0, 'truck': 0, 'bus': 0, 'motorcycle': 0}
    start_time = time.time()

    while True:
        ret, frame = cap.read()
        if not ret:
            print(f"End of video: {video_file}")
            break

        # Detect objects
        results = model(frame)

        # Count vehicles
        for result in results:
            for *box, conf, cls in result.boxes.data:
                vehicle_type = model.names[int(cls)]
                if vehicle_type in vehicle_counts:
                    vehicle_counts[vehicle_type] += 1
                    total_counts[vehicle_type] += 1
                    video_counts[current_video_index][vehicle_type] += 1
                    
                    # Draw bounding box and label on the frame
                    x1, y1, x2, y2 = map(int, box)
                    cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                    cv2.putText(frame, vehicle_type, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

        # Display the current frame
        cv2.imshow('Vehicle Detection', frame)

        # Check if 20 seconds have passed
        if time.time() - last_update_time >= video_duration:
            # Save the counts to the CSV file
            try:
                # Get the current date and time
                now = datetime.now()
                current_date = now.strftime('%Y-%m-%d')
                current_time_str = now.strftime('%H:%M:%S')
                
                data_to_save = {
                    'Video Name': video_file,
                    'Date': current_date,
                    'Time': current_time_str,
                    'Total Count': sum(vehicle_counts.values()),
                    'Car Count': vehicle_counts['car'],
                    'Truck Count': vehicle_counts['truck'],
                    'Bus Count': vehicle_counts['bus'],
                    'Motorcycle Count': vehicle_counts['motorcycle'],
                }
                df = pd.DataFrame([data_to_save])
                df.to_csv(output_csv_path, mode='a', header=not os.path.exists(output_csv_path), index=False)
                print(f"Data saved at {current_date} {current_time_str} for {video_file}")  # Print statement to indicate data saving
            except PermissionError:
                print(f"Permission denied for writing to {output_csv_path}. Trying a different path.")
                fallback_csv_path = 'C:/Users/solai prakash/Music/vehicle_counts_fallback.csv'
                df.to_csv(fallback_csv_path, mode='a', header=not os.path.exists(fallback_csv_path), index=False)

            # Update the last update time
            last_update_time = time.time()

        # Break the loop if 'q' is pressed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            cap.release()
            cv2.destroyAllWindows()
            exit()  # Exit the program

    cap.release()

    # Switch to the next video
    current_video_index = (current_video_index + 1) % len(video_files)
    print(f"Switching to next video: {video_files[current_video_index]}")

# Print insights
print("Total Vehicle Counts:")
for vehicle_type, count in total_counts.items():
    print(f"{vehicle_type.capitalize()}: {count}")

# Close any OpenCV windows
cv2.destroyAllWindows()