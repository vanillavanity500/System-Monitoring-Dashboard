from flask import Flask, render_template, jsonify
import psutil
import plotly.graph_objs as go
import plotly.io as pio

app = Flask(__name__)

def get_system_metrics():
    cpu_percent = psutil.cpu_percent()
    mem_percent = psutil.virtual_memory().percent
    disk_percent = psutil.disk_usage('/').percent
    return {'cpu': cpu_percent, 'memory': mem_percent, 'disk': disk_percent}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/metrics')
def metrics():
    data = get_system_metrics()
    return jsonify(data)

if __name__ == '__main__':
    app.run(debug=True)
