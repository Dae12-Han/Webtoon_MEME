import cv2
import mediapipe as mp
import numpy as np
import math
mp_face_detection = mp.solutions.face_detection
mp_drawing = mp.solutions.drawing_utils

#이미지 여러장 불러오기
import glob
images = glob.glob('./cartoonized_images/*.jpg')
#IMAGE_FILES = ['./cartoonized_images/img3_cartoon.jpg']

IMAGE_FILES = []
for img in images:
    IMAGE_FILES.append(img)

'''
#x,y좌표 배열 저장
Coordinate=[]
global Coordinate
'''

with mp_face_detection.FaceDetection(
    model_selection=1, min_detection_confidence=0.5) as face_detection:
  for idx, file in enumerate(IMAGE_FILES):
    image = cv2.imread(file)
    #y_height, x_width, _ = image.shape
    # Convert the BGR image to RGB and process it with MediaPipe Face Detection.
    results = face_detection.process(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))

    # Draw face detections of each face.
    if not results.detections:
      continue
    annotated_image = image.copy()
    num=1
    
    for detection in results.detections:
      annotated_image = image.copy()
      print('\n===============')
      print('MOUTH CENTER:  ' + 'people' + str(num))
      print(mp_face_detection.get_key_point(
          detection, mp_face_detection.FaceKeyPoint.MOUTH_CENTER)) #x, y 전체 좌표
    
        
      #print(mp_face_detection.get_key_point(detection, mp_face_detection.FaceKeyPoint.MOUTH_CENTER).x) #x 좌표
      #print(mp_face_detection.get_key_point(detection, mp_face_detection.FaceKeyPoint.MOUTH_CENTER).y) #y 좌표
        
      #x = int(mp_face_detection.get_key_point(detection, mp_face_detection.FaceKeyPoint.MOUTH_CENTER).x*x_width)
      #y = int(mp_face_detection.get_key_point(detection, mp_face_detection.FaceKeyPoint.MOUTH_CENTER).y*y_height)
      #print("x 좌표: ", x, "y 좌표: ", y)
      
      logo = cv2.imread("./speech_bubble/speech_bubble.png", cv2.IMREAD_COLOR) #만들어진 말풍선
      #back = cv2.imread("/content/p5.jpg", cv2.IMREAD_COLOR) #만화로 바뀐 이미지
      back = cv2.imread(file, cv2.IMREAD_COLOR) #만화로 바뀐 이미지    

      background = cv2.resize(back, dsize=(1000, 600),
                              interpolation=cv2.INTER_AREA)

      logo = cv2.resize(logo, dsize=(200, 100), interpolation=cv2.INTER_AREA)
      logo_gray = cv2.cvtColor(logo, cv2.COLOR_BGR2GRAY)
      ret, logo_mask = cv2.threshold(logo_gray, 249, 255, cv2.THRESH_BINARY)

      logo_mask_inv = cv2.bitwise_not(logo_mask)
    
      x = int(mp_face_detection.get_key_point(detection, mp_face_detection.FaceKeyPoint.MOUTH_CENTER).x*background.shape[1])
      y = int(mp_face_detection.get_key_point(detection, mp_face_detection.FaceKeyPoint.MOUTH_CENTER).y*background.shape[0])
      print("x coordinate: ",x, "y coordinate: ", y)


      # 넣고 싶은 위치에 합성할 이미지의 크기만큼 배경 이미지를 잘라냄
      height, width = logo_gray.shape[:2]
      #background_cut = background[0:height, 0:width]
      background_cut = background[y-int(logo.shape[0]/2):y+int(logo.shape[0]/2),x-int(logo.shape[1]/2):x+int(logo.shape[1]/2)]

      # 배경 이미지에는 로고 들어갈 위치 삭제
      # 로고에는 로고만 냄기고 배경 삭제
      img1 = cv2.bitwise_and(logo, logo, mask=logo_mask_inv)
      img2 = cv2.bitwise_and(background_cut, background_cut, mask=logo_mask)

      tmp = cv2.add(img1, img2)
      #background[0:height, 0:width] = tmp #위치
    
      print("그림 세로: " , image.shape[0])
      #그림 안 관심영역 크기
      background[y-int(logo.shape[0]/2):y+int(logo.shape[0]/2),x-int(logo.shape[1]/2):x+int(logo.shape[1]/2)] = tmp #위치

      cv2.imwrite('./results/speech_bubble_result' + str(idx) + '.png', background)
      #mp_drawing.draw_detection(annotated_image, detection)
      num+=1

    #나온 이미지 결과값 저장하기
    #cv2.imwrite('./results/result' + str(idx) + '.png', annotated_image)
    
    

    
