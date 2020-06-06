# -*- coding: utf-8 -*-
# Author zhang_wqin
# 2020 - 3 - 23

'''
建议说明:
    1. 本程序基本上没有处理异常，所以最好严格按照我的要求创建文件夹，文件,  否则，我也不知道会发生什么错误
    2. 文件夹名称中不能包含 '.' 否则会被认为是 某种文件， 
      eg.  'fold1 . a '在操作系统看来，是一个正常的文件夹名称，但是在本程序不是正确的文件夹名称 
      
    3. Classifier() 构造函数要提供两个必须参数， 
       1) dir_path : 指明数据的存储路径
       2) modified ： 由于用户可以在img 文件夹下，自行添加新人物，
            所以必须指明自己有没有修改过 img 文件夹下的图片，包括添加，删除，重命名, ...
            modified = True, 表明已经修改过，程序就要重新训练
            modified = False, 就可以直接读 原来的模型，暂时不用训练
        modified 信息，用户必须 如实填写
     **** [modified ] 信息最好写成 False, 因为我好像没有写 modified == True 时候的处理代码
        
     4. 程序运行期间，用户可以通过按键 
       q:  [quit]  退出程序，程序会以文件的形式 保存相应的信息
       a:  [add]  添加新人物，包括输入姓名，程序自动截取10张图片 留作训练数据
       d:  [delete] 删除某一人物的所有信息记录
       t:  [train] 训练模型
       
       [add], [delete] 时，要求屏幕中暂时只能有一个人，用于添加，删除此人
       其他时刻，允许有多个人出现，并识别出多个人的名字
       
    5. 
        
 '''

import os
from sys import exit
import cv2
import numpy as np
import time

"""
    dir_path 是一个文件夹的路径，该文件必须包含以下子文件夹


     dir_path |
              |- img
              |    |-- P1     
              |    |    | p1_0.png
              |    |    | p1_1.png
              |    |    | ...
              |    |  
              |    |-- P2
              |    |   | p2_0.png
              |    |   | p2_1.png
              |    |   | ...
              |    |
              |    |-- P3
              |
              |             
              |- config.txt
              |- ...
"""

class Classifier(object):
    def __init__(self, dir_path, modified):
        self.dir_path = dir_path
        self.modified = modified
        self.person = 1
        self.names = ['?']
        self.faces, self.labels = [], []
        self.img_folder = []
        
        self.no_data = True
        self.img_dir = ''
        self.new_path = ''
        self.new_name = ''
        self.DELETE = False   # 标记是否被删除过，用于最后退出时，要不要保存数据
        self.ADD = False
        
        self.face_recognizer = None
        
        
        
        self.isfile()
        #self.load_names()
        self.load_imgs()
        self.train_model()
        
    
        """
        functions:
            1. isfile() 根据获取的路径，读取该路径下所有的子文件夹以及子文件，
                     如果不存在，则创建必要的子文件夹img，和某些文件 config.txt，
                     config.txt 在程序退出时保存当前 已知道的人名
                     
            2. load_names()  从config.txt 文件中读取
            
            3. load_imgs()  从img 文件夹中读取人脸图像
            
            4.
            
            5.
            
            6.
          
        """

    '''#1 读取给定的文件夹中的 文件夹，文件列表 '''
    def isfile(self):
        if os.path.exists(self.dir_path):
            
            list = os.listdir(self.dir_path)
            self.files = [x for x in list if '.' in x]
            self.folds = [x for x in list if x not in self.files]
            
            # 判断是否存在 img 文件夹， 不存在则 创建 img 
            if 'img' not in self.folds:
                path = os.path.join(self.dir_path, 'img')
                print('create ','folder "img" in [',self.dir_path,']')
                os.mkdir(path)
            
                    
            # 判断是否存在config.txt 文件, 不存在则 创建 config.txt
            #第一次运行，不存在文件，创建文件, 然后写入一个 'unknown' 项目
            if 'config.txt' not in self.files:
                path = os.path.join(self.dir_path, 'config.txt')
                print('create ','config.txt in [',self.dir_path,']')
                f = open(path,mode = 'w+')
                f.close()
            
            # 记录一下img_dir, 以及img 中的子文件夹， 方便后续使用
            self.img_dir = os.path.join(self.dir_path, 'img')
            self.img_folder = os.listdir(self.img_dir)
        else:
            print('Must provide an empty folder exists in your disk')
            exit(0)

    
    
    '''# 2 读取文件, 获取人名信息， 人名信息在 config.txt 文件中 '''
    def load_names(self):
       path = os.path.join(self.dir_path, 'config.txt')
       
       if os.path.exists(path):
           #存在此文件，读取文件
           try:
               with open(path,mode = 'r',encoding='utf-8') as f:
                   for line in f.readlines():                   
                       self.names.append(line.strip())
                   self.person = len(self.names) - 1
                   f.close()
           except Exception as e:
               print(e)
           
           

    ''' #3  读取人图像信息  '''  
    def load_imgs(self):
        #  img 文件夹为空， 直接结束
        if len(self.img_folder) == 0:
            self.no_data = True
            return 
        
        # img 文件夹 存在子文件夹。每一个子文件夹，表示一个人的相片集
        else:
            for folder in self.img_folder:
                fpath = os.path.join(self.img_dir, folder)
                
                # 读入10 张图片
                for i in range(10):
                    img = cv2.imread(fpath + '\\' + str(i) + '.png', cv2.IMREAD_GRAYSCALE)
                    #print(type(img))
                    self.faces.append(img)
                    self.labels.append(self.person)
                
                # 人数 +1， 将名字加入 self.name 
                self.person += 1
                self.names.append(folder)
            self.no_data = False


    # 训练样本， 返回一个人脸分类器
    def train_model(self):      
        #  没有训练数据，就应该退出
        if self.no_data == True:
            self.face_recognizer = None
            return 
              
        #创建一个 LBPH人脸分类器 
        face_recognizer = cv2.face.LBPHFaceRecognizer_create()
        
        # 开始训练计时
        print('Training.....')
        time_start=time.time()
        
        # 训练
        face_recognizer.train(self.faces, np.array(self.labels))
        
        # 训练结束计时
        time_end=time.time()
        print("Train over")
        print('totally cost ',time_end - time_start, ' seconds')
        
        # 返回训练好的模型
        print('we have trained ', self.names)
        self.face_recognizer = face_recognizer
        
    
    def save(self):
        # 判断是不是被修改过,如果被修改过
        if self.ADD or self.DELETE:
            path = os.path.join(self.dir_path, 'config.txt')
            
            with open(path,mode = 'w+',encoding='utf-8') as f:
                for name in self.names:                   
                    f.write(name+'\n')
                f.close()
            print('save successfully')



    def add(self):
        print('Insert a new record   ing...')
        
        name = str(input("Tell me your name, for example 'Tom', type 'can' to cancel: "))
        if name == 'can':
            print('Add failed: you have canceled this operation')
            return False
        
        # 如果名字已经存在，循环
        while name in self.img_folder:
            name = str(input("this name was occupied already, please try a new one, type 'can' to cancel: "))
            if name == 'can':
                print('Add failed: you have canceled this operation')
                return False

             
        path =  os.path.join(self.img_dir, name)
        os.mkdir(path)
        
        self.new_path = path+'\\'
        self.new_name = name
        self.names.append(name)  # 加入 该名字
        self.img_folder.append(name)
        # 是不是要加入 self.face, 再说
        
        print(' hello, ', name, ', we will snapshot 10 pictures for you')    
        self.ADD = True
        self.no_data = False
        return True
        

        
    def delete(self):
        print('Delete a  record   ing...')
        
        name = str(input("Tell me the name you want to delete, type 'can' to cancel: "))
        if name == 'can':
            return False
        
        # 如果该名字 不存在， 循环
        while name not in self.img_folder:
            name = str(input("this name not exists, please try again, type 'can' to cancel: "))
            if name == 'can':
                return False
        
        path = self.img_dir + '\\' + name
        
        # 先删除该文件夹下的所有文件， 再删除该文件夹
        ls = os.listdir(path)
        for i in ls:
            c_path = os.path.join(path, i)
            os.remove(c_path)
        os.removedirs(path)
        
        self.names.remove(name) #删除 该名字
        # 是不是要删除 self.face, 再说
        
        self.DELETE = True
        return True


if __name__ == '__main__':
    dir_path = r'E:\AI face recognition\test'
    demo = Classifier(dir_path, False)
    print('folers ',demo.folds)
    print('img_folders ',demo.img_folder)

    print(demo.names)
    print(demo.labels)
    
    demo.add()
