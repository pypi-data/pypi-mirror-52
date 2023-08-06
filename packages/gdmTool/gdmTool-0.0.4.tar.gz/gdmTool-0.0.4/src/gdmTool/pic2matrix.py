#
# Used as a function for deep learning picture data transformation matrix
#
# partial release history:
# 2019-09-06 fl   Created
#
# Copyright (c) 2004-2019 by Cosmosource.  All rights reserved.
# Copyright (c) 2004-2019 by Yuan Gao.
#
# See the README file for information on usage and redistribution.


import numpy
import os
import cv2


def pic_transform(pic):
    """
    利用 PIL 包的 image方法 把图片转化数据
    :param pic: 图片路径
    :return: numpy矩阵
    """

    img = cv2.imread(pic)
    return img


def read(input_Path):
    """
    读取文件目录并返回数据集
    :param input_Path: 文件/文件夹目录
    :return: 数据集/标签集
    """

    # 定义返回的数组
    _files = []
    _labels = []
    # 递归读取文件夹下所有文件
    fileList = os.listdir(input_Path)
    for i in range(0, len(fileList)):
        path = os.path.join(input_Path, fileList[i])
        if os.path.isdir(path):
            _files.extend(read(path))
        if os.path.isfile(path):
            dataSet = pic_transform(path)
            _files.append(dataSet)
            # 将文件名作为标签,并拆分出来
            _labels.append(fileList[i].split('.')[0])
    # 以numpy的数据类型形式返回
    return numpy.array(_files), numpy.array(_labels)


def cut(dataSet, train_proportion, test_proportion, valid_proportion):
    """
    对已知整体数据集的切片,并返回为训练集,测试集,验证集
    :param dataSet: 整体数据集
    :param train_proportion: 训练集占比
    :param test_proportion: 测试集占比
    :param valid_proportion: 验证集占比
    :return:
    """

    # 数据的shuffle
    index_dex = numpy.random.permutation(dataSet.shape[0]).tolist()

    # 求数据集占比
    train_cut = int(len(index_dex) * train_proportion)
    test_cut = int(len(index_dex) * test_proportion)
    valid_cut = int(len(index_dex) * valid_proportion)

    # 数据集的分割
    train_index = index_dex[:train_cut]
    test_index = index_dex[train_cut:train_cut + test_cut]
    valid_index = index_dex[train_cut + test_cut:train_cut + test_cut + valid_cut]
    return train_index, test_index, valid_index