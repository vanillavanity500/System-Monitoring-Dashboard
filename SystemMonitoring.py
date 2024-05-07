import psutil
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

# Update system metrics
def update_metrics(frame):
    cpu_percent = psutil.cpu_percent()
    mem_percent = psutil.virtual_memory().percent
    disk_percent = psutil.disk_usage('/').percent
    
    # Update the plot
    ax.clear()
    ax.bar(['CPU', 'Memory', 'Disk'], [cpu_percent, mem_percent, disk_percent], color=['red', 'green', 'blue'])
    ax.set_ylim(0, 100)
    ax.set_ylabel('Usage (%)')
    ax.set_title('System Monitoring Dashboard')

# Create a figure and axis
fig, ax = plt.subplots()

# Start updating metrics every second
ani = FuncAnimation(fig, update_metrics, interval=1000)

# Show the plot
plt.show()
