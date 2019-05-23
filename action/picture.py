# coding:utf-8
# 作者：    Han Sanyang
# 创建时间：2019/3/12 16:23
# 文件名：  picture


from PIL import Image
import math
import operator
from functools import reduce

class Picture():
    def __init__(self):
        pass

    def similarity(self, s, r):

        image1=Image.open(s)
        image3=Image.open(r)
        #把图像对象转换为直方图数据，存在list h1、h2 中
        h1=image1.histogram()
        h2=image3.histogram()

        result = math.sqrt(reduce(operator.add,  list(map(lambda a,b: (a-b)**2, h1, h2)))/len(h1) )
        '''
        sqrt:计算平方根，reduce函数：前一次调用的结果和sequence的下一个元素传递给operator.add
        operator.add(x,y)对应表达式：x+y
        这个函数是方差的数学公式：S^2= ∑(X-Y) ^2 / (n-1)
        '''
        print(result)
        return result
