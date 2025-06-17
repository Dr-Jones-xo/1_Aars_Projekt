import network
import time
from machine import Pin
import dht
from umqtt.simple import MQTTClient
import machine
from neopixel import NeoPixel


ssid = 'IT-TEKNOLOG-2'
password = 'KeaTeknolog6!'

mqtt_server = '192.168.0.3'
mqtt_user = 'hamsa'
mqtt_pass = '12345678'

client_id = 'esp32_dht'
topic_pub = b'sensor/dht11'


dht_sensor = dht.DHT11(Pin(19))
message_interval = 10

pixel_pin = Pin(12, Pin.OUT)  
num_pixels = 12
np = NeoPixel(pixel_pin, num_pixels)


def connect_wifi():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(ssid, password)
    while not wlan.isconnected():
        time.sleep(1)
    print('WiFi forbundet:', wlan.ifconfig()[0])

def connect_mqtt():
    client = MQTTClient(client_id, mqtt_server, user=mqtt_user, password=mqtt_pass)
    client.connect()
    print('Forbundet til MQTT broker:', mqtt_server)
    return client


def update_led(temp, hum):
    temp_ok = 2 <= temp <= 5
    hum_ok = 60 <= hum <= 80

    if temp_ok and hum_ok:
        color = (0, 255, 0) 
    else:
        color = (255, 0, 0) 

    for i in range(num_pixels):
        np[i] = color
    np.write()


try:
    connect_wifi()
    client = connect_mqtt()
except OSError:
    print('Fejl under opstart, genstarter...')
    time.sleep(10)
    machine.reset()


while True:
    try:
        dht_sensor.measure()
        temp = dht_sensor.temperature()
        hum = dht_sensor.humidity()

       
        update_led(temp, hum)

        msg = f"{temp}, {hum}" 
        client.publish(topic_pub, msg)
        print('Sendt:', msg)

        time.sleep(message_interval)

    except Exception as e:
        print('Fejl:', e)
        time.sleep(10)
        machine.reset()

