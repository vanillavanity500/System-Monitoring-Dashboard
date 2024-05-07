import psutil
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import csv
from datetime import datetime
import logging

# Configure logging
logging.basicConfig(filename='monitoring.log', level=logging.ERROR)

# Function to send alerts
def send_alert(message):
    print("ALERT:", message)
    logging.error("ALERT: " + message)

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

