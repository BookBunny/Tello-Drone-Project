import time
import cv2
import numpy as np
from djitellopy import tello

w, h = 720, 480
fb_range = [6200, 6800]
pid = [0.2, 0.2, 0]
pError = 0

drone = tello.Tello()
drone.connect()
drone.streamon()
drone.takeoff()

drone.send_rc_control(0, 0, 20, 0)
time.sleep(2.2)


def find_face(img):
    face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(img_gray, scaleFactor=1.2, minNeighbors=8)
    my_face_list = []
    my_face_list_area = []

    for (x, y, w, h) in faces:
        cv2.rectangle(img, (x, y), (x + w, y + h), (0, 0, 255), 2)
        cx = x + w // 2
        cy = y + h // 2
        area = w * h
        my_face_list.append([cx, cy])
        my_face_list_area.append(area)
        cv2.circle(img, (cx, cy), 5, (0, 255, 0), cv2.FILLED)
    if len(my_face_list_area) != 0:
        i = my_face_list_area.index(max(my_face_list_area))
        return img, [my_face_list[i], my_face_list_area]
    else:
        return img, [[0, 0], [0]]


def track_face(drone, info, w, pid, pError):
    area = info[1][0]
    x, y = info[0]
    fb = 0
    error = x - w // 2
    speed = pid[0] * error + pid[1] * (error - pError)
    speed = int(np.clip(speed, -100, 100))

    if area > fb_range[0] and area < fb_range[1]:
        fb = 0
    elif area > fb_range[1]:
        fb = -20
    elif area < fb_range[0] and area != 0:
        fb = 20
    if x == 0:
        speed = 0
        error = 0

    print(speed, fb)
    drone.send_rc_control(0, fb, 0, speed)
    return error


def main():
    pError = 0
    while True:
        img = drone.get_frame_read().frame
        img = cv2.resize(img, (w, h))
        img, info = find_face(img)
        pError = track_face(drone, info, w, pid, pError)
        print(drone.get_battery())
        cv2.imshow("Output", img)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            drone.land()
            break


main()
