# 🚀 API Monitoring Dashboard

Real-time API health and performance monitoring, powered by Flask.

![Dashboard Preview](path/to/dashboard_preview.gif)

## 📋 Table of Contents

- [✨ Features](#-features)
- [🛠 Prerequisites](#-prerequisites)
- [🚀 Quick Start](#-quick-start)
- [⚙️ Configuration](#️-configuration)
- [🖥 Running the Application](#-running-the-application)
- [🌐 Accessing the Dashboard](#-accessing-the-dashboard)
- [📊 Usage](#-usage)
- [🎨 Customization](#-customization)
- [📝 Logging](#-logging)
- [🚀 Deployment](#-deployment)
- [🤝 Contributing](#-contributing)
- [📄 License](#-license)

## ✨ Features

- 🔄 **Real-time Monitoring**: Periodic API health checks
- 📊 **Dashboard Visualization**: Live status, response times, and error rates
- 🚨 **Error Tracking**: Detailed error logging and display
- 📈 **Interactive Charts**: Visual insights into API performance
- 🔍 **Modal Details**: In-depth information on individual API calls

## 🛠 Prerequisites

- Python 3.6+
- pip (Python package installer)
- Virtual Environment (recommended)

## 🚀 Quick Start

1. **Clone the repo**
   ```bash
   git clone https://github.com/yourusername/api-monitoring-dashboard.git
   cd api-monitoring-dashboard
   ```

2. **Set up virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure APIs** (see [Configuration](#️-configuration) section)

5. **Run the app**
   ```bash
   python app.py
   ```

6. **View the dashboard**
   Open `http://localhost:5001` in your browser

## ⚙️ Configuration

### API Configuration (api_config.yaml)

Create an `api_config.yaml` file in the project root:

Install Dependencies
txt
Configuration
1. API Configuration
The application uses an api_config.yaml file to define the APIs to monitor. Update this file to configure your APIs.
30
API Naming: Each API configuration starts with a unique identifier (e.g., ExampleAPI).
Method: HTTP method to use (GET, POST, etc.).
Endpoint: The URL of the API endpoint.
Headers: Any headers required for the API call. Replace "your_api_key_here" with your actual API key or token.
Params: Query parameters for GET requests.
Data: JSON payload for POST requests.
Timeout: Maximum time (in seconds) to wait for a response.
> Important: Ensure you replace any placeholder values (like API keys) with your actual credentials. Keep your API keys secure and never commit them to version control.
2. Secure Your API Keys
It's crucial to avoid hardcoding sensitive information like API keys. Consider using environment variables or a separate configuration file that's excluded from version control.
Using Environment Variables:
Update your api_config.yaml:
"
Before running the application, set the environment variable:
'
Using a .env File:
Create a .env file:
your_actual_api_key
Use a package like python-dotenv to load the .env file.
Running the Application
1. Start the Flask Application
By default, the Flask app runs on port 5001.
py
2. Using Gunicorn (Recommended for Production)
5001
Parameters:
app:app refers to the app object in the app.py file.
-b 0.0.0.0:5001 binds the application to all network interfaces on port 5001.
Accessing the Dashboard
Open your web browser and navigate to:
/
You should see the API Monitoring Dashboard displaying the status of your configured APIs.
Usage
API Cards: Each API has a card displaying its current status, average response time, and the time of the last check.
Modals for Details: Click on an API card to view detailed information about recent calls and errors.
Charts:
Response Time History: Visualizes the response times of APIs over time.
Error Rate History: Displays the error rates. This chart only appears if there are errors.
Overall Status: Shows aggregated uptime, average response time, and error rate across all APIs.
Customization
1. Adjust Monitoring Interval
By default, the application checks the APIs every 60 seconds. To change this:
Open app.py.
Locate the line starting the monitoring thread:
)
Change 60 to your desired interval in seconds.
2. Modify APIs
Add a New API: Append a new configuration to api_config.yaml following the existing structure.
Remove an API: Delete the API configuration from api_config.yaml.
Update an API: Modify the parameters in api_config.yaml as needed.
3. Update the Dashboard Appearance
The front-end is located in templates/index.html. You can modify the HTML and CSS to change the appearance or add new features.
Logging
Logging is configured using Python's built-in logging module.
Log Level: Set to INFO by default.
Log Output: Outputs to the console.
Modify Log Level: In app.py, change the following line:
)
Example to set it to DEBUG:
)
Log Messages: Includes information about API success or failure and any exceptions encountered.
Deployment
1. Production Considerations
Web Server: Use a production-ready web server like Gunicorn or uWSGI.
Reverse Proxy: Consider using Nginx or Apache as a reverse proxy for better performance and security.
SSL/TLS: Secure your application with HTTPS.
2. Using Gunicorn and Nginx
Gunicorn: Already covered in Running the Application.
Nginx Configuration: Sample Nginx configuration:
}
3. Process Management
Use a process manager like supervisord or systemd to ensure your application runs continuously.
Contributing
Contributions are welcome! Please open an issue or submit a pull request on GitHub.
License
This project is licensed under the MIT License.
---
Note: Replace placeholders like yourusername, your_api_key_here, and your_domain.com with your actual details.