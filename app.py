from flask import Flask, render_template, jsonify
import requests
import time
from threading import Thread, Lock
from collections import deque
from statistics import mean, median
import json
import logging
import os
from requests.exceptions import Timeout
import yaml  # Add this import to handle YAML configurations

app = Flask(__name__)

# Configure logging
logging.basicConfig(level=logging.INFO)

# Load API configurations from an external YAML file
with open('api_config.yaml', 'r') as f:
    api_configs = yaml.safe_load(f)

# Initialize monitoring data for each API, limiting to 100 elements
monitoring_data = {api_name: deque(maxlen=100) for api_name in api_configs.keys()}
# Store error data (up to 50 entries)
error_data = deque(maxlen=50)

# Flag to ensure the monitor thread is started only once
thread_started = False
thread_lock = Lock()

def make_request(api_name):
    config = api_configs[api_name]
    method = config.get('method', 'GET').upper()
    endpoint = config['endpoint']
    headers = config.get('headers', {})
    params = config.get('params', {})
    data = config.get('data', {})
    timeout = config.get('timeout', 60)

    try:
        if method == 'GET':
            response = requests.get(endpoint, headers=headers, params=params, timeout=timeout)
        elif method == 'POST':
            response = requests.post(endpoint, headers=headers, json=data, params=params, timeout=timeout)
        else:
            raise ValueError(f"Unsupported HTTP method: {method}")
        response.raise_for_status()
        
        # Try to parse JSON, but handle cases where the response is not JSON
        try:
            return response.json()
        except ValueError:
            # If it's not JSON, return the text content
            return {"text_content": response.text}
    except Exception as e:
        raise e

def monitor_api(interval=60):
    logging.info("Monitoring thread started.")
    while True:
        for api_name in monitoring_data.keys():
            result = {}
            start_time = time.time()
            try:
                response = make_request(api_name)
                result['status'] = 'Success'
                result['response'] = response
                logging.info(f"API {api_name} succeeded.")
            except Exception as e:
                result['status'] = 'Error'
                result['error'] = str(e)
                # Add error to error_data queue
                error_data.appendleft({
                    'timestamp': time.strftime('%Y-%m-%d %H:%M:%S'),
                    'api': api_name,
                    'error': str(e)
                })
                logging.error(f"API {api_name} failed with error: {e}")
            end_time = time.time()
            result['response_time'] = round(end_time - start_time, 4)
            result['timestamp'] = time.strftime('%Y-%m-%d %H:%M:%S')
            result['api'] = api_name
            monitoring_data[api_name].appendleft(result)
        # Wait for the specified interval before the next check
        time.sleep(interval)

def start_monitoring_thread():
    logging.info("Starting monitoring thread.")
    global thread_started
    with thread_lock:
        if not thread_started:
            monitor_thread = Thread(target=monitor_api, args=(60,))
            monitor_thread.daemon = True
            monitor_thread.start()
            thread_started = True
            logging.info("Monitoring thread started.")

@app.route('/')
def index():
    avg_response_times = {}
    overall_uptime = 100.0
    overall_response_times = []
    overall_errors = 0
    overall_error_rate = 0
    overall_avg_response_time = 0
    total_calls = 0

    for api_name, data in monitoring_data.items():
        if data:
            recent_data = list(data)  # Convert deque to list
            avg_response_times[api_name] = round(mean(item['response_time'] for item in recent_data), 2)
            overall_response_times.extend([item['response_time'] for item in recent_data])
            overall_errors += sum(1 for item in recent_data if item['status'] == 'Error')
            total_calls += len(recent_data)
        else:
            avg_response_times[api_name] = 0.0

    if total_calls > 0:
        overall_uptime = round(100 - (overall_errors / total_calls * 100), 2)
        overall_error_rate = round((overall_errors / total_calls * 100), 2)
        overall_avg_response_time = round(mean(overall_response_times), 2) if overall_response_times else 0
    overall_status = {
        'uptime': overall_uptime,
        'avg_response_time': overall_avg_response_time,
        'error_rate': overall_error_rate
    }

    sorted_data = {api_name: sorted(list(data), key=lambda x: x['timestamp'], reverse=True) 
                   for api_name, data in monitoring_data.items()}
    sorted_errors = sorted(list(error_data), key=lambda x: x['timestamp'], reverse=True)

    return render_template('index.html', 
                           data=sorted_data, 
                           errors=sorted_errors,
                           avg_response_times=avg_response_times,
                           apis=json.dumps(list(monitoring_data.keys())),
                           overall_status=overall_status)

@app.route('/chart_data')
def chart_data():
    chart_data = {}
    for api_name, data in monitoring_data.items():
        recent_data = sorted(list(data), key=lambda x: x['timestamp'])  # Convert deque to list and sort by timestamp, oldest first
        response_times = [item['response_time'] for item in recent_data]
        timestamps = [item['timestamp'] for item in recent_data]
        
        # Calculate error rate for each timestamp
        error_rates = []
        for i in range(len(recent_data)):
            window = recent_data[max(0, i-49):i+1]  # Use a rolling window of up to 50 items
            errors = sum(1 for item in window if item['status'] == 'Error')
            error_rate = (errors / len(window)) * 100 if window else 0
            error_rates.append(round(error_rate, 2))

        chart_data[api_name] = {
            'response_times': response_times,
            'timestamps': timestamps,
            'error_rates': error_rates
        }
    
    return jsonify(chart_data)

@app.route('/model_data/<model>')
def model_data(model):
    if model in monitoring_data:
        # Convert deque to list before jsonifying
        return jsonify(list(monitoring_data[model]))
    else:
        return jsonify({"error": "Model not found"}), 404

# Start the monitoring thread when the app starts
start_monitoring_thread()

if __name__ == '__main__':
    logging.info("Monitoring thread started in main block.")
    logging.info("Starting Flask app.")
    app.run(port=5001)