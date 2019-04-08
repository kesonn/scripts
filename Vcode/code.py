#coding=utf8

from PIL import Image

# 载入图片
im = Image.open('1.jpg')
# print im  # 打印出一个对象 <PIL.JpegImagePlugin.JpegImageFile image mode=RGB size=60x20 at 0x29D75F8>

# 图像的格式
print im.format # JPEG

# 图像点的格式
print im.mode # RGB和L

# 得到数据的尺寸
Width, Height = im.size
# print Width, Height # 60 20

# 显示图片
# im.show()

# 图像翻转
# im = im.transpose(Image.ROTATE_90)# 旋转90度

# 裁切图片
# cropImg = im.crop((0,0,20,20))
# cropImg.show()
# cropImg = im.crop((20,0,40,20))
# cropImg.show()

# 保存图片 保存是默认按后缀保存成对应的格式
im.save('new.bmp')
im2 = Image.open('new.bmp')
print im2.format # BMP


#因为干扰颜色太多，首先需要对图像进行去噪
def Binarized(Image,Threshold):
    '''
    用二分法做判别 处理每一个点
    :param Image:原始图片
    :param Threshold:阈值
    '''

    ImgNew = Image.crop()
    Pixels = ImgNew.load()
    (Width, Height) = ImgNew.size
    for i in range(Width):
        for j in range(Height):
            if Pixels[i, j] > Threshold: # 大于阈值的置为白色，否则黑色
                Pixels[i, j] = 255 # 白色
            else:
                Pixels[i, j] = 0 # 黑色
    return ImgNew

#切割，对图片研究发现，每幅图字符都是在20-30，40-50，60-70，80-90中。
#所以把图片切割就可以得到每个字符。
def get_x_data(im):
    imData=array(im)
    img_1=imData[:,20:30]
    img_2=imData[:,40:50]
    img_3=imData[:,60:70]
    img_4=imData[:,80:90]
    return  [img_1,img_2,img_3,img_4]


#上次得到了数据以后接下来就是用机器学习的方法来训练
from sklearn.neighbors import KNeighborsClassifier # 引入模型
from sklearn.cross_validation import cross_val_score
import matplotlib.pyplot  as plt

#核心代码
feature_all=array(feature_all)
feature_all = np.reshape(feature_all, (feature_all.shape[0], -1))
label_all=array(label_all)
lis_step=range(1,100,4)
# 得到模型
lis_score=[]
for i in lis_step:
    print i
    knn=KNeighborsClassifier(n_neighbors=i)
    scores=cross_val_score(knn,feature_all,label_all,cv=10,scoring="accuracy")
    lis_score.append(scores.mean())
plt.plot(lis_step,lis_score)
plt.show()

