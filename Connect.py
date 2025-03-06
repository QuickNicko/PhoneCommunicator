import socket
import time
import androidhelper  # Built-in for Pydroid 3

# Replace with your laptop's IP
LAPTOP_IP = "192.168.1.1"
PORT = 8888

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # UDP Socket
droid = androidhelper.Android()

droid.startSensingTimed(2, 50)  # Start gyroscope sensor, update every 50ms

while True:
    sensor_data = droid.sensorsGetGyroscope().result  # Read gyro
    if sensor_data:
        x, y, z = sensor_data["x"], sensor_data["y"], sensor_data["z"]
        data = f"{x},{y},{z}"
        sock.sendto(data.encode(), (LAPTOP_IP, PORT))  # Send via UDP
        print("Sent:", data)  # Debugging
    time.sleep(0.1)
