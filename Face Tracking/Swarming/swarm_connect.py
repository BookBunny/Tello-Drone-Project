from djitellopy import Tello

ssid = "Your wifi network name"
password = "Your wifi password"

# Create a Tello object
drone = Tello()

# Connect to the Tello drone's Wi-Fi network
drone.connect()

# Send the Wi-Fi credentials to the Tello drone
drone.connect_to_wifi(ssid, password)


# Disconnect from the Tello drone's Wi-Fi network
drone.streamoff()
drone.end()
