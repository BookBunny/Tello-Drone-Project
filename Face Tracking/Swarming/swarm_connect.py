from djitellopy import Tello

ssid = "CGA2121_c2W3n6M"
password = "hnCygzRt7AB5Wc9V3W"

# Create a Tello object
drone = Tello()

# Connect to the Tello drone's Wi-Fi network
drone.connect()

# Send the Wi-Fi credentials to the Tello drone
drone.connect_to_wifi(ssid, password)


# Disconnect from the Tello drone's Wi-Fi network
drone.streamoff()
drone.end()
