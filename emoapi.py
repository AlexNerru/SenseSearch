from statistics import mode
import os
import cv2
from keras.models import load_model
import numpy as np
import imutils

from utils.datasets import get_labels
from utils.inference import detect_faces
from utils.inference import draw_text
from utils.inference import draw_bounding_box
from utils.inference import apply_offsets
from utils.inference import load_detection_model
from utils.preprocessor import preprocess_input

detection_model_path = 'trained_models/detection_models/haarcascade_frontalface_default.xml'
emotion_model_path = 'trained_models/emotion_models/fer2013_mini_XCEPTION.102-0.66.hdf5'
emotion_labels = get_labels('fer2013')
face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_alt.xml')

frame_window = 10
emotion_offsets = (20, 40)

face_detection = load_detection_model(detection_model_path)
emotion_classifier = load_model(os.path.join(os.path.dirname(os.path.realpath(__file__)),
									   emotion_model_path), compile=False)

emotion_target_size = emotion_classifier.input_shape[1:3]

emotion_window = []



def emotionimg(img):
    # bgr_image = video_capture.read()[1]
    gray_face = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    gray_face = cv2.resize(gray_face, (emotion_target_size))
    gray_face = preprocess_input(gray_face, True)
    gray_face = np.expand_dims(gray_face, 0)
    gray_face = np.expand_dims(gray_face, -1)
    emotion_prediction = emotion_classifier.predict(gray_face)
    emotion_label_arg = np.argmax(emotion_prediction)
    emotion_text = emotion_labels[emotion_label_arg]
    return emotion_text


def detect_faces(frame):
    frame = imutils.resize(frame)
    small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
    gray = cv2.cvtColor(small_frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(
        gray,
        scaleFactor=1.05,
        minNeighbors=5,
        minSize=(20, 20),
        flags=cv2.CASCADE_SCALE_IMAGE
    )
    return faces


def videoemot(path):
    cap = cv2.VideoCapture(path)
    emot = []
    while(cap.isOpened()):
        ret, frame = cap.read()
        if ret:
            a = detect_faces(frame)*4
            if len(a) > 0:
                for f in a:
                    try:
                        emot.append(emotionimg(frame[f[1]:f[1] + f[3], f[0]:f[0] + f[2]]))
                        #cv2.rectangle(frame, (f[0], f[1]), (f[0] + f[2], f[1] + f[3]), (0, 255, 0), 2)
                    except:
                        continue
        else:
            break
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    cap.release()
    count = len(emot)
    em_list = ('angry', 'disgust', 'fear', 'happy', 'neutral', 'sad', 'surprise')
    em_1 = {}
    for k in em_list:
        em_1[k] = 0
    for k in emot:
        em_1[k]+=1
    for k in em_list:
        try:
            em_1[k]=(float(em_1[k])/count)*100
        except:
            em_1[k] = 0
    return em_1

