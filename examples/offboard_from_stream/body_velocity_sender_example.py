"""
MAVSDK Offboard Control - Local Velocity Sender
=================================================

This script provides an interface for controlling a drone's velocity and yaw through keyboard inputs,
utilizing MAVSDK over UDP. It features an interactive GUI built with Pygame for real-time control and feedback,
enabling dynamic adjustment of the drone's flight parameters.

Overview:
---------
- Sends control packets to command drone movements in local body coordinates with optional yaw adjustments.
- Offers two modes of operation: 'Instant Reset' and 'Incremental Control', toggled by pressing 'M'.
- Provides a graphical interface to visualize and control the drone's movement and yaw.

Setup Requirements:
-------------------
- A MAVSDK-compatible drone or a SITL setup running and accessible on the network.
- The receiver node (`receiver.py`) must be operational to handle and execute the commands sent from this script.
- Ensure that the receiver and this sender script are configured to communicate over the specified IP and port.

Features:
---------
- **Velocity Control**: Use W, A, S, D for forward, backward, left, and right movements respectively.
- **Altitude Adjustment**: Up and Down arrow keys control vertical movement, with up increasing altitude and down decreasing it.
- **Yaw Control**: Left and Right arrow keys adjust yaw. In 'Instant Reset' mode, yaw rate returns to zero upon key release. In 'Incremental Control' mode, yaw rate persists and increments with each key press.
- **Mode Switching**: Press 'M' to toggle between 'Instant Reset' and 'Incremental Control' modes.
- **Control Enable/Disable**: 'E' to enable sending commands, 'C' to cancel and send a stop command.
- **Emergency Hold**: Press 'H' to immediately stop all movements.
- **Application Exit**: Press 'Q' to safely exit the application, ensuring all movements are halted.

Usage Instructions:
-------------------
1. Ensure your MAVSDK setup (either SITL or a real drone) is operational and that `receiver.py` is running.
2. Start this script in a Python environment where Pygame is installed. The script's GUI will display on your screen.
3. Use the keyboard controls as outlined to command the drone. Ensure you start command transmission by pressing 'E' and can stop it anytime with 'H' or 'C'.

Safety Notice:
--------------
- When operating with a real drone, ensure you are in a safe, open environment to avoid any accidents.
- Always be prepared to take manual control of the drone if necessary.

Developer:
- Alireza Ghaderi
- GitHub: alireza787b
- Date: April 2024

Dependencies:
- Pygame for GUI operations.
- MAVSDK
- PX4
- Python's `socket` library for UDP communication.
- `control_packet.py` for formatting control commands.

The code is designed to be clear and modifiable for different use cases, allowing adjustments to IP settings, control rates, and more directly within the script.
"""

import socket
import pygame
import sys
from control_packet import ControlPacket, SetpointMode

# Constants for communication and control
UDP_IP = "127.0.0.1"
UDP_PORT = 5005
SEND_RATE = 0.1  # Packet send rate in seconds (10 Hz)
DEFAULT_SPEED = 1.0  # meters per second
YAW_RATE_STEP = 5.0  # degrees per step
INCREMENTAL_MODE = False  # False for instant reset, True for incremental control

# Initialize Pygame and set up the display
pygame.init()
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption('MAVSDK Offboard Control - Local Velocity Sender')

# Colors, fonts, and initial settings
BACKGROUND_COLOR = (30, 30, 30)
TEXT_COLOR = (255, 255, 255)
FONT = pygame.font.Font(None, 36)
SMALL_FONT = pygame.font.Font(None, 24)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

# Setup UDP socket for sending commands
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

def send_velocity_body(velocity_x, velocity_y, velocity_z, yaw_rate):
    """Send a velocity command with optional yaw rate to the drone."""
    packet = ControlPacket(
        mode=SetpointMode.VELOCITY_BODY,
        enable_flag=True,
        yaw_control_flag=True,
        position=(0, 0, 0),
        velocity=(velocity_x, velocity_y, velocity_z),
        acceleration=(0, 0, 0),
        attitude=(0, 0, 0, 0),
        attitude_rate=(0, 0, 0, yaw_rate)
    )
    packed_data = packet.pack()
    sock.sendto(packed_data, (UDP_IP, UDP_PORT))

def display_text(message, position, font=FONT, color=TEXT_COLOR):
    """Displays text on the Pygame screen at the given position."""
    text = font.render(message, True, color)
    screen.blit(text, position)

def main():
    """Main function to handle keyboard inputs for drone control."""
    global INCREMENTAL_MODE
    running = True
    enabled = False
    velocity_x, velocity_y, velocity_z, yaw_rate = 0, 0, 0, 0
    clock = pygame.time.Clock()

    while running:
        screen.fill(BACKGROUND_COLOR)
        display_text("MAVSDK Offboard Control: Local Velocity Sender", (50, 20), font=FONT)
        display_text("Press 'E' to enable, 'C' to cancel, 'M' to toggle mode, 'H' to hold, 'Q' to quit", (50, 50), font=SMALL_FONT)
        mode_text = "Incremental" if INCREMENTAL_MODE else "Instant Reset"
        display_text(f"Mode: {mode_text}", (50, 80), font=SMALL_FONT)
        if enabled:
            display_text("Status: Enabled", (50, 100), font=SMALL_FONT, color=GREEN)
        else:
            display_text("Status: Disabled", (50, 100), font=SMALL_FONT, color=RED)
        display_text(f"Current Command: Vx={velocity_x}, Vy={velocity_y}, Vz={velocity_z}, Yaw Rate={yaw_rate}", (50, 500), font=SMALL_FONT)
        display_text(f"IP: {UDP_IP}, Port: {UDP_PORT}, Rate: {SEND_RATE}s", (50, 550), font=SMALL_FONT)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    send_velocity_body(0, 0, 0, 0)  # Safety stop
                    running = False
                elif event.key == pygame.K_e:
                    enabled = True
                elif event.key == pygame.K_c:
                    send_velocity_body(0, 0, 0, 0)  # Safety stop
                    enabled = False
                elif event.key == pygame.K_m:
                    INCREMENTAL_MODE = not INCREMENTAL_MODE
                elif event.key == pygame.K_h:
                    velocity_x, velocity_y, velocity_z, yaw_rate = 0, 0, 0, 0

                if enabled:
                    if event.key == pygame.K_w:
                        velocity_x = velocity_x + DEFAULT_SPEED if INCREMENTAL_MODE else DEFAULT_SPEED
                    elif event.key == pygame.K_s:
                        velocity_x = velocity_x - DEFAULT_SPEED if INCREMENTAL_MODE else -DEFAULT_SPEED
                    elif event.key == pygame.K_a:
                        velocity_y = velocity_y - DEFAULT_SPEED if INCREMENTAL_MODE else -DEFAULT_SPEED
                    elif event.key == pygame.K_d:
                        velocity_y = velocity_y + DEFAULT_SPEED if INCREMENTAL_MODE else DEFAULT_SPEED
                    elif event.key == pygame.K_UP:
                        velocity_z = velocity_z - DEFAULT_SPEED if INCREMENTAL_MODE else -DEFAULT_SPEED  # Reversed
                    elif event.key == pygame.K_DOWN:
                        velocity_z = velocity_z + DEFAULT_SPEED if INCREMENTAL_MODE else DEFAULT_SPEED  # Reversed
                    elif event.key == pygame.K_LEFT:
                        yaw_rate = -YAW_RATE_STEP if not INCREMENTAL_MODE else (yaw_rate - YAW_RATE_STEP)
                    elif event.key == pygame.K_RIGHT:
                        yaw_rate = YAW_RATE_STEP if not INCREMENTAL_MODE else (yaw_rate + YAW_RATE_STEP)

            elif event.type == pygame.KEYUP:
                if not INCREMENTAL_MODE:
                    if event.key in [pygame.K_w, pygame.K_s]:
                        velocity_x = 0
                    elif event.key in [pygame.K_a, pygame.K_d]:
                        velocity_y = 0
                    elif event.key in [pygame.K_UP, pygame.K_DOWN]:
                        velocity_z = 0
                    elif event.key in [pygame.K_LEFT, pygame.K_RIGHT]:
                        yaw_rate = 0

        if enabled:
            send_velocity_body(velocity_x, velocity_y, velocity_z, yaw_rate)

        pygame.display.flip()
        clock.tick(1 / SEND_RATE)

    sock.close()
    pygame.quit()

if __name__ == "__main__":
    main()
