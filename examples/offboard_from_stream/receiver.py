#!/usr/bin/env python3
"""
Drone Offboard Control Receiver
===============================

Overview:
---------
This script facilitates real-time reception and handling of drone control packets over UDP,
using MAVSDK to execute offboard control commands on a connected drone. It integrates with
the custom ControlPacket class to unpack control directives, and subsequently manages drone
state transitions to ensure smooth operation.

Features:
---------
- Real-time Packet Reception: Listens on a UDP socket for incoming control packets.
- MAVSDK Integration: Utilizes MAVSDK for comprehensive drone control, including setting
  initial positions, and managing various control setpoints like position, velocity, and yaw.
- Robust State Handling: Checks and transitions drone state to ensure offboard control can
  be safely engaged and disengaged.
- Yaw Management: Supports optional yaw control, setting either a dynamic or static yaw
  based on packet instructions.

Usage:
------
To use this script:
1. Ensure the MAVSDK server is running and the drone is connected.
2. Run this script on the same network as the MAVSDK server.
3. Send properly formatted control packets to the IP and port specified in this script.

Packet Handling:
----------------
The script unpacks received packets using the ControlPacket class. It then checks the enable
flag within these packets to either initiate or halt offboard control. If enabled, the script
handles the specified control setpoints (position, velocity, yaw, etc.) and updates the drone's
state accordingly.


Author:
-------
Alireza Ghaderi
GitHub: alireza787b
Date: April 2024

Example Usage:
--------------
Ensure that the drone is connected and the MAVSDK server is running. Execute this script
in a Python environment where MAVSDK-Python is installed. The script will handle setup
and loop indefinitely, processing incoming packets until manually stopped.

Dependencies:
- MAVSDK-Python
- Python 3.7 or higher

The script's flow is asynchronous to efficiently handle I/O operations. It is crucial
to ensure that the system running this script has network access to the drone's telemetry
and control interface, typically provided by MAVSDK.

# Assume appropriate imports and setup already discussed.
async def main():
    print("Starting the drone control packet receiver...")
    drone = await setup_drone()
    await receive_packets(drone)

if __name__ == "__main__":
    asyncio.run(main())

"""

import asyncio
import socket
from mavsdk import System
import mavsdk
from mavsdk.offboard import AccelerationNed, Attitude, OffboardError, PositionGlobalYaw, PositionNedYaw, VelocityBodyYawspeed, VelocityNedYaw
from control_packet import ControlPacket, SetpointMode  # Ensure this import matches your setup

UDP_IP = "0.0.0.0"
UDP_PORT = 5005
BUFFER_SIZE = 1024  # Adjust based on expected packet size
PX4_MAVLINK_NODE = "udp://:14540"


async def setup_drone():
    drone = System()
    await drone.connect(system_address=PX4_MAVLINK_NODE)

    print("Waiting for drone to connect...")
    async for state in drone.core.connection_state():
        if state.is_connected:
            print("-- Connected to drone!")
            break

    print("Checking global position estimate...")
    async for health in drone.telemetry.health():
        if health.is_global_position_ok:
            print("-- Global position estimate OK")
            break

    return drone

async def handle_packet(drone, packet):
    control_packet = ControlPacket.unpack(packet)
    control_packet.debug_print()

    if control_packet.enable_flag:
        print("Enable flag is true, processing offboard control...")
        is_active = await drone.offboard.is_active()
        current_yaw = 0  # Default yaw initialization

        if not is_active:
            print("Offboard mode is not active, initializing...")
            # Correctly obtaining current position and yaw from telemetry
            async for telemetry in drone.telemetry.attitude_euler():
                current_yaw = telemetry.yaw_deg  # Capture the initial yaw in degrees
                break

            async for position in drone.telemetry.position_velocity_ned():
                current_position = position
                break  # Break after obtaining the first most recent value

            print(f"Setting initial position and yaw: North {current_position.position.north_m}, East {current_position.position.east_m}, Down {current_position.position.down_m}, Yaw {current_yaw}")
            await drone.offboard.set_position_ned(
                PositionNedYaw(current_position.position.north_m, current_position.position.east_m,
                               current_position.position.down_m, current_yaw))
            try:
                await drone.offboard.start()
                print("Offboard mode started successfully.")
            except OffboardError as error:
                print(f"Failed to start offboard mode: {error._result.result}")
                return

        # Determine if yaw control is specified
        yaw = control_packet.attitude[2] if control_packet.setpoint_flags & SetpointMode.YAW_CONTROL.value else current_yaw

        if control_packet.setpoint_flags & SetpointMode.POSITION_LOCAL_NED.value:
            print(f"Sending POSITION_LOCAL_NED setpoint: North {control_packet.position[0]}, East {control_packet.position[1]}, Down {control_packet.position[2]}, Yaw {yaw}")
            await drone.offboard.set_position_ned(
                PositionNedYaw(control_packet.position[0], control_packet.position[1], control_packet.position[2], yaw))
            
        if control_packet.setpoint_flags & SetpointMode.VELOCITY_BODY.value:
            vx = control_packet.velocity[0]
            vy = control_packet.velocity[1]
            vz = control_packet.velocity[2]
            yaw_rate = control_packet.attitude_rate[3]  # Assume yaw rate is the fourth element in attitude tuple
            await drone.offboard.set_velocity_body(VelocityBodyYawspeed(vx, vy, vz, yaw_rate))
            print(f"Setting VELOCITY_BODY setpoint: Vx={vx}, Vy={vy}, Vz={vz}, Yaw rate={yaw_rate}")
            
        if control_packet.setpoint_flags & SetpointMode.ATTITUDE_CONTROL.value:
            roll = control_packet.attitude[0]
            pitch = control_packet.attitude[1]
            yaw = control_packet.attitude[2]
            thrust = control_packet.attitude[3]  # Ensure thrust is a value between 0 and 1
            print(f"Setting ATTITUDE setpoint: Roll={roll}°, Pitch={pitch}°, Yaw={yaw}°, Thrust={thrust}")
            await drone.offboard.set_attitude(Attitude(roll, pitch, yaw, thrust))
        if control_packet.setpoint_flags & SetpointMode.POSITION_VELOCITY_ACCELERATION_NED.value:
            position = PositionNedYaw(control_packet.position[0], control_packet.position[1], control_packet.position[2], control_packet.attitude[2])
            velocity = VelocityNedYaw(control_packet.velocity[0], control_packet.velocity[1], control_packet.velocity[2], control_packet.attitude_rate[2])
            acceleration = AccelerationNed(control_packet.acceleration[0], control_packet.acceleration[1], control_packet.acceleration[2])
            print(f"Sending POSITION_VELOCITY_ACCELERATION_NED setpoint: Position {position}, Velocity {velocity}, Acceleration {acceleration}")
            await drone.offboard.set_position_velocity_acceleration_ned(position, velocity, acceleration)
        if control_packet.setpoint_flags & SetpointMode.POSITION_GLOBAL_LATLON.value:
            lat = control_packet.position[0]
            lon = control_packet.position[1]
            alt = control_packet.position[2]
            yaw = control_packet.attitude[2] 
            altitude_type = mavsdk.offboard.AltitudeType.AMSL  # Choose based on your requirements: AGL or AMSL or REL_HOME 

            print(f"Sending POSITION_GLOBAL_LATLON setpoint: Latitude {lat}, Longitude {lon}, Altitude {alt}, Yaw {yaw}")
            await drone.offboard.set_position_global(PositionGlobalYaw(lat, lon, alt, yaw, altitude_type))
        if control_packet.setpoint_flags & SetpointMode.ACCELERATION_NED.value:
            # Extract acceleration values from the packet
            north_acc = control_packet.acceleration[0]
            east_acc = control_packet.acceleration[1]
            down_acc = control_packet.acceleration[2]
            print(f"Setting NED acceleration: North {north_acc} m/s², East {east_acc} m/s², Down {down_acc} m/s²")
            await drone.offboard.set_acceleration_ned(
                AccelerationNed(north_m_s2=north_acc, east_m_s2=east_acc, down_m_s2=down_acc)
            )
        # Check for velocity NED setpoint
        if control_packet.setpoint_flags & SetpointMode.VELOCITY_NED.value:
            north_vel = control_packet.velocity[0]
            east_vel = control_packet.velocity[1]
            down_vel = control_packet.velocity[2]
            yaw = control_packet.attitude[2]  # Assuming yaw is stored in the attitude tuple

            print(f"Setting NED velocity: North {north_vel}, East {east_vel}, Down {down_vel}, Yaw {yaw}")
            await drone.offboard.set_velocity_ned(
                VelocityNedYaw(north_m_s=north_vel, east_m_s=east_vel, down_m_s=down_vel, yaw_deg=yaw)
            )
            



    else:
        is_active = await drone.offboard.is_active()
        if is_active:
            print("Enable flag is false, stopping offboard mode...")
            await drone.offboard.stop()

async def receive_packets(drone):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((UDP_IP, UDP_PORT))
    print("UDP socket bound and listening for packets...")

    while True:
        data, _ = sock.recvfrom(BUFFER_SIZE)
        if data:
            await handle_packet(drone, data)

async def run():
    drone = await setup_drone()
    await receive_packets(drone)

if __name__ == "__main__":
    asyncio.run(run())