#!/usr/bin/env python
# -*- coding: utf-8 -*-
from numpy import *
import operator
from os import listdir

def ImgToVetcor(filename):
	mat=zeros((1,1024))
	fr=open(filename)
	for i in range(32):
		lineStr=fr.readline()
		for j in range(32):
			mat[0,32*i+j]=int(lineStr[j])
	return mat
def KNN(inputMat,trainingMat,Labels,Knumber):
	trainingLength=trainingMat.shape[0]#它的功能是读取矩阵的长度，比如shape[0]就是读取矩阵第一维度的长度 获取有多少行 #tile 沿各个维度重复的次数
	diffMat = tile(inputMat, (trainingLength,1)) - trainingMat
	#print diffMat
	#得到差值数组
	sqDiffMat=square(diffMat)
	#sqDiffMat = diffMat**2
	#差值数组求平方
	sqDistances = sqDiffMat.sum(axis=1) #axis=0, 表示列。axis=1, 表示行。行相加　已经变成一列了
	#print sqDistances
	distances =sqrt(sqDistances) #开平方
	sortedDistIndicies = distances.argsort() #升序排列　返回的是位置而不是数组值的大小
	classCount={}
	for i in range(Knumber):
		voteIlabel = Labels[sortedDistIndicies[i]]
		classCount[voteIlabel] = classCount.get(voteIlabel,0) + 1 #得到指定键的值　如果没有返回后面的默认值
	#print classCount
	sortedClassCount = sorted(classCount.iteritems(), key=operator.itemgetter(1), reverse=True)
	#iteritems() 键值对儿　 / key=operator.itemgetter(1) 定义函数key，获取对象的第1个域的值 按照第几个进行排序　 reverse=True降序排列
	return sortedClassCount[0][0]
	 
	 
	
hwLabels=[] #初始化ｌａｂｅｌ数组　用来存储标签
trainingFileList = listdir('trainingDigits') # 获得当前目录中的内容 文件名 这是个数组
#print trainingFileList
FileNumbers=len(trainingFileList)#文件数量
trainingMat=zeros((FileNumbers,1024)) #创建Ｍ行１０２４列空二维数组
for i in range(FileNumbers):
	fileNamestr=trainingFileList[i]
	fileStr=fileNamestr.split('.')[0] 
	#Python split()通过指定分隔符对字符串进行切片，如果参数num 有指定值，则仅分隔 num 个子字符串
	#这是为先去除下划线 并得到前面部分的字符串
	classNumstr=int(fileStr.split('_')[0]) #这次得到了数字
	hwLabels.append(classNumstr) #添加到ｌａｂｅｌ数组
	trainingMat[i,:]=ImgToVetcor('trainingDigits/%s'%fileNamestr)

testFileList = listdir('testDigits')
TestNumber=len(testFileList)

for i in range(20):
	fileNameStr = testFileList[i]
	fileStr = fileNameStr.split('.')[0]     #take off .txt
	classNumStr = int(fileStr.split('_')[0])
	vectorUnderTest = ImgToVetcor('testDigits/%s' % fileNameStr)
	classifierResult = KNN(vectorUnderTest, trainingMat, hwLabels, 3)
	print "the classifier came back with: %d, the real answer is: %d" % (classifierResult, classNumStr)

fileNameStr = testFileList[45]
fileStr = fileNameStr.split('.')[0]     #take off .txt
classNumStr = int(fileStr.split('_')[0])
vectorUnderTest = ImgToVetcor('testDigits/%s' % fileNameStr)
#print shape(trainingMat)
classifierResult = KNN(vectorUnderTest, trainingMat, hwLabels, 40)
print "the classifier came back with: %d, the real answer is: %d" % (classifierResult, classNumStr)


