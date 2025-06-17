import base64
import threading
from io import BytesIO
from matplotlib.figure import Figure
from flask import Flask, render_template
from flask_socketio import SocketIO, emit
from get_stue_dht11_data import get_TOF_data
from time import sleep


app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")


def stue_temp():

    timestamps, temp, hum = get_TOF_data(5)  
    fig = Figure() 
    ax = fig.subplots()
    fig.subplots_adjust(bottom=0.3)
    ax.tick_params(axis='x', which = 'both', rotation=30)
    ax.set_facecolor("#fff")
    ax.plot(timestamps, temp, linestyle = "dashed", c="#F11", linewidth="1.5", marker="o")  
    ax.set_xlabel("Timestamps")
    ax.set_ylabel("Temperature celsius")
    fig.patch.set_facecolor('#fff')
    ax.tick_params(axis='x', colors="black")
    ax.tick_params(axis='y', colors="blue")
    ax.spines['left'].set_color("blue")
    ax.spines['right'].set_color("blue")
    ax.spines['top'].set_color("blue")
    ax.spines['bottom'].set_color("blue")
   
    buf = BytesIO()
    fig.savefig(buf, format="png")
  
    data = base64.b64encode(buf.getbuffer()).decode("ascii")
    return data

def stue_hum():
  
    timestamps, temp, hum = get_TOF_data(5)  
    print(timestamps, temp, hum)
    fig = Figure() 
    ax = fig.subplots()
    fig.subplots_adjust(bottom=0.3)
    ax.tick_params(axis='x', which = 'both', rotation=30)
    ax.set_facecolor("#fff")
    ax.plot(timestamps, hum, linestyle = "dashed", c="#F11", linewidth="1.5", marker="o")  
    ax.set_xlabel("Timestamps")
    ax.set_ylabel("Humidity %")
    fig.patch.set_facecolor('#fff')
    ax.tick_params(axis='x', colors="black")
    ax.tick_params(axis='y', colors="blue")
    ax.spines['left'].set_color("blue")
    ax.spines['right'].set_color("blue")
    ax.spines['top'].set_color("blue")
    ax.spines['bottom'].set_color("blue")
  
    buf = BytesIO()
    fig.savefig(buf, format="png")
   
    data = base64.b64encode(buf.getbuffer()).decode("ascii")
    return data
   


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/Historik')
def Historik():
    stue_temperature = stue_temp()
    stue_humidity = stue_hum()
    return render_template('stue.html', stue_temperature=stue_temperature, stue_humidity=stue_humidity)


@app.route('/test')
def test():
    return render_template('test.html')


@socketio.on('get_data')
def handle_get_data():
    timestamps, temp, hum = get_TOF_data(1)
    print(timestamps, temp, hum)
    emit('data_update', {'temp': temp[0], 'hum': hum[0]})

@socketio.on('connect')
def test_connect():
    print('Client connected')


if __name__ == "__main__":
    socketio.run(app, host="0.0.0.0", port=5002, debug=True)
