import socket
import time
from plyer import sensor

# Replace with your laptop's IP
LAPTOP_IP = "192.168.x.x"
PORT = 8888

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # UDP Socket

# Set up gyroscope sensor (plyer supports this on Android)
sensor.enable(sensor.GYROSCOPE)  # Enable gyroscope sensor

while True:
    # Get the gyroscope data
    gyro_data = sensor.gyroscope
    if gyro_data:
        x, y, z = gyro_data  # Gyroscope X, Y, Z values
        data = f"{x},{y},{z}"
        sock.sendto(data.encode(), (LAPTOP_IP, PORT))  # Send via UDP
        print("Sent:", data)  # Debugging
    time.sleep(0.1)
