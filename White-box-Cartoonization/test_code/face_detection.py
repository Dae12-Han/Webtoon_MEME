import cv2
import mediapipe as mp
import numpy as np
from PIL import Image,ImageDraw,ImageFont, ImageOps, ImageFilter
import textwrap
mp_face_detection = mp.solutions.face_detection
mp_drawing = mp.solutions.drawing_utils

#이미지 여러장 불러오기
import os
import glob

IMAGE_FILES = []
for i in os.listdir('./cartoonized_images/'):
    path='./cartoonized_images/'+i
    IMAGE_FILES.append(path)

#images = glob.glob('./cartoonized_images/*.jpg')
#images = glob.glob('./cartoonized_images/test4.jpg')

#MAGE_FILES = []
#or img in images:
#   IMAGE_FILES.append(img)

with mp_face_detection.FaceDetection(model_selection=1, min_detection_confidence=0.5) as face_detection:
    for idx, file in enumerate(IMAGE_FILES):
        image = cv2.imread(file)
        # Convert the BGR image to RGB and process it with MediaPipe Face Detection.
        results = face_detection.process(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))

        # Draw face detections of each face.
        if not results.detections:
            continue
        annotated_image = image.copy()
        annotated_image = cv2.resize(annotated_image, dsize=(1000, 600),interpolation=cv2.INTER_AREA) 
        
        #말풍선 이미지 불러오기
        speech_bubble = cv2.imread("./speech_bubble/speech_bubble.png", cv2.IMREAD_COLOR)
        speech_bubble = cv2.resize(speech_bubble, dsize=(200, 100), interpolation=cv2.INTER_AREA)
        #배경 불러오기
        back=cv2.imread(file, cv2.IMREAD_COLOR)
        background = cv2.resize(back, dsize=(1000, 600),interpolation=cv2.INTER_AREA) 
        
        #말풍선 Threshold
        speech_bubble_gray = cv2.cvtColor(speech_bubble, cv2.COLOR_BGR2GRAY)
        ret, speech_bubble_mask = cv2.threshold(speech_bubble_gray, 249, 255, cv2.THRESH_BINARY)
        speech_bubble_mask_inv = cv2.bitwise_not(speech_bubble_mask)
        
        for detection in results.detections:
            
            #print(mp_face_detection.get_key_point(detection, mp_face_detection.FaceKeyPoint.RIGHT_EAR))
            
            #오른쪽 귀 좌표 (이미지상에서는 왼쪽으로 보임)
            x=int(mp_face_detection.get_key_point(detection, mp_face_detection.FaceKeyPoint.LEFT_EAR_TRAGION).x*annotated_image.shape[1])
            #왼쪽 귀 좌표 (이미지상에서는 오른쪽으로 보임)
            y=int(mp_face_detection.get_key_point(detection, mp_face_detection.FaceKeyPoint.LEFT_EAR_TRAGION).y*annotated_image.shape[0])
            #mp_drawing.draw_detection(annotated_image, detection)
            #annotated_image=cv2.circle(annotated_image,(int(x*annotated_image.shape[1]),int(y*annotated_image.shape[0])),3,(0,0,255),-1)
            print(x,y)

            #말풍선 높이, 너비
            height, width = speech_bubble_gray.shape[:2]
            
            if (x-width)>=0 and (y-height)>=0 and (y+height)<600 and (x+width)<1000:
                background_cut = background[y-height:y, x-width:x]
                img1 = cv2.bitwise_and(speech_bubble, speech_bubble, mask=speech_bubble_mask_inv)
                img2 = cv2.bitwise_and(background_cut, background_cut, mask=speech_bubble_mask)
                tmp = cv2.add(img1, img2)            
                background[y-height:y, x-width:x] = tmp
                
        cv2.imwrite('./results/speech_bubble_result' + str(idx) + '.png', background)