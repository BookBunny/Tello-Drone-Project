from djitellopy import TelloSwarm

drones = ['192.168.10.1', '192.168.10.2', '192.168.10.3', '192.168.10.4']

# Create a TelloSwarm object with 4 drones
swarm = TelloSwarm.fromIps(drones)

# Set the second drone as the master drone
swarm.set_master('192.168.10.2')

# Connect to the drones
swarm.connect()

# Take off all the drones
swarm.takeoff()

# Fly the drones in a square pattern
for i in range(4):
    swarm.move_forward(100)
    swarm.rotate_clockwise(90)

# Flip all the drones to the left
swarm.flip_left()

# Land all the drones
swarm.land()

# Disconnect from the drones
swarm.end()
