import numpy as np
#学習データ読み込み
filename = 'C:/lib/LeapSDK/build/data_gu.csv'
raw_data = open(filename, 'r')
data_gu = np.loadtxt(raw_data, delimiter=",")

filename = 'C:/lib/LeapSDK/build/data_tyoki.csv'
raw_data = open(filename, 'r')
data_tyoki = np.loadtxt(raw_data, delimiter=",")

filename = 'C:/lib/LeapSDK/build/data_pa.csv'
raw_data = open(filename, 'r')
data_pa = np.loadtxt(raw_data, delimiter=",")

#ラベル付け
labels_size = (1000,1)
labels_gu = np.random.randint(1, 2, size=labels_size)
labels_tyoki = np.random.randint(2, 3, size=labels_size)
labels_pa = np.random.randint(3, 4, size=labels_size)

#配列の合体
data = np.vstack([data_gu,data_tyoki])
data = np.vstack([data,data_pa])
labels = np.vstack([labels_gu,labels_tyoki])
labels = np.vstack([labels,labels_pa])

#knn読み込み
import cv2
knn = cv2.ml.KNearest_create()
knn.train(data.astype(np.float32), cv2.ml.ROW_SAMPLE, labels.astype(np.float32))

import sys
import statistics

#k近傍法の実行
def reading():
    line = sys.stdin.readline()
    line = line.rstrip().split()  
    if not (len(line) == 0):
        newdata = np.array(list(map(float, line))).reshape((1, 5))
        newdata = newdata.astype(np.float32)
        ret, results, neighbours, dist = knn.findNearest(newdata, 1211)
        return results[0]

#flagからメッセージを出力する        
def command(a, i):
#iはflagの数
    if i == 1:
        if a[0] == 1:
            print("*****OK!*****\n")
        if a[0] == 2:
            print('*****ありがとう!*****\n')
    elif i == 2:
        if a[0] == 1 and a[1] == 2:
            print('*****後で連絡します。*****\n')
        elif a[0] == 2 and a[1] == 1:
            print('*****いいね～～*****\n')
        else:
            print('コマンドが設定されていません\n')
    else:
        print('コマンドが設定されていません\n')

#最頻値        
def mode(labelkeep):
    i = 0
    while True:
        try :    
            mode = statistics.mode(labelkeep)
        except TypeError:
            labelkeep[i] = reading()
            i = (i + 1)%50
            continue
        else:
            break
    return mode   

#flag グ→チョキ=break グ→パ=1 チョキ→グ=0 チョキ→パ=0 パ→グ=2 パ→チョキ=break
while True:
    fflag = np.array([0]*10)   
    labelkeep = np.array([0]*50)
    #labelkeepの初期化
    t = 0
    while t < 50:
        labelkeep[t] = reading()
        t += 1
        
    oldlabel = mode(labelkeep)  
    i = 0
    while True:
        j = 0
        while j < 49:
            labelkeep[j] = labelkeep[j+1]
            j += 1
        labelkeep[49] = reading()
        newlabel = mode(labelkeep)
        if oldlabel == newlabel:
            flag = 0
        else:
            #グー
            if oldlabel == 1:
                if newlabel == 2:
                    break
                elif newlabel == 3:
                    flag = 1
            #チョキ
            elif oldlabel == 2:
                if newlabel == 1:
                    flag = 0
                elif newlabel == 3:
                    flag = 0
            #パー
            elif oldlabel == 3:
                if newlabel == 1:
                    flag = 2
                elif newlabel == 2:
                    break
        if not (flag == 0):
            fflag[i] = flag
            print(fflag[i])
            i = i + 1
        oldlabel = newlabel
        
    command(fflag, i)