# import cv2
# from djitellopy import tello
#
#
# def detect_face(image):
#     # Load the face detection cascade
#     face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
#
#     # Convert the input image to grayscale
#     gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
#
#     # Detect faces in the grayscale image
#     faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5)
#
#     # Make a copy of the input image
#     output_image = image.copy()
#
#     # Draw a rectangle and circle around each detected face
#     for (x, y, w, h) in faces:
#         # Draw a rectangle around the face
#         cv2.rectangle(output_image, (x, y), (x + w, y + h), (0, 255, 0), 2)
#
#         # Draw a small circle in the center of the face
#         center_x = x + w // 2
#         center_y = y + h // 2
#
#         cv2.circle(output_image, (center_x, center_y), 5, (0, 255, 0), cv2.FILLED)
#
#     # Get the face area and center
#     if len(faces) > 0:
#         (x, y, w, h) = faces[0]
#         face_area = w * h
#         face_center = (int(x + w / 2), int(y + h / 2))
#     else:
#         face_area = None
#         face_center = None
#
#     # Return the output image with rectangles and circles and the face area and center as a tuple
#     return output_image, [face_area, face_center]
#
#
# cap = cv2.VideoCapture(0)
# while True:
#     _, img = cap.read()
#     live_feed, info = detect_face(img)
#     cv2.imshow('Output', live_feed)
#     print('Face area:', info[0])
#     print('Face center:', info[1])
#     if cv2.waitKey(1) & 0xFF == ord('q'):
#         break
#
# cap.release()
# cv2.destroyAllWindows()

import cv2
import time
import djitellopy as tello


def detect_face(frame):
    # Load the face detection cascade
    face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

    # Convert the input frame to grayscale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Detect faces in the grayscale imagen
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5)

    # Draw a rectangle and circle around each detected face
    for (x, y, w, h) in faces:
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
        center_x = int(x + w / 2)
        center_y = int(y + h / 2)
        radius = int(min(w, h) / 2)
        cv2.circle(frame, (center_x, center_y), 2, (0, 0, 255), cv2.FILLED)

    # Get the face area and center
    if len(faces) > 0:
        (x, y, w, h) = faces[0]
        face_area = w * h
        face_center = (int(x + w / 2), int(y + h / 2))
    else:
        face_area = None
        face_center = None

    # Return the face area, center, and live feed as a tuple
    return frame, [face_area, face_center]


def track_face():
    # Initialize the drone and start the video stream
    drone = tello.Tello()
    drone.connect()
    drone.takeoff()
    drone.streamon()

    # Wait for the video stream to start
    time.sleep(2)

    # Set the speed of the drone and the distance from the face
    speed = 20
    distance = 100

    # Start a loop to track the face and control the drone
    while True:
        # Get the current frame from the drone's video stream
        frame = drone.get_frame_read().frame

        # Detect the face in the current frame
        live_feed, info = detect_face(frame)

        # Get the face center from the detected face information
        if info[1] is not None:
            face_center = info[1]

            # Calculate the error between the center of the frame and the center of the face
            frame_center = (frame.shape[1] // 2, frame.shape[0] // 2)
            error = (face_center[0] - frame_center[0], face_center[1] - frame_center[1])

            # Calculate the lateral and vertical velocities of the drone based on the error
            lateral_velocity = int(-error[0] / frame_center[0] * speed)
            vertical_velocity = int(-error[1] / frame_center[1] * speed)

            # Calculate the distance between the drone and the face
            distance_error = distance - info[0] ** 0.5 if info[0] is not None else 0

            # Adjust the lateral and vertical velocities based on the distance error
            if distance_error > 0:
                lateral_velocity = max(lateral_velocity, -speed)
                vertical_velocity = max(vertical_velocity, -speed)
            elif distance_error < 0:
                lateral_velocity = min(lateral_velocity, speed)
                vertical_velocity = min(vertical_velocity, speed)

            # Move the drone based on the velocities
            drone.send_rc_control(0, lateral_velocity, vertical_velocity, 0)

        # If the face is not detected, stop the drone
        else:
            drone.send_rc_control(0, 0, 0, 0)

        # Show the live feed with the detected face and the tracking information
        cv2.imshow('Live Feed', live_feed)

        # Quit the program if 'q' is pressed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Land the drone and close the windows
    drone.land()
    cv2.destroyAllWindows()


track_face()
