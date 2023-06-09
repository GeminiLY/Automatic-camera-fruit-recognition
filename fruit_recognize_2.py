import cv2

# 加载图像
img = cv2.imread('1.jpg')

# 缩放图像
scale_percent = 50 # 缩放比例
width = int(img.shape[1] * scale_percent / 100)
height = int(img.shape[0] * scale_percent / 100)
dim = (width, height)
resized = cv2.resize(img, dim, interpolation = cv2.INTER_AREA)

# 灰度化和阈值化
gray = cv2.cvtColor(resized, cv2.COLOR_BGR2GRAY)
ret, thresh = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)

# 查找轮廓
contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

# 初始化水果数量
apple_count = 0
banana_count = 0
orange_count = 0
pear_count = 0

# 统计每种水果的数量
for i, contour in enumerate(contours):
    area = cv2.contourArea(contour)
    if area > 1000: # 只处理较大的轮廓
        x, y, w, h = cv2.boundingRect(contour)
        roi = resized[y:y+h, x:x+w] # 获取ROI区域
        hsv = cv2.cvtColor(roi, cv2.COLOR_BGR2HSV) # 转换到HSV色彩空间
        # 根据颜色阈值判断水果类型
        if hsv[:,:,0].mean() > 20 and hsv[:,:,0].mean() < 40 and hsv[:,:,1].mean() > 80 and hsv[:,:,2].mean() > 50:
            apple_count += 1
            cv2.putText(resized, 'Apple', (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)
        elif hsv[:,:,0].mean() > 30 and hsv[:,:,0].mean() < 70 and hsv[:,:,1].mean() > 80 and hsv[:,:,2].mean() > 50:
            banana_count += 1
            cv2.putText(resized, 'Banana', (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)
        elif hsv[:,:,0].mean() > 5 and hsv[:,:,0].mean() < 20 and hsv[:,:,1].mean() > 80 and hsv[:,:,2].mean() > 50:
            orange_count += 1
            cv2.putText(resized, 'Orange', (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)
        elif hsv[:,:,0].mean() > 160 and hsv[:,:,0].mean() < 180 and hsv[:,:,1].mean() > 80 and hsv[:,:,2].mean() > 50:
            pear_count += 1
            cv2.putText(resized, 'Pear', (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)

cv2.putText(resized, 'Apples: {}'.format(apple_count), (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)
cv2.putText(resized, 'Bananas: {}'.format(banana_count), (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)
cv2.putText(resized, 'Oranges: {}'.format(orange_count), (10, 90), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)
cv2.putText(resized, 'Pears: {}'.format(pear_count), (10, 120), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)

cv2.imshow('Fruits', resized)
cv2.waitKey(0)
cv2.destroyAllWindows()
