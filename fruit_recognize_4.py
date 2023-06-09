import cv2
import numpy as np

# 读取图片
img = cv2.imread('4.jpg')

# 缩放图像
scale_percent = 50  # 缩放比例
width = int(img.shape[1] * scale_percent / 100)
height = int(img.shape[0] * scale_percent / 100)
dim = (width, height)
img = cv2.resize(img, dim, interpolation=cv2.INTER_AREA)

# # 调整亮度和对比度
# alpha = 1  # 对比度调整参数
# beta = 50  # 亮度调整参数
# result = cv2.addWeighted(img, alpha, np.zeros(img.shape, img.dtype), 0, beta)
# # 显示结果
# cv2.imshow('image', result)
# cv2.waitKey(0)

# 将图片转换为灰度图
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# # 进行二值化处理
# ret, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)

# # 尝试不同的阈值值
# for threshold_value in range(50, 150, 10):
#     # 进行二值化处理
#     ret, thresh = cv2.threshold(gray, threshold_value, 255, cv2.THRESH_BINARY)
#
#     # 显示结果
#     cv2.imshow('image', thresh)
#     cv2.waitKey(0)
# cv2.destroyAllWindows()


# 进行自适应阈值处理
thresh = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 11, 2)

# 寻找轮廓
contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

# 过滤面积小于3000的轮廓
filtered_contours = []
for cnt in contours:
    area = cv2.contourArea(cnt)
    if area < 3000 or area > 12000:
        continue
    filtered_contours.append(cnt)

# 绘制轮廓
cv2.drawContours(img, filtered_contours, -1, (0, 0, 255), 2)

# 统计轮廓数量
num_contours = len(filtered_contours)
print("Number of contours detected:", num_contours)

# color_templates = {
#     'apple': ([0, 20, 80], [10, 255, 255]),  # 红色带淡黄色
#     'banana': ([20, 100, 100], [70, 255, 255]),  # 黄色带一点绿色
#     'pear': ([40, 20, 80], [80, 200, 200]),  # 浅绿色带点灰色
#     'orange': ([10, 100, 100], [40, 255, 255])  # 橘色
# }
#
# # 将图片转换为HSV颜色空间
# hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

# # 分析每个轮廓内的颜色分布
# fruit_counts = {}
# for contour in filtered_contours:
#     # 创建掩模
#     mask = np.zeros_like(hsv[:, :, 0])
#     cv2.drawContours(mask, [contour], -1, 255, -1)
#
#     # 计算颜色直方图
#     hist_hue = cv2.calcHist([hsv], [0], mask, [180], [0, 180])
#
#     # 将颜色直方图归一化
#     hist_hue = cv2.normalize(hist_hue, hist_hue, 0, 1, cv2.NORM_MINMAX)
#
#     # 找到与每个水果颜色模板的相似度
#     scores = {}
#     for fruit, template in color_templates.items():
#         # 判断该水果是否在颜色模板中
#         if fruit not in scores:
#             scores[fruit] = 0
#
#         # 判断该像素是否在颜色范围内
#         mask_color = cv2.inRange(hsv, np.array(template[0]), np.array(template[1]))
#         hist_color = cv2.calcHist([hsv], [0], mask_color, [180], [0, 180])
#
#         # 将颜色直方图归一化
#         hist_color = cv2.normalize(hist_color, hist_color, 0, 1, cv2.NORM_MINMAX)
#
#         # 计算相似度分数
#         score = cv2.compareHist(hist_hue, hist_color, cv2.HISTCMP_CORREL)
#         scores[fruit] = score
#
#     # 找到分数最高的水果
#     max_score = max(scores.values())
#     for fruit, score in scores.items():
#         if score == max_score:
#             if fruit not in fruit_counts:
#                 fruit_counts[fruit] = 0
#             fruit_counts[fruit] += 1
#
# for fruit, count in fruit_counts.items():
#     print(fruit, count)


# 定义各个水果的颜色阈值
apple_lower = np.array([0, 20, 80])
apple_upper = np.array([10, 255, 255])
banana_lower = np.array([20, 100, 100])
banana_upper = np.array([70, 255, 255])
orange_lower = np.array([10, 100, 100])
orange_upper = np.array([40, 255, 255])
pear_lower = np.array([40, 20, 80])
pear_upper = np.array([80, 200, 200])

# 遍历每个轮廓，并识别其所属的水果类别
apple_count = 0
banana_count = 0
orange_count = 0
pear_count = 0

for contour in filtered_contours:
    area = cv2.contourArea(contour)
    if area < 100:
        continue
    x, y, w, h = cv2.boundingRect(contour)
    roi = img[y:y + h, x:x + w]
    hsv_roi = cv2.cvtColor(roi, cv2.COLOR_BGR2HSV)
    if apple_lower[0] <= hsv_roi[:, :, 0].mean() <= apple_upper[0] and apple_lower[1] <= hsv_roi[:, :, 1].mean() <= \
            apple_upper[1] and apple_lower[2] <= hsv_roi[:, :, 2].mean() <= apple_upper[2]:
        apple_count += 1
        cv2.putText(img, 'Apple', (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)
    elif banana_lower[0] <= hsv_roi[:, :, 0].mean() <= banana_upper[0] and banana_lower[1] <= hsv_roi[:, :, 1].mean() <= \
            banana_upper[1] and banana_lower[2] <= hsv_roi[:, :, 2].mean() <= banana_upper[2]:
        banana_count += 1
        cv2.putText(img, 'Banana', (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)
    elif orange_lower[0] <= hsv_roi[:, :, 0].mean() <= orange_upper[0] and orange_lower[1] <= hsv_roi[:, :, 1].mean() <= \
            orange_upper[1] and orange_lower[2] <= hsv_roi[:, :, 2].mean() <= orange_upper[2]:
        orange_count += 1
        cv2.putText(img, 'Orange', (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)
    elif pear_lower[0] <= hsv_roi[:, :, 0].mean() <= pear_upper[0] and pear_lower[1] <= hsv_roi[:, :, 1].mean() <= \
            pear_upper[1] and pear_lower[2] <= hsv_roi[:, :, 2].mean() <= pear_upper[2]:
        pear_count += 1
        cv2.putText(img, 'Pear', (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)

print('There are', apple_count, 'apples.')
print('There are', banana_count, 'bananas.')
print('There are', orange_count, 'oranges.')
print('There are', pear_count, 'pears.')

# 显示结果
cv2.imshow('image', img)
cv2.waitKey(0)
cv2.destroyAllWindows()
