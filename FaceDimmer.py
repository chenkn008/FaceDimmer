import cv2
import face_recognition
import time
import osascript

with open("scripts/brighten.applescript") as brighten_file:
    brighten_script = brighten_file.read()

with open("scripts/dim.applescript") as dim_file:
    dim_script = dim_file.read()

def dim():
    osascript.osascript(dim_script)

def brighten():
    osascript.osascript(brighten_script)

# use logistic_growth_func to calculate time_delay
# f(t) = c/(1+a*(e**(-t)))
# t = times of face_detected
# c = up limit of the growth e.g. 15
def logistic_growth(t):
    e = 2.71828
    c = 15
    a = 7
    return c/(1+ a*(e**(-t)))


# Get a reference to webcam #0 (the default one)
video_capture = cv2.VideoCapture(0)
video_capture.set(3, 160)  # Width of the frames in the video stream.
video_capture.set(4, 120)  # Height of the frames in the video stream.
# sec = 3
# video_capture.set(cv2.CAP_PROP_POS_MSEC,sec*1000)
# Wait for webcam started
while not video_capture.isOpened():
    time.sleep(2)

count_no_face_detected = 0
count_face_detected    = 0
screen_is_dimmed = False

time_delay = 5
count_threshold = 3  # how many itmes no face will trigure
while True:
    # Grab a single frame of video
    ret, frame = video_capture.read()

    frame_rgb = frame[:, :, ::-1]

    # face_locations = face_recognition.face_locations(frame_small_rgb)
    face_locations = face_recognition.face_locations(frame_rgb)
    if len(face_locations) > 0 : # if face detected
        count_no_face_detected = 0
        count_face_detected += 1
        time_delay = logistic_growth(count_face_detected)
        # print(time_delay)
        if screen_is_dimmed :
            brighten()
            screen_is_dimmed = False
    else:
        count_no_face_detected += 1
        # count_face_detected = max(count_threshold - count_no_face_detected, 0)
        count_face_detected = max(2 - count_no_face_detected, 0)
        time_delay = logistic_growth(count_face_detected)
        # print(time_delay)
        # if (count_no_face_detected >= count_threshold) and (not screen_is_dimmed):
        if (count_no_face_detected >= count_threshold):
            dim()
            screen_is_dimmed = True

    time.sleep(time_delay)
