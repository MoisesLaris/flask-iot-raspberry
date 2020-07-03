import RPi.GPIO as GPIO
import time
import json
import random
from random import random
from flask import Flask, render_template, make_response
import Adafruit_DHT

app = Flask(__name__)
GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)

GPIO.setup(11, GPIO.OUT)
servo = GPIO.PWM(11,50)
servo.start(0)
i = 2

dht = Adafruit_DHT.DHT11

@app.route('/')
def index():

    data = { 'servo': i }
    return render_template('index.html', **data)
@app.route('/<device>/<action>')
def do(device,action):
    if device == "servo":
        actuator=servo
    global i
    if action == "mas" and i<12:
        i=i+1
        actuator.ChangeDutyCycle(i)
        time.sleep(0.3)
        actuator.ChangeDutyCycle(0)
        time.sleep(0.3)
    if action == "menos" and i>2:
        i=i-1
        actuator.ChangeDutyCycle(i)
        time.sleep(0.3)
        actuator.ChangeDutyCycle(0)
        time.sleep(0.3)
    data = { 'servo' : i  }
    return render_template('index.html', **data)

@app.route('/histogram')
def histogram():
    return render_template('histogram.html')

@app.route('/data', methods=["GET","POST"])
def data():
    humedad, temperatura = Adafruit_DHT.read_retry(dht, 23)
    data = [temperatura, humedad]
    response = make_response(json.dumps(data))
    response.content_type = 'application/json'
    return response

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
