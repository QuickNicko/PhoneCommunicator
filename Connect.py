from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.widget import Widget
from kivy.graphics import Ellipse, Color
import socket
import math

# Network settings
UDP_IP = "192.168.1.100"  # Change this to your laptop's IP
UDP_PORT = 5005
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

class Joystick(Widget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.max_distance = 60

        with self.canvas:
            Color(0.8, 0, 0, 0.5)  # Outer circle color
            self.outer_circle = Ellipse(size=(120, 120))

            Color(0, 0.8, 0, 1)  # Joystick color
            self.joystick = Ellipse(size=(50, 50))

        self.bind(pos=self.update_graphics, size=self.update_graphics)

    def update_graphics(self, *args):
        self.center_x = self.parent.width / 2
        self.center_y = self.parent.height / 2
        self.joystick_x = self.center_x
        self.joystick_y = self.center_y
        self.outer_circle.pos = (self.center_x - 60, self.center_y - 60)
        self.joystick.pos = (self.joystick_x - 25, self.joystick_y - 25)

    def on_touch_move(self, touch):
        dx, dy = touch.x - self.center_x, touch.y - self.center_y
        distance = math.sqrt(dx ** 2 + dy ** 2)
        if distance > self.max_distance:
            angle = math.atan2(dy, dx)
            dx = self.max_distance * math.cos(angle)
            dy = self.max_distance * math.sin(angle)
        self.joystick_x = self.center_x + dx
        self.joystick_y = self.center_y + dy
        self.joystick.pos = (self.joystick_x - 25, self.joystick_y - 25)
        sock.sendto(f"{dx},{dy}".encode(), (UDP_IP, UDP_PORT))

    def on_touch_up(self, touch):
        self.joystick_x = self.center_x
        self.joystick_y = self.center_y
        self.joystick.pos = (self.joystick_x - 25, self.joystick_y - 25)
        sock.sendto(f"0,0".encode(), (UDP_IP, UDP_PORT))

class JoystickApp(App):
    def build(self):
        layout = FloatLayout()
        joystick = Joystick()
        layout.add_widget(joystick)
        return layout

if __name__ == "__main__":
    JoystickApp().run()
