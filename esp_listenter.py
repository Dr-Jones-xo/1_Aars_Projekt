import sqlite3
import paho.mqtt.client as mqtt
from datetime import datetime

BROKER = "localhost"
PORT = 1883
USERNAME = "hamsa"
PASSWORD = "12345678"
TOPIC = "sensor/dht11"

def on_connect(client, userdata, flags, rc):
    print("Forbundet til broker med kode:", rc)
    client.subscribe(TOPIC)

def on_message(client, userdata, msg):
    data = msg.payload.decode()
    print(f"[MQTT] {msg.topic}: {data}")

    try:
        temp, hum = map(float, data.split(","))
        now = datetime.now().strftime("%d/%m/%y %H:%M:%S")
        conn = sqlite3.connect("database/Temp.db")
        cur = conn.cursor()
        cur.execute("INSERT INTO TOF (Temp, Hum, Dato) VALUES (?, ?, ?)", (temp, hum, now))
        conn.commit()
        conn.close()
    except Exception as e:
        print("Fejl ved indsættelse i database:", e)

client = mqtt.Client()
client.username_pw_set(USERNAME, PASSWORD)
client.on_connect = on_connect
client.on_message = on_message

client.connect(BROKER, PORT, 60)

print(f"Lytter på '{TOPIC}'...")
client.loop_forever()
