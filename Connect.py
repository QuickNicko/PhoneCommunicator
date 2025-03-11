import pygame
import socket
import math
import time

# Initialize pygame
pygame.init()

# Screen settings
WIDTH, HEIGHT = 400, 400
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Virtual Joystick")

# Joystick settings
JOYSTICK_RADIUS = 50
CENTER = (WIDTH // 2, HEIGHT // 2)
MAX_DISTANCE = 60  # Limit joystick movement range

# Network settings
UDP_IP = "192.168.1.100"  # Change this to your laptop's IP
UDP_PORT = 5005
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

running = True
joystick_pos = CENTER

while running:
    screen.fill((30, 30, 30))  # Background color
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN or event.type == pygame.MOUSEMOTION:
            if pygame.mouse.get_pressed()[0]:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                dx, dy = mouse_x - CENTER[0], mouse_y - CENTER[1]
                distance = math.sqrt(dx ** 2 + dy ** 2)
                if distance > MAX_DISTANCE:
                    angle = math.atan2(dy, dx)
                    dx = MAX_DISTANCE * math.cos(angle)
                    dy = MAX_DISTANCE * math.sin(angle)
                joystick_pos = (int(CENTER[0] + dx), int(CENTER[1] + dy))
        elif event.type == pygame.MOUSEBUTTONUP:
            joystick_pos = CENTER
    
    # Draw joystick
    pygame.draw.circle(screen, (200, 0, 0), CENTER, MAX_DISTANCE)  # Outer boundary
    pygame.draw.circle(screen, (0, 200, 0), joystick_pos, JOYSTICK_RADIUS)  # Inner joystick
    
    # Send joystick data

    x, y = joystick_pos[0] - CENTER[0], joystick_pos[1] - CENTER[1]
    sock.sendto(f"{x},{y}".encode(), (UDP_IP, UDP_PORT))
    print(x, y)
    time.sleep(0.01)
    
    pygame.display.flip()
    
pygame.quit()
