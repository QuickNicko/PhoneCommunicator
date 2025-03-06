from kivy.app import App
from kivy.uix.button import Button
from kivy.clock import Clock
from plyer import accelerometer
import socket

# UDP Setup
UAV_IP = "192.168.1.200"  # Change this to the UAV's or laptop's IP
UAV_PORT = 8888

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Global state for STOP button
sending_data = True

def send_gyro_data(dt):
    global sending_data
    if sending_data:
        try:
            data = accelerometer.acceleration  # Gyroscope data (x, y, z)
            if data:
                msg = f"{data[0]},{data[1]},{data[2]}"
                sock.sendto(msg.encode(), (UAV_IP, UAV_PORT))
        except:
            pass  # Handle sensor errors

class GyroApp(App):
    def build(self):
        global sending_data
        button = Button(text="STOP", font_size=30)
        button.bind(on_press=self.toggle_sending)
        
        # Start gyroscope data stream
        accelerometer.enable()
        Clock.schedule_interval(send_gyro_data, 0.1)  # Send data every 100ms
        
        return button

    def toggle_sending(self, instance):
        global sending_data
        sending_data = not sending_data
        instance.text = "START" if not sending_data else "STOP"

if __name__ == "__main__":
    GyroApp().run()
