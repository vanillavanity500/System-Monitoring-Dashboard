import psutil
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import csv
from datetime import datetime
import logging
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Configure logging
LOG_FILE = 'monitoring.log'
logging.basicConfig(filename=LOG_FILE, level=logging.ERROR)

# Email configuration
EMAIL_HOST = 'smtp.example.com'
EMAIL_PORT = 587
EMAIL_USERNAME = 'your_email@example.com'
EMAIL_PASSWORD = 'your_email_password'
EMAIL_RECEIVERS = ['recipient1@example.com', 'recipient2@example.com']

# Function to send email alert
def send_email(subject, message):
    msg = MIMEMultipart()
    msg['From'] = EMAIL_USERNAME
    msg['To'] = ', '.join(EMAIL_RECEIVERS)
    msg['Subject'] = subject
    msg.attach(MIMEText(message, 'plain'))
    
    try:
        server = smtplib.SMTP(EMAIL_HOST, EMAIL_PORT)
        server.starttls()
        server.login(EMAIL_USERNAME, EMAIL_PASSWORD)
        text = msg.as_string()
        server.sendmail(EMAIL_USERNAME, EMAIL_RECEIVERS, text)
        server.quit()
        logging.info('Email alert sent successfully')
    except Exception as e:
        logging.error('Failed to send email alert: ' + str(e))

# Function to send alerts
def send_alert(message):
    print("ALERT:", message)
    logging.error("ALERT: " + message)
    send_email("System Monitoring Alert", message)

# Function to update system metrics
def update_metrics(frame):
    try:
        cpu_percent = psutil.cpu_percent()
        mem_percent = psutil.virtual_memory().percent
        disk_percent = psutil.disk_usage('/').percent
        
        # Update the plot
        ax.clear()
        ax.bar(['CPU', 'Memory', 'Disk'], [cpu_percent, mem_percent, disk_percent], color=['red', 'green', 'blue'])
        ax.set_ylim(0, 100)
        ax.set_ylabel('Usage (%)')
        ax.set_title('System Monitoring Dashboard')
        
        # Write data to CSV
        with open('system_metrics.csv', 'a', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow([datetime.now(), cpu_percent, mem_percent, disk_percent])
        
        # Check for alerts
        if cpu_percent > 80:
            send_alert("High CPU Usage!")
        if mem_percent > 80:
            send_alert("High Memory Usage!")
        if disk_percent > 80:
            send_alert("High Disk Usage!")
    
    except Exception as e:
        logging.error(str(e))

# Create a figure and axis
fig, ax = plt.subplots()

# Start updating metrics every second
ani = FuncAnimation(fig, update_metrics, interval=1000)

# Show the plot
plt.show()

