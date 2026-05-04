# tools/serial_probe.py
# Requires: pip install pyserial requests
import serial
import time
import requests
import os

DASHBOARD_URL = os.getenv('DASHBOARD_URL', 'http://localhost:3000/log')
PORT = '/dev/ttyUSB0'   # adjust to your adapter
BAUD = 115200

def post_log(msg, data=None):
    try:
        requests.post(DASHBOARD_URL, json={"type":"serial", "msg": msg, "data": data}, timeout=2)
    except Exception:
        pass

def read_loop():
    try:
        with serial.Serial(PORT, BAUD, timeout=1) as ser:
            post_log(f"Opened {PORT}@{BAUD}")
            while True:
                line = ser.readline()
                if line:
                    text = line.decode(errors='replace').strip()
                    print(text)
                    post_log("serial-line", {"line": text})
                time.sleep(0.01)
    except Exception as e:
        post_log("serial-error", {"error": str(e)})
        print("Error:", e)

if __name__ == "__main__":
    read_loop()
