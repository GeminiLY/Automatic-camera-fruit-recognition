import os
import sys
import cv2
import time
import zipfile
import datetime
import schedule
import mimetypes
import numpy as np
from smtplib import SMTP_SSL                    # SSL加密的   传输协议
from email import encoders
from email.mime.text import MIMEText            # 构建邮件文本
from email.mime.base import MIMEBase            # 构建邮件附件
from email.mime.multipart import MIMEMultipart  # 构建邮件体
from email.header import Header                 # 发送内容


# 开机自启动需要 等一会不然会报错（可能是开机没联网）
# time.sleep(60)


# 调用摄像头拍摄照片
def get_photo():
    # 开启摄像头
    capture = cv2.VideoCapture(0)
    cap = cv2.VideoCapture(1, cv2.CAP_DSHOW)
    # 设置分辨率
    cap.set(3, 1920)
    cap.set(4, 1080)
    # 获取当前时间
    now_time = datetime.datetime.now()
    timeStr = datetime.datetime.strftime(now_time, '%Y_%m_%d_%H_%M')
    # 将摄像头中的一帧图片数据保存
    f, frame = cap.read()
    # 设置照片文件名
    photo_name = timeStr + ".jpg"
    # 获取脚本所在目录
    now_dir = sys.path[0]
    # 将图片保存为本地文件
    cv2.imwrite(now_dir + "/images/" + photo_name, frame)
    # 关闭摄像头
    cap.release()

    # # 获取前一张照片的文件名
    # time_detail = timeStr.split("_")
    # if time_detail[4] == "00":
    #     time_detail[3] = str(int(time_detail[3]) - 1)
    #     time_detail[4] = "50"
    # else:
    #     time_detail[4] = str(int(time_detail[4]) - 10)
    # earlier_photo = "_".join(time_detail) + ".jpg"

    # # load images
    # image1 = cv2.imread(earlier_photo)
    # image2 = cv2.imread(photo_name)

    # # compute difference
    # # method_1
    # difference = cv2.subtract(image1, image2)
    # # method_2
    # difference = image1.copy()
    # cv2.absdiff(image1, image2, difference)
    #
    # cv2.imwrite('diff.png', difference)


# 检查网络，断网重启wifi
def restart_wifi():
    status = os.system("ping -w 3 www.baidu.com")
    if status == 1:
        # 关闭wifi
        os.system('sudo ip link set wlan0 down')
        # 开启wifi
        os.system('sudo ip link set wlan0 up')
    else:
        print('已经连上网了')
    return status


# 将文件夹压缩成zip
def make_zip(source_dir, output_filename):
    zipf = zipfile.ZipFile(output_filename, 'w')
    pre_len = len(os.path.dirname(source_dir))
    for root, dirnames, files in os.walk(source_dir):
        for file in files:
            print(file)
            pathfile = os.path.join(root, file)
            arcname = pathfile[pre_len:].strip(os.path.sep)  # 相对路径
            zipf.write(pathfile, arcname)
    zipf.close()


# 把图片文件发送到我的邮箱
def send_message(filepath):
    # 选择QQ邮箱发送照片
    host_server = 'smtp.qq.com'  # QQ邮箱smtp服务器
    pwd = 'wvusupfgrqkhgeac'  # 授权码
    from_qq_mail = '1515298555@qq.com'  # 发件人
    to_qq_mail = '1515298555@qq.com'  # 收件人
    msg = MIMEMultipart()  # 创建一封带附件的邮件

    msg['Subject'] = Header('摄像头照片', 'UTF-8')  # 消息主题
    msg['From'] = from_qq_mail  # 发件人
    msg['To'] = Header("YH", 'UTF-8')  # 收件人
    msg.attach(MIMEText("照片数据", 'html', 'UTF-8'))  # 添加邮件文本信息

    # 加载附件到邮箱中
    data = open(filepath, 'rb')
    ctype, encoding = mimetypes.guess_type(filepath)
    if ctype is None or encoding is not None:
        ctype = 'application/octet-stream'
    maintype, subtype = ctype.split('/', 1)
    file_msg = MIMEBase(maintype, subtype)
    file_msg.set_payload(data.read())
    data.close()
    # 把附件编码
    encoders.encode_base64(file_msg)
    # 修改附件名称
    file_msg.add_header('Content-Disposition', 'attachment', filename="data.zip")
    msg.attach(file_msg)

    # 开始发送邮件
    smtp = SMTP_SSL(host_server)  # 链接服务器
    smtp.login(from_qq_mail, pwd)  # 登录邮箱
    smtp.sendmail(from_qq_mail, to_qq_mail, msg.as_string())  # 发送邮箱
    smtp.quit()  # 退出


def del_files():
    now_dir = sys.path[0]
    # 删除压缩包
    os.remove("images.zip")
    # 删除照片
    test_path = now_dir + "/images/"
    for root, dirs, files in os.walk(test_path):
        for name in files:
            if name.endswith(".jpg"):  # 指定要删除的格式，这里是jpg 可以换成其他格式
                os.remove(os.path.join(root, name))


# 创建定时
def start():
    schedule.every().hours.do(get_photo)  # 每小时运行一次


schedule.every().day.at("21:37").do(start)
# 如果方法需要传参的话do(func,参数1)

# schedule.every(1).day.at("20:48").do(get_photo)
# schedule.every().hours.do(get_photo)
# schedule.every(1).day.do(make_zip, "images", "images.zip")
# schedule.every(1).day.do(send_message, "images.zip")
# schedule.every(1).day.do(del_files)

# 开循环
while True:
    schedule.run_pending()
    time.sleep(1)
    now_time = datetime.datetime.now()
    timeStr = datetime.datetime.strftime(now_time, '%H_%M')
    if timeStr == "21_38":
        break

cv2.destroyAllWindows()

make_zip("images", "images.zip")
send_message("images.zip")
del_files()
