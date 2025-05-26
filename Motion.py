import serial
import time
import requests

motion_url = "http://127.0.0.1:7999/1/config/set"

motion_timeout = 5  # seconds to keep recording after motion
last_motion_time = 0
recording = False

# Change this to your Arduino port (e.g., 'COM3' on Windows)
ser = serial.Serial('/dev/ttyACM0', 9600, timeout=1)

def start_recording():
    try:
        requests.get(f"{motion_url}?emulate_motion=1")
        print("Started recording")
    except Exception as e:
        print("Failed to start recording:", e)

def stop_recording():
    try:
        requests.get(f"{motion_url}?emulate_motion=0")
        print("Stopped recording")
    except Exception as e:
        print("Failed to stop recording:", e)

while True:
    if ser.in_waiting:
        line = ser.readline().decode().strip()
        print("Arduino:", line)
        if "DETECTED" in line:
            last_motion_time = time.time()
            if not recording:
                start_recording()
                recording = True

    if recording and (time.time() - last_motion_time > motion_timeout):
        stop_recording()
        recording = False

    time.sleep(0.1)
