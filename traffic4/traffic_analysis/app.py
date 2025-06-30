from flask import Flask, render_template, request, jsonify
import mysql.connector
import pandas as pd
from datetime import datetime

app = Flask(__name__)

# Database connection details
db_config = {
    'user': 'root',
    'password': '',
    'host': 'localhost',
    'database': 'traffic_vehicle_count'
}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/data', methods=['GET'])
def get_data():
    lane = request.args.get('lane')
    db_connection = mysql.connector.connect(**db_config)
    cursor = db_connection.cursor()

    if lane:
        cursor.execute("SELECT * FROM `vehicle count` WHERE lane_number = %s", (lane,))
    else:
        cursor.execute("SELECT * FROM `vehicle count`")

    data = cursor.fetchall()
    cursor.close()
    db_connection.close()

    df = pd.DataFrame(data, columns=['id', 'lane_number', 'date', 'time', 'total_count', 'car_count', 'truck_count', 'bus_count', 'motorcycle_count'])
    df['date'] = pd.to_datetime(df['date'])
    timestamps = df['date'].dt.strftime('%Y-%m-%d %H:%M:%S').tolist()
    counts = df['total_count'].tolist()

    return jsonify({'timestamps': timestamps, 'counts': counts})

@app.route('/predict', methods=['POST'])
def predict():
    selected_date = request.form['date']
    selected_date = pd.to_datetime(selected_date)

    db_connection = mysql.connector.connect(**db_config)
    cursor = db_connection.cursor()
    cursor.execute("SELECT * FROM `vehicle count` WHERE date = %s", (selected_date.date(),))
    data = cursor.fetchall()
    cursor.close()
    db_connection.close()

    df = pd.DataFrame(data, columns=['id', 'lane_number', 'date', 'time', 'total_count', 'car_count', 'truck_count', 'bus_count', 'motorcycle_count'])
    df['date'] = pd.to_datetime(df['date'])
    timestamps = df['date'].dt.strftime('%Y-%m-%d %H:%M:%S').tolist()
    counts = df['total_count'].tolist()

    return render_template('index.html', timestamps=timestamps, counts=counts)

if __name__ == '__main__':
    app.run(debug=True)
