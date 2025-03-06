import socket
import time
from sensor import Gyroscope

# Replace with your laptop's IP address
LAPTOP_IP = "192.168.x.x"  # Find it using `ipconfig` or `ifconfig`
PORT = 8888  # UDP Port (same as on the receiver)

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # UDP Socket

gyro = Gyroscope()

while True:
    x, y, z = gyro.read()  # Read gyroscope data
    data = f"{x},{y},{z}"
    
    sock.sendto(data.encode(), (LAPTOP_IP, PORT))  # Send over UDP
    time.sleep(0.1)  # Send every 100ms
