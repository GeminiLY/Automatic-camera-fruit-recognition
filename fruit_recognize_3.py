import cv2
import numpy as np

# 读入图像
img = cv2.imread('1.jpg')

# 将图像转换为HSV色彩空间
hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

# 设定颜色阈值，提取图像中的水果区域
lower_red = np.array([0, 100, 100])
upper_red = np.array([10, 255, 255])
mask1 = cv2.inRange(hsv, lower_red, upper_red)

lower_red = np.array([160, 100, 100])
upper_red = np.array([179, 255, 255])
mask2 = cv2.inRange(hsv, lower_red, upper_red)

mask = mask1 + mask2

# 对提取到的水果区域进行轮廓检测
contours, hierarchy = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

# 定义各个水果的颜色阈值
apple_lower = np.array([0, 50, 50])
apple_upper = np.array([10, 255, 255])
banana_lower = np.array([20, 50, 50])
banana_upper = np.array([40, 255, 255])
orange_lower = np.array([10, 50, 50])
orange_upper = np.array([25, 255, 255])
pear_lower = np.array([70, 50, 50])
pear_upper = np.array([90, 255, 255])

# 遍历每个轮廓，并识别其所属的水果类别
apple_count = 0
banana_count = 0
orange_count = 0
pear_count = 0

for contour in contours:
    area = cv2.contourArea(contour)
    if area < 100:
        continue
    x, y, w, h = cv2.boundingRect(contour)
    roi = img[y:y+h, x:x+w]
    hsv_roi = cv2.cvtColor(roi, cv2.COLOR_BGR2HSV)
    if apple_lower[0] <= hsv_roi[:, :, 0].mean() <= apple_upper[0] and apple_lower[1] <= hsv_roi[:, :, 1].mean() <= apple_upper[1] and apple_lower[2] <= hsv_roi[:, :, 2].mean() <= apple_upper[2]:
        apple_count += 1
        cv2.putText(img, 'Apple', (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)
    elif banana_lower[0] <= hsv_roi[:, :, 0].mean() <= banana_upper[0] and banana_lower[1] <= hsv_roi[:, :, 1].mean() <= banana_upper[1] and banana_lower[2] <= hsv_roi[:, :, 2].mean() <= banana_upper[2]:
        banana_count += 1
        cv2.putText(img, 'Banana', (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)
    elif orange_lower[0] <= hsv_roi[:, :, 0].mean() <= orange_upper[0] and orange_lower[1] <= hsv_roi[:, :, 1].mean() <= orange_upper[1] and orange_lower[2] <= hsv_roi[:, :, 2].mean() <= orange_upper[2]:
        orange_count += 1
        cv2.putText(img, 'Orange', (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)
    elif pear_lower[0] <= hsv_roi[:, :, 0].mean() <= pear_upper[0] and pear_lower[1] <= hsv_roi[:, :, 1].mean() <= pear_upper[1] and pear_lower[2] <= hsv_roi[:, :, 2].mean() <= pear_upper[2]:
        pear_count += 1
        cv2.putText(img, 'Pear', (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)

print('There are', apple_count, 'apples.')
print('There are', banana_count, 'bananas.')
print('There are', orange_count, 'oranges.')
print('There are', pear_count, 'pears.')

cv2.imshow('Result', img)
cv2.waitKey(0)
cv2.destroyAllWindows()
