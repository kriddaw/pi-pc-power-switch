from flask import Flask, render_template, redirect, url_for, flash, jsonify
import RPi.GPIO as GPIO
import time
import signal
import sys


app = Flask(__name__)
app.secret_key = 'th1$is$3cr3t'

# GPIO setup
relay_pin = 17
status_pin = 22
GPIO.setmode(GPIO.BCM)
GPIO.setup(relay_pin, GPIO.OUT)
GPIO.setup(status_pin, GPIO.IN)

# Cleanup GPIO if program ends
def signal_handler(sig, frame):
    print('Cleaning up GPIO...')
    GPIO.cleanup()
    sys.exit(0)

# Function to toggle the relay
def toggle_relay():
    GPIO.output(relay_pin, GPIO.HIGH)
    time.sleep(1)
    GPIO.output(relay_pin, GPIO.LOW)

# Function to check power status
def check_status():
    return GPIO.input(status_pin)

@app.route('/')
def index():
    status = check_status()
    return render_template('index.html', status=status)

@app.route('/toggle_relay', methods=['POST'])
def toggle():
    if check_status():
        flash('PC is already on')
    else:
        toggle_relay()
    return redirect(url_for('index'))

@app.route('/get_status')
def get_status():
    status = check_status()
    return jsonify(status=status)

if __name__ == '__main__':
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    app.run(host='0.0.0.0', port=5000)

