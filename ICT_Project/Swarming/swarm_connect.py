import math
from djitellopy import Tello
import time


def follow_master(master_drone_ref, slave_drones_ref):
    # Establish communication between the drones
    # Use Wi-Fi or Bluetooth to establish communication
    # between the drones. You can use a simple
    # peer-to-peer protocol or a more sophisticated
    # communication protocol like MQTT or ROS.

    # Implement a swarming algorithm
    # The swarming algorithm will dictate how the slave drones
    # follow the master drone. Here's a simple algorithm that
    # makes the slave drones follow the master drone at a fixed
    # distance and angle:

    while True:
        # Get the position and orientation of the master drone
        master_state = master_drone_ref.get_current_state()
        master_x = master_state[0]
        master_y = master_state[1]
        master_z = master_state[2]
        master_yaw = master_state[3]

        counter = 1
        for slave in slave_drones_ref:
            # Calculate the desired position and orientation of the slave drones
            slave_x1 = master_x + counter * math.cos(master_yaw)
            slave_y1 = master_y + counter * math.sin(master_yaw)
            slave_z1 = master_z
            slave_yaw1 = master_yaw

            # Send commands to the slave drones to make them follow the master drone
            slave.move_to(slave_x1, slave_y1, slave_z1, slave_yaw1)

            # Send commands to the slave drones to perform other tasks
            # For example, you can make the drones perform synchronized
            # movements like flips or rotations.
            counter += 0.5


# Add the IP addresses of the Tello drones you want to connect to
ip_list = ["192.168.10.1", "192.168.10.2", "192.168.10.3"]

drones = []

# Connect to each Tello drone in the list
for ip in ip_list:
    drone = Tello(ip)
    drone.connect()
    print("Connected to drone with IP:", ip)
    drones.append(drone)

# # Disconnect from each Tello drone
# for drone in drones:
#     drone.disconnect()
#     print("Disconnected from drone with IP:", drone.get_ip())

for drone in drones:
    drone.takeoff()

master_drone = drones[0]
slave_drones = drones[1:]

time.sleep(2)

follow_master(master_drone, slave_drones)
