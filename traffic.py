import cv2
import pandas as pd
from ultralytics import YOLO
import os
import time
import matplotlib.pyplot as plt

# Load YOLOv8 model
model = YOLO('yolov8n.pt')

# Initialize lists to store counts
video_data = []

# List of input video files
video_files = ['lane1.mp4', 'lane2.mp4', 'lane3.mp4', 'lane4.mp4']

# Initialize vehicle counters
total_counts = {'car': 0, 'truck': 0, 'bus': 0, 'motorcycle': 0}

# Define the output CSV file path
output_csv_path = 'D:/Ai based traffic/traffic4/vehicle_counts.csv'

# Set up the plot for real-time visualization
plt.ion()  # Turn on interactive mode
fig, ax = plt.subplots(figsize=(10, 6))
bars = ax.bar(total_counts.keys(), total_counts.values(), color=['blue', 'orange', 'green', 'red'])
ax.set_title('Real-Time Vehicle Counts')
ax.set_xlabel('Vehicle Type')
ax.set_ylabel('Count')
ax.set_ylim(0, 100)  # Set a fixed limit for better visualization; adjust as necessary
plt.xticks(rotation=45)
plt.grid(axis='y')

# Process each video
for video_file in video_files:
    cap = cv2.VideoCapture(video_file)
    vehicle_counts = {'car': 0, 'truck': 0, 'bus': 0, 'motorcycle': 0}
    start_time = time.time()
    last_update_time = time.time()  # Track the last update time

    # Create an empty DataFrame for the current video
    video_df = pd.DataFrame(columns=['Video Name', 'Timestamp', 'Total Count', 'Car Count', 'Truck Count', 'Bus Count', 'Motorcycle Count', 'Vehicle Types', 'Average Speed', 'Direction'])

    while True:
        ret, frame = cap.read()
        if not ret:
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

        # Get current timestamp
        current_time = time.time() - start_time
        total_count = sum(vehicle_counts.values())
        vehicle_types = ', '.join([vt for vt in vehicle_counts.keys() if vehicle_counts[vt] > 0])
        # Create a new DataFrame row
        new_data = pd.DataFrame([{
            'Video Name': video_file,
            'Timestamp': round(current_time, 2),
            'Total Count': total_count,
            'Car Count': vehicle_counts['car'],
            'Truck Count': vehicle_counts['truck'],
            'Bus Count': vehicle_counts['bus'],
            'Motorcycle Count': vehicle_counts['motorcycle'],
            'Vehicle Types': vehicle_types,
            'Average Speed': None,  # Placeholder for speed if implemented
            'Direction': None        # Placeholder for direction if implemented
        }])

        # Concatenate the new data to the existing DataFrame
        video_df = pd.concat([video_df, new_data], ignore_index=True)

        # Check if 20 seconds have passed
        if time.time() - last_update_time >= 20:
            # Save the DataFrame to a CSV file
            try:


                video_df.to_csv(output_csv_path, mode='a', header=not os.path.exists(output_csv_path), index=False)
            except PermissionError:
                print(f"Permission denied for writing to {output_csv_path}. Trying a different path.")
                # Fallback path for the CSV file
                fallback_csv_path = 'D:/vehicle_counts_fallback.csv'
                video_df.to_csv(fallback_csv_path, mode='a', header=not os.path.exists(fallback_csv_path), index=False)

            # Reset the DataFrame
            video_df = pd.DataFrame(columns=['Video Name', 'Timestamp', 'Total Count', 'Car Count', 'Truck Count', 'Bus Count', 'Motorcycle Count', 'Vehicle Types', 'Average Speed', 'Direction'])

            # Update the last update time
            last_update_time = time.time()

        # Update the bar chart in real-time
        for i, bar in enumerate(bars):
            bar.set_height(total_counts[list(total_counts.keys())[i]])
        plt.pause(0.01)  # Pause to allow the plot to update

    # Save any remaining data in the DataFrame
    try:
        video_df.to_csv(output_csv_path, mode='a', header=False, index=False)
    except PermissionError:
        print(f"Permission denied for writing to {output_csv_path}. Trying a different path.")
        fallback_csv_path = 'D:/vehicle_counts_fallback.csv'
        video_df.to_csv(fallback_csv_path, mode='a', header=False, index=False)

    cap.release()

# Print insights
print("Total Vehicle Counts:")
for vehicle_type, count in total_counts.items():
    print(f"{vehicle_type.capitalize()}: {count}")

print("\nData saved to 'vehicle_counts.csv' or fallback file.")

# Show the final plot
plt.ioff()  # Turn off interactive mode
plt.show()