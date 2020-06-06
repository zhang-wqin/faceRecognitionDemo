# -*- coding: utf-8 -*-

from Classifier import *
import cv2 


path = r'E:\AI_face_recongnition_demo'
# 自行提供一个空目录,必须已经存在

demo = Classifier(path, False)


TRAINED = False

if demo.face_recognizer != None:
    TRAINED = True
    print("face_recognition is Trained")


face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades+'haarcascade_frontalface_default.xml')
cap = cv2.VideoCapture(0)

ADD, DELETE, QUIT = False, False, False
cnt, pic = 1, 0


if __name__ == '__main__':
    while(True):
        ret, frame = cap.read() 
        
        faces = face_cascade.detectMultiScale(frame, 1.2, 2)
        img = frame
        
        
        for (x,y,w,h) in faces:
            # 找到人脸的区域
            face_area = img[y:y+h, x:x+w]
            
            # 添加新人物
            if ADD == True:
                #if cnt < 11 这样截取的10张图基本是连续的，换一种方式
                if cnt%10 == 9:
                    cv2.imwrite(demo.new_path+str(pic)+'.png', face_area)
                    demo.faces.append(cv2.cvtColor(face_area, cv2.COLOR_BGR2GRAY))
                    demo.labels.append(demo.person)
                    print("Done for No.", pic, " pictures", 'cnt = ',cnt)
                    pic += 1
                    
                    if pic == 10:
                        cnt, pic, ADD = 1, 0, False
                        demo.person += 1
                        print('add successfully')
                        print('-'*30)
                        break                 
                cnt += 1
                break
                    
            
            if TRAINED == True:
                # 预测该用户是谁
                gray_face_area = cv2.cvtColor(face_area, cv2.COLOR_BGR2GRAY)
                label, confidence = demo.face_recognizer.predict(gray_face_area)
                confidence = round(confidence, 3)
                
                # 画出矩形框
                cv2.rectangle(img, (x, y), (x+w, y+h), (0, 255, 0), 2)
                
                '''
                #画出名字
                if confidence > 40:
                    text = str(label)+demo.names[label] + str(confidence)  
                else:
                    text = str(label)+demo.names[0] + str(confidence)
                '''
                 #画出名字
                if label != 0 and confidence > 25:
                    text = str(label)+demo.names[label] + str(confidence)  
                else:
                    text = str(label)+demo.names[0] + str(confidence)
                
                
                cv2.putText(img, text, (x, y), cv2.FONT_HERSHEY_DUPLEX, 2, (0, 255, 0), 2, 3)
        
        cv2.imshow('frame2',img)
            
        # 检测操作
        char = cv2.waitKey(50) & 0xFF
        if char == ord('q'):
            # 先保存已有的数据
            #demo.save()
            #exit(0)
            break
        elif char == ord('t'):
            if demo.no_data == True:
                print('Error: no data, please add some train imgs first')
                continue
            
            demo.train_model()
            TRAINED = True
            continue
        
        elif char == ord('a'):
            # 添加新人物          
            ADD = demo.add()
            print(ADD)
            continue
         
        # 此功能不完善，最好不要使用, 会报错[list out of range]
        elif char == ord('d'):
            ## 删除已有的人物记录
            DELETE = demo.delete()
            
            if DELETE == True:
                print('delete successfully')
            else:
                print('Delete failed: you have canceled this operation')
            continue

# 最后，关闭所有窗口
cap.release()
cv2.destroyAllWindows()
