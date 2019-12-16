# coding=utf-8
import caffe
import numpy as np


def LikeValue(v1, v2):
    #return np.dot(v1, v2) / (np.linalg.norm(v1) * np.linalg.norm(v2))
    inA=np.mat(v1)
    inB=np.mat(v2)
    num=float(inA*inB.T)
    denom=np.linalg.norm(inA)*np.linalg.norm(inB)
    return 0.5+0.5*(num/denom)


class SingleFace(object):
    # 人的名字
    label = object()

    # 截取人脸后的图像
    roi = object()

    # 人脸中提取的特征向量
    feature = object()


class YotoFace(object):
    def __init__(self):
        # 设置为仅cpu模式
        # caffe.set_mode_cpu()

	caffe.set_mode_gpu()
	caffe.set_device(0)
        # 初始化Net
        self.net = caffe.Net("face_deploy.prototxt", "face_model.caffemodel", caffe.TEST)
        # 均值
        self.avg = np.array([129.1863, 104.7624, 93.5940])
        # 众多的singleface
        self.facearray = []

    # 提取特征值的函数
    def ExtractFeature(self, img_224):
        img_1 = img_224 - self.avg  # subtract mean (numpy takes care of dimensions :)
        img_1 = img_1.transpose((2, 0, 1))

        img_1 = img_1 / 255
        img_1 = img_1[None, :]  # add singleton dimension

        out_1 = self.net.forward(data=img_1)
        caffe_fc8_1 = self.net.blobs['fc5'].data[0]
        # test = out_1['prob'][0]

        return caffe_fc8_1

    # 由图片和label生成SingleFace
    def Generate(self, input_224, label):
        # 提取特征值
        feature_ = self.ExtractFeature(input_224)
        if feature_ is None:
            return False

        # 检查该用户是否已经存在
        for face in self.facearray:
            if label == face.label:
                return False

        # 注册
        #new = SingleFace()
        #new.label = label
        #new.feature = feature_.copy()
        #new.roi = input_224
        #self.facearray.append(new)
        return True

    # 识别
    def Recognition(self, input_224):

	self.facearray=[]        
	# 要对比的脸的特征值
        single = self.ExtractFeature(input_224).copy()
        # 保存相似度的list
        like_array = []
	username=open("./user_data/user_name.txt","r")
	for name in username:
	    name=name.strip('\r\n')
	    user_face_path="./user_data/user_image/"+name+".npy"
	    user_face=np.load(user_face_path)
	    face_feature=self.ExtractFeature(user_face)
        # 判断当前的脸和现有的脸的相似度
	    print(LikeValue(single, face_feature))
            like_array.append(LikeValue(single, face_feature))
	    # 注册
            new = SingleFace()
            new.label = name
            #new.feature = user_feature
            #new.roi = user_face
            self.facearray.append(new)
	username.close()
        biggest = np.argmax(like_array)
        if like_array[biggest] < 0.83:
            return False, None
        else:
            return True, biggest
