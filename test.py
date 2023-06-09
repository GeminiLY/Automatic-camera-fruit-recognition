import cv2
import math
import numpy as np


# load images
image1 = cv2.imread("2023_02_06_03_55.jpg")
image2 = cv2.imread("2023_02_06_03_56.jpg")

# compute difference
difference = image1.copy()
cv2.absdiff(image1, image2, difference)
cv2.imwrite('difference.png', difference)

# 反色
diff_reverse = 255 - difference
cv2.imwrite("diff_reverse.png", diff_reverse)

# # converting the difference into grascale
# gray = cv2.cvtColor(difference, cv2.COLOR_BGR2GRAY)

IMGpath = "diff_reverse.png"
img = cv2.imread(IMGpath)
hsv_img = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

# -------------------苹果检测-----------------#
apple_num = 0
lower_apple = np.array([0, 50, 50])  # 颜色范围低阈值
upper_apple = np.array([30, 255, 255])  # 颜色范围高阈值
mask_apple = cv2.inRange(hsv_img, lower_apple, upper_apple)  # 根据颜色范围删选
mask_apple = cv2.medianBlur(mask_apple, 9)  # 中值滤波
cv2.imshow('mask_apple', mask_apple)
cv2.imwrite('mask_apple.jpg', mask_apple)
contours2, hierarchy2 = cv2.findContours(mask_apple, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
for cnt2 in contours2:
    center, radius = cv2.minEnclosingCircle(cnt2)
    area = cv2.contourArea(cnt2)
    # print(radius)
    rate = area / (math.pi * radius * radius)

    if radius > 50 and radius < 75 and rate < 0.91:
        # print(radius)
        cv2.circle(img, (int(center[0]), int(center[1])), int(radius), (0, 255, 0), 2)
        print("apple")
        # cv2.putText(img, 'apple', (int(center[0]), int(center[1])), font, 1, (255, 0, 0), 2)
        # apple_num += 1
# item_1 = QTableWidgetItem("%d" % apple_num)
# self.tableWidget.setItem(6, 0, item_1)
