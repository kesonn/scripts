#coding=utf8
from PIL import Image
img_path = 'C:/Users/Administrator/Desktop/vcodes/im/18410.png'
image = Image.open(img_path)

image = image.convert('L')  # 转化为灰度图

def get_bin_image(image,shold=130):
    #二值化  shold 是颜色临界值
    table = []
    for i in range(255):
        if i < shold:
            table.append(0)
        else:
            table.append(1)
    return image.point(table, '1')


def get_crop_imgs(img):
    """
    按照图片的特点,进行切割,这个要根据具体的验证码来进行工作. # 见原理图
    :param img:
    :return:
    """
    child_img_list = []
    for i in range(4):
        x = 2 + i * (6 + 4)  # 见原理图
        y = 0
        child_img = img.crop((x, y, x + 6, y + 10))
        child_img_list.append(child_img)

    return child_img_list