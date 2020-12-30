import cv3
import face_recognition
import time
from PIL import Image, ImageDraw
import osascript

with open("scripts/brighten.applescript") as brighten_file:
    brighten_script = brighten_file.read()

with open("scripts/dim.applescript") as dim_file:
    dim_script = dim_file.read()

def dim():
    osascript.osascript(dim_script)

def brighten():
    osascript.osascript(brighten_script)

# Get a reference to webcam #0 (the default one)
video_capture = cv2.VideoCapture(0)
sec = 3
video_capture.set(cv2.CAP_PROP_POS_MSEC,sec*1000)
video_capture.set(3, 160)  # Width of the frames in the video stream.
video_capture.set(4, 120)  # Height of the frames in the video stream.

count_no_face_detected = 0
screen_is_dimmed = False 

while True:
    # Grab a single frame of video
    ret, frame = video_capture.read()

    # Resize frame of video to 1/4 size for faster face recognition processing
    # frame_small = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
    # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
    # frame_small_rgb = frame_small[:, :, ::-1]
    frame_rgb = frame[:, :, ::-1]

    # face_locations = face_recognition.face_locations(frame_small_rgb)
    face_locations = face_recognition.face_locations(frame_rgb)
    if len(face_locations) > 0 :
        # print("Face detected")
        count_no_face_detected = 0
        if screen_is_dimmed :
            brighten()
            screen_is_dimmed = False
    else:
        # print("No face detected")
        count_no_face_detected += 1
        if (count_no_face_detected >= 3) and (not screen_is_dimmed):
            dim()
            screen_is_dimmed = True

    # print(face_locations)

    # pil_image = Image.fromarray(frame_small_rgb)
    # draw = ImageDraw.Draw(pil_image)
    # for (top, right, bottom, left) in face_locations:
    #     draw.rectangle(((left, top), (right, bottom)), outline=(0, 0, 255),width=5)
    # pil_image.show()

    time.sleep(3)

    # pil_image = Image.fromarray(frame)
    # draw = ImageDraw.Draw(pil_image)
    # pil_image.show()
