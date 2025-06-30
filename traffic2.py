import cv2
import pandas as pd
from ultralytics import YOLO
import os
import time
from datetime import datetime
import mysql.connector

# Load YOLOv8 model
model = YOLO('yolov8n.pt')

# List of input video files
video_files = ['lane1.mp4', 'lane2.mp4', 'lane3.mp4', 'lane4.mp4']
lane_numbers = ['Lane 1', 'Lane 2', 'Lane 3', 'Lane 4']  # Corresponding lane numbers

# Database connection details
db_config = {
    'user': 'root',
    'password': '',
    'host': 'localhost',
    'database': 'traffic_vehicle_count'
}

# Initialize vehicle counters
total_counts = {'car': 0, 'truck': 0, 'bus': 0, 'motorcycle': 0}
video_counts = [{'car': 0, 'truck': 0, 'bus': 0, 'motorcycle': 0} for _ in video_files]

# Connect to the MySQL database
try:
    db_connection = mysql.connector.connect(**db_config)
    cursor = db_connection.cursor()
    print("Connected to the database successfully.")
except mysql.connector.Error as err:
    print(f"Error: {err}")
    exit()

# Process each video
current_video_index = 0
last_update_time = time.time()  # Track the last update time
video_duration = 10  # Duration to process each video in seconds

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

        # Check if 10 seconds have passed for database update
        if time.time() - last_update_time >= 10:
            # Save the counts to the MySQL database
            try:
                # Get the current date and time
                now = datetime.now()
                current_date = now.strftime('%Y-%m-%d')
                current_time_str = now.strftime('%H:%M:%S')
                
                # Prepare the SQL insert statement
                insert_query = """
                INSERT INTO `vehicle count` (lane_number, date, time, total_count, car_count, truck_count, bus_count, motorcycle_count)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                """
                data_to_save = (
                    lane_numbers[current_video_index],  # Lane number
                    current_date,
                    current_time_str,
                    sum(vehicle_counts.values()),
                    vehicle_counts['car'],
                    vehicle_counts['truck'],
                    vehicle_counts['bus'],
                    vehicle_counts['motorcycle']
                )
                
                # Execute the insert query
                cursor.execute(insert_query, data_to_save)
                db_connection.commit()  # Commit the transaction
                
                # Print confirmation message
                print(f"Data updated in DB at {current_date} {current_time_str} for {lane_numbers[current_video_index]}: {data_to_save}")
            except mysql.connector.Error as err:
                print(f"Error: {err}")

            # Reset vehicle counts for the next interval
            vehicle_counts = {'car': 0, 'truck': 0, 'bus': 0, 'motorcycle': 0}
            last_update_time = time.time()  # Update the last update time

        # Break the loop if 'q' is pressed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            cap.release()
            cv2.destroyAllWindows()
            cursor.close()
            db_connection.close()
            exit()  # Exit the program

        # Check if 10 seconds have passed for video switching
        if time.time() - start_time >= video_duration:
            break  # Switch to the next video

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