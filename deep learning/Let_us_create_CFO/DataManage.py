# -*- coding: UTF-8 -*-
import numpy as np
import os
from os.path import join
import csv

class DataMange(object):
    id = '0'
    def __init__(self):
        self.description = str(1024)
        self.id = str(1024)
        self.class_ = str(1024)
        self.file_path_now = str(1024)
        self.info_str = str(1024)


    # 创建csv目录


    def save(self):
        if self.description == str(1024) or self.id == str(1024) or self.class_ == str(1024) or self.file_path_now == str(1024):
            return False
        else:
            (dirname, filename) = os.path.split(self.file_path_now)
            idx = np.where(self.info_str[:, 1] == filename)
            self.info_str[idx[0], 0] = self.id
            self.info_str[idx[0], 2] = self.class_
            self.info_str[idx[0], 3] = self.description

            with open(join('label', str(self.id) + '.csv'), 'w', encoding="utf-8") as f:
                f.write('id, video name, video class, description\n')

            with open(join('label', str(self.id) + '.csv'), 'a', encoding="utf-8") as f:
                for i in range(len(self.file_list)):
                    f.write(self.info_str[i, 0] + ',' + self.info_str[i, 1] + ',' + self.info_str[i, 2] + ',' +
                            self.info_str[i, 3] + '\n')
        return True


    def set_description(self, description):
        self.description = description
        pass

    # 载入数据
    def file_data_now(self, file_path):
        self.file_path_now = file_path
        (dirname, filename) = os.path.split(file_path)
        self.file_list = [x for x in os.listdir(dirname) if is_image_file(x)]
        # 创建文件信息
        if not os.path.exists(join('label', str(self.id) + '.csv')):
            self.info_str = np.asarray(self.file_list, np.str)
            self.info_str = self.info_str[:, np.newaxis]
            id = (np.ones_like(self.info_str, np.int16) * 1024).astype(np.str)
            dis = (np.ones_like(self.info_str, np.int16) * 1024).astype(np.str)
            cla = (np.ones_like(self.info_str, np.int16) * 1024).astype(np.str)
            self.info_str = np.concatenate([id, self.info_str, cla, dis], axis=1)
        else:
            self.info_str = np.loadtxt(join('label', str(self.id) + '.csv'), dtype=np.str, delimiter=',')[1:]
        (dirname, filename) = os.path.split(self.file_path_now)
        idx = np.where(self.info_str[:, 1] == filename)
        self.class_ = self.info_str[idx[0], 2][0]
        self.description = self.info_str[idx[0], 3][0]
        pass

    # 下一个视频
    def file_next(self):
        (dirname, filename) = os.path.split(self.file_path_now)
        index = self.file_list.index(filename)
        self.file_path_now = join(dirname, self.file_list[index+1])

        (dirname, filename) = os.path.split(self.file_path_now)
        idx = np.where(self.info_str[:, 1] == filename)
        self.class_ = self.info_str[idx[0], 2][0]
        self.description = self.info_str[idx[0], 3][0]

        return self.file_path_now
    #上一个视频
    def file_pre(self):
        (dirname, filename) = os.path.split(self.file_path_now)
        index = self.file_list.index(filename)
        self.file_path_now = join(dirname, self.file_list[index-1])
        (dirname, filename) = os.path.split(self.file_path_now)
        idx = np.where(self.info_str[:, 1] == filename)
        self.class_ = self.info_str[idx[0], 2][0]
        self.description = self.info_str[idx[0], 3][0]
        return self.file_path_now
    # 获取视频列表
    def get_file_list(self):
        if self.file_list != None:
            return self.file_list
        else:
            print('There is no file list')
            return
    # 设置分类
    def set_class(self, class_):
        self.class_ = class_

    # 设置分类
    def get_class(self):
        return self.class_

    def set_id(self, id):
        self.id = id

    def get_id(self):
        return self.id
def is_image_file(filename):
    return any(filename.endswith(extension) for extension in [".mp4"])