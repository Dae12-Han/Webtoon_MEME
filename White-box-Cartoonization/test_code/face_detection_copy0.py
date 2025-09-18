# -*- coding: utf-8 -*-

from PIL import Image,ImageDraw,ImageFont, ImageOps, ImageFilter
from os import remove
from termcolor import colored
from PIL import Image
import matplotlib.pyplot as plt
import textwrap
import glob

import cv2
import mediapipe as mp
mp_face_detection = mp.solutions.face_detection
mp_drawing = mp.solutions.drawing_utils

import numpy as np
import os

IMAGE_FILES = []
for i in os.listdir('./cartoonized_images'):
  path = "./cartoonized_images/" + i
  IMAGE_FILES.append(path)

with mp_face_detection.FaceDetection(
    model_selection=1, min_detection_confidence=0.5) as face_detection:
  for idx, file in enumerate(IMAGE_FILES):
    image = cv2.imread(file)
    # Convert the BGR image to RGB and process it with MediaPipe Face Detection.
    results = face_detection.process(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))

    # Draw face detections of each face.
    if not results.detections:
      continue
    annotated_image = image.copy()

    num=1
    for detection in results.detections:
      annotated_image = image.copy()
      print("\n")
      print("==================================================================")
      print('Nose tip:  '+ str(num))
      print(mp_face_detection.get_key_point(
          detection, mp_face_detection.FaceKeyPoint.NOSE_TIP))
      print(type(mp_face_detection.get_key_point(
          detection, mp_face_detection.FaceKeyPoint.NOSE_TIP)))
      mp_drawing.draw_detection(annotated_image, detection)
      cv2.imshow("image" ,annotated_image)
      print("mmmmm")

      cv2.waitKey(0)
      choice_text= input(f"{num}번째 사람에 말풍선을 넣으시겠습니까? (y/n): ")
      if choice_text == "n":
        continue

      elif choice_text == "y":

        fig = plt.figure() # rows*cols 행렬의 i번째 subplot 생성
        rows = 1
        cols = 5
        i = 1
        xlabels = ["xlabel", "1", "2", "3", "4", "5"]

        for filename in glob.glob("./ballon/*.png"):
          img = cv2.imread(filename)
          img = cv2.resize(img, dsize=(1000, 500),
                              interpolation=cv2.INTER_AREA)
          ax = fig.add_subplot(rows, cols, i)
          ax.imshow(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
          ax.set_xlabel(xlabels[i])
          ax.set_xticks([]), ax.set_yticks([])
          if i >= 5:
              break
          i += 1
            
        plt.show()
            
        selectword = int(input("사용하실 말풍선 번호를 입력해주세요: "))

        print("-"*40)
        draw_text = input("대사를 입력하세요: ")
        para = textwrap.wrap(draw_text, width=15)
        font = ImageFont.truetype("./NanumGoDigANiGoGoDing.ttf", 50)
        
        text_width = 550
        text_height = 550

        canvas = Image.new('RGB', (text_width, text_height), "white")
        draw = ImageDraw.Draw(canvas)

        current_h, pad = 100, 10
        w1, h1 = 0, 0
        for line in para:
            w, h = draw.textsize(line, font=font)
            draw.text(((text_width - w) / 2, current_h), line, font=font, fill="black", attrs='bold', aline="center")
            current_h += h + pad
            w1 += w
            h1 += h

        print(w1, h1, current_h) # w1은 글자길이, h1은 줄 길이
        canvas.save("./bubble/next1.png")

        src = cv2.imread("./bubble/next1.png", cv2.IMREAD_UNCHANGED)
        if selectword == 1:
            if w1 >= 240:
                dst = src[0:current_h+70, 0:text_width].copy()
            else:
                dst = src[h1+30:current_h+30, int((text_width/2)-(w1/2)-60):int((text_width/2)+(w1/2)+60)].copy()
        
        elif selectword == 2:
            if w1 >= 240:
                dst = src[int(250-(250-(h1/2))-10):current_h+90, 0:text_width].copy()
            else:
                dst = src[h1+10:current_h+50, int((text_width/2)-(w1/2)-110):int((text_width/2)+(w1/2)+110)].copy()

        elif selectword == 3:
            if w1 >= 240:
                dst = src[int(250-(250-(h1/2))):current_h+70, 0:text_width].copy()
            else:
                dst = src[h1+30:current_h+40, int(250-(w1/2)-80):int(250+(w1/2)+80)].copy()

        elif selectword == 4:
            if w1 >= 240:
                dst = src[30:current_h+70, 0:text_width].copy()
            else:
                dst = src[h1+30:current_h+30, int((text_width/2)-(w1/2)-60):int((text_width/2)+(w1/2)+60)].copy()

        elif selectword == 5:
            if w1 >= 240:
                dst = src[30:current_h+70, 0:text_width].copy()
            else:
                dst = src[h1+30:current_h+30, int((text_width/2)-(w1/2)-60):int((text_width/2)+(w1/2)+60)].copy()
        else:
            print("잘못 입력하셨습니다.")

        cv2.imwrite("./bubble/next2.png", dst)

        cv2.waitKey(0)
        cv2.destroyAllWindows()

        # print("-"*40)
        # print("여기서부터는 배경 투명화작업입니다.")
        im = Image.open("./bubble/next2.png").convert('RGB')
        im_inv = ImageOps.invert(im)

        im_inv_L = im_inv.convert("L")
        im.putalpha(im_inv_L)
        # im.show()
        im.save("./bubble/next3.png")

        # print("-"*40)
        # print("여기서부터는 이미지 합성 작업입니다.")

        if selectword == 1:
            background = Image.open("./ballon/word1.png")
        elif selectword == 2:
            background = Image.open("./ballon/word2-1.png")
        elif selectword == 3:
            background = Image.open("./ballon/word2-2.png")
        elif selectword == 4:
            background = Image.open("./ballon/word3-1.png")
        elif selectword == 5:
            background = Image.open("./ballon/word3-2.png")

        foreground = Image.open("./bubble/next3.png")

        (img_h, img_w) = foreground.size
        resize_back = background.resize((img_h, img_w))

        resize_back.paste(foreground, (0, 0), foreground)

        # resize_back.show()
        resize_back.save("./bubble/final.png")

        remove("./bubble/next1.png")
        remove("./bubble/next2.png")
        remove("./bubble/next3.png")
        # remove("C:/Users/tree4/OneDrive/Desktop/test/final.png")

        print("모든 말풍선 작업이 완료되었습니다.")

      else:
        print("잘못 입력하셨습니다.")
        num += 1
        continue


      # from google.colab.patches import cv2_imshow
      # 대사를 입력받아 빈 이미지 중앙에 삽입하였고 여백을 제거해 글자만 나타낼 수 있도록 사이즈 조절을 하였습니다.
      logo = cv2.imread("./bubble/final.png", cv2.IMREAD_COLOR) # 말풍선 이미지를 받아들입니다.
      
      if num == 1:
        back = cv2.imread(file, cv2.IMREAD_COLOR)
      else:
        back = cv2.imread("./results/tempbackground_"+str(idx)+".png", cv2.IMREAD_COLOR)

      background = cv2.resize(back, dsize=(1000, 600),
                              interpolation=cv2.INTER_AREA) # 들어온 만화이미지가 이 부분에서 리사이즈 됩니다.
      print(background.shape)

      logo = cv2.resize(logo, dsize=(250, 150), interpolation=cv2.INTER_AREA)

      logo_gray = cv2.cvtColor(logo, cv2.COLOR_BGR2GRAY)
      ret, logo_mask = cv2.threshold(logo_gray, 251, 255, cv2.THRESH_BINARY)

      logo_mask_inv = cv2.bitwise_not(logo_mask)

      lift = mp_face_detection.get_key_point(
          detection, mp_face_detection.FaceKeyPoint.MOUTH_CENTER).y - mp_face_detection.get_key_point(
          detection, mp_face_detection.FaceKeyPoint.LEFT_EYE).y

      x = int(mp_face_detection.get_key_point(
          detection, mp_face_detection.FaceKeyPoint.NOSE_TIP).x*background.shape[1])
      y = int((mp_face_detection.get_key_point(
          detection, mp_face_detection.FaceKeyPoint.NOSE_TIP).y - 4 * lift)*background.shape[0])
      
      if y < 0:
        y = 0

      # 넣고 싶은 위치에 합성할 이미지의 크기만큼 배경 이미지를 잘라냄
      height, width = logo_gray.shape[:2]
      if (x+width > 1000):
        x = 750
      if (y+height > 600):
        y = 450
      
      background_cut = background[y:y+height, x:x+width]
      # 배경 이미지에는 로고 들어갈 위치 삭제
      # 로고에는 로고만 냄기고 배경 삭제
      img1 = cv2.bitwise_and(logo, logo, mask=logo_mask_inv)
      img2 = cv2.bitwise_and(background_cut, background_cut, mask=logo_mask)

      tmp = cv2.add(img1, img2)

      background[y:y+height, x:x+width] = tmp

      cv2.imshow(f"{num}번째" ,background)
      cv2.waitKey(0)
      cv2.imwrite("./results/tempbackground_"+str(idx)+".png", background)
      num += 1
      

    # cv2.imwrite('gdrive/MyDrive/content/tmp/annotated_image' + str(idx) + '.jpg', annotated_image)
#print(Result)



#첫번째 두번째 이미지 합치기
img1='./results/tempbackground_0.png'
img2='.results/tempbackground_1.png'

img1=cv2.imread(img1,1)
img2=cv2.imread(img2,1)

img1=cv2.resize(img1,(1000,600))
img2=cv2.resize(img2,(1000,600))

addv=cv2.vconcat([img1,img2])
addh=cv2.hconcat([img1,img2])

cv2.imwrite('./results/result'+'.png',addv)

#두번째 세번째 합치기
img1='./results/result.png'
img2='./results/tempbackground_2.png'

img1=cv2.imread(img1,1)
img2=cv2.imread(img2,1)

img2=cv2.resize(img2,(1000,600))

addv=cv2.vconcat([img1,img2])

cv2.imwrite('./results/result'+'.png',addv)

#세번쩨 네번째 합치기
img1='./results/result.png'
img2='./results//tempbackground_3.png'

img1=cv2.imread(img1,1)
img2=cv2.imread(img2,1)

img2=cv2.resize(img2,(1000,600))

addv=cv2.vconcat([img1,img2])

cv2.imwrite('./results/result'+'.png',addv)

#네번쩨 다섯번째 합치기
img1='./results/result.png'
img2='./results/tempbackground_4.png'

img1=cv2.imread(img1,1)
img2=cv2.imread(img2,1)

img2=cv2.resize(img2,(1000,600))

addv=cv2.vconcat([img1,img2])

cv2.imwrite('./results/result.png', addv)