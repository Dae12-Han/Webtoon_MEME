import cv2 
import numpy as np
from google.colab.patches import cv2_imshow
# 대사를 입력받아 빈 이미지 중앙에 삽입하였고 여백을 제거해 글자만 나타낼 수 있도록 사이즈 조절을 하였습니다.
from PIL import Image,ImageDraw,ImageFont, ImageOps, ImageFilter
import textwrap

logo = cv2.imread("/content/KakaoTalk_20211025_191909677.png", cv2.IMREAD_COLOR) #만들어진 말풍선
back = cv2.imread("/content/p5.jpg", cv2.IMREAD_COLOR) #만화로 바뀐 이미지

background = cv2.resize(back, dsize=(1000, 600),
                         interpolation=cv2.INTER_AREA)

logo = cv2.resize(logo, dsize=(200, 100), interpolation=cv2.INTER_AREA)
logo_gray = cv2.cvtColor(logo, cv2.COLOR_BGR2GRAY)
ret, logo_mask = cv2.threshold(logo_gray, 249, 255, cv2.THRESH_BINARY)

logo_mask_inv = cv2.bitwise_not(logo_mask)


# 넣고 싶은 위치에 합성할 이미지의 크기만큼 배경 이미지를 잘라냄
height, width = logo_gray.shape[:2]
background_cut = background[0:height, 0:width]

# 배경 이미지에는 로고 들어갈 위치 삭제
# 로고에는 로고만 냄기고 배경 삭제
img1 = cv2.bitwise_and(logo, logo, mask=logo_mask_inv)
img2 = cv2.bitwise_and(background_cut, background_cut, mask=logo_mask)

tmp = cv2.add(img1, img2)
background[0:height, 0:width] = tmp #위치

#cv2_imshow(background) #최종 이미지

#cv2.waitKey(0)

cv2.imwrite('./results/speech_bubble_result' + '.png', background)