import sys
import cv2
from matplotlib import pyplot as plt
import numpy as np
from scipy.spatial import distance
import os
from scipy.ndimage import label
from sklearn.metrics import f1_score

def segment_on_dt(a, img):
    border = cv2.dilate(img, None, iterations=5)
    border = border - cv2.erode(border, None)

    dt = cv2.distanceTransform(img, 2, 3)
    dt = ((dt - dt.min()) / (dt.max() - dt.min()) * 255).astype(np.uint8)

    _, dt = cv2.threshold(img,50,100,cv2.THRESH_BINARY+cv2.THRESH_OTSU)
    #_, dt = cv2.threshold(dt, 120, 205, cv2.THRESH_BINARY)
 
    lbl, ncc = label(dt) # conta quantas regioes diferentes foram achadas na imagem de threshold
    count = 0
    somas = []

    lbl = lbl * (255/ (ncc + 1))    # Completing the markers now. 
    lbl[border == 255] = 255
    
    lbl = lbl.astype(np.int32)
    cv2.watershed(a, lbl)
    
    lbl = lbl.astype(np.uint8)
    return 255 - lbl

def main():
    p = ["01", "02", "03", "04", "05", "06", "07", "08", "09", "10", "11", "12", "13", "14", "15", "16", "17", "18"] #lista de pacientes (string)


    #inicializa o path de todas as imagens
    patients = []
    slices = []
    for i in p:
        dir = "./slices_Pat" + i
        slices.append(len(os.listdir(dir+ "/sistole")))
        images = []
        for j in range(0, slices[int(i)-1]):
            image = []
            image.append(dir+"/sistole/Pat" + i + "_sistole_slice" + str(j) +".pgm")
            image.append(dir+"/diastole/Pat"+ i + "_diastole_slice" + str(j) +".pgm")
            images.append(image)
        patients.append(images)

    expert1 = []
    slices = []
    for i in p:
        dir = "./slices_Pat" + i
        slices.append(len(os.listdir(dir+ "/sistole")))
        images = []
        for j in range(0, slices[int(i)-1]):
            image = []
            image.append(dir+"/experts/Pat" + i + "_sistole_expert1" + str(j) +"_endo.pgm")
            image.append(dir+"/experts/Pat" + i + "_diastole_expert1" + str(j) +"_endo.pgm")
            images.append(image)
        expert1.append(images)


    expert2 = []
    slices = []
    for i in p:
        dir = "./slices_Pat" + i
        slices.append(len(os.listdir(dir+ "/sistole")))
        images = []
        for j in range(0, slices[int(i)-1]):
            image = []
            image.append(dir+"/experts/Pat" + i + "_sistole_expert2" + str(j) +"_endo.pgm")
            image.append(dir+"/experts/Pat" + i + "_diastole_expert2" + str(j) +"_endo.pgm")
            images.append(image)
        expert2.append(images)



    #abre todas as imagens no opencv na variavel IMG
    #ordenado por img[n_paciente][n_corte][sistole ou diastole]
    img  =  []
    for i in range(0, len(patients)):
        images = []
        for j in range(0, len(patients[i])):
            image = [cv2.imread(file,0) for file in patients[i][j]]
            images.append(image)
        img.append(images)


    #abre todas as imagens no opencv na variavel experts
    #ordenado por experts[expert 1 ou 2][n_paciente][n_corte][sistole ou diastole]

    experts1  =  []
    for i in range(0, len(expert1)):
        images = []
        for j in range(0, len(expert1[i])):
            image = [cv2.imread(file,0) for file in expert1[i][j]]
            images.append(image)
        experts1.append(images)


    experts2  =  []
    for i in range(0, len(expert2)):
        images = []
        for j in range(0, len(expert2[i])):
            image = [cv2.imread(file,0) for file in expert2[i][j]]
            images.append(image)
        experts2.append(images)


    experts = [experts1, experts2]


    for pat in range(len(img)):
        for corte in range(len(img[pat])):
            for i in range(0,2): #teste = img[pat][corte][0 ou 1]
                teste = img[pat][corte][i]
                img_gray = teste
                teste = cv2.cvtColor(teste,cv2.COLOR_GRAY2BGR)
                #computa imagem binaria pra ajudar a segmentacao
                _, img_bin = cv2.threshold(img_gray, 0, 255,
                        cv2.THRESH_OTSU)
                #faz a abertura para remover ruidos
                img_bin = cv2.morphologyEx(img_bin, cv2.MORPH_OPEN,
                        np.ones((3, 3), dtype=int))
                #calcula os componentes
                result = segment_on_dt(teste, img_bin)


                #calcula a distancia euclidiana entre cada componente e o centro da imagem
                cx = (len(teste)/2)-1
                cy = (len(teste[0])/2)-1
                menor = 999999
                mx = cx
                my = cy
                if result[cx][cy] == 0:
                    for x in range(len(result)):
                        for y in range(len(result[0])):
                            if result[x][y] != 0:
                                dist = distance.euclidean((cx, cy), (x, y))
                                if menor > dist:
                                    mx = x
                                    my = y
                                    menor = dist

                #deixa apenas o componente mais proximo do centro na imagem, e deixa os outros pintados de preto
                teste[result != result[mx][my]] = 0
                teste[result == result[mx][my]] = 255
                teste = cv2.cvtColor(teste,cv2.COLOR_BGR2GRAY)
                #salva o calculo do endocardio no proprio vetor de imagens
                img[pat][corte][i] = teste


    # calcula f_score pra 1 expert
    y_true = []
    y_pred = []
    for pat in range(len(experts[1])):
        for corte in range(len(experts[1][pat])):
            for k in range(2):
                for i in range(100):
                    for j in range(100):
                        y_true.append(experts[1][pat][corte][k][i][j])
                        y_pred.append(img[pat][corte][k][i][j])
    
    #print f1_score(y_true, y_pred, average='micro')  
    

    #imprime matriz de confusao para cada imagem
    print "Paciente; Corte; Sis ou Dias; Expert; TP; TN; FP; FN;"   
    
    TP = 0
    TN = 0
    FN = 0
    FP = 0
    for exp in range(len(experts)):
        for pat in range(len(experts[0])):
            for corte in range(len(experts[0][pat])):
                for k in range(2):
                    TP = 0
                    TN = 0
                    FN = 0
                    FP = 0
                    for i in range(100):
                        for j in range(100):
                            if img[pat][corte][k][i][j] == 0 and experts[exp][pat][corte][k][i][j] == 0:
                                TN = TN + 1
                            elif img[pat][corte][k][i][j] == 0 and experts[exp][pat][corte][k][i][j] == 255:
                                FN = FN + 1
                            elif img[pat][corte][k][i][j] == 255 and experts[exp][pat][corte][k][i][j] == 255:
                                TP = TP + 1
                            elif img[pat][corte][k][i][j] == 255 and experts[exp][pat][corte][k][i][j] == 0:
                                FP = FP + 1
                    if k == 0:
                        print str(pat+1) + "; " + str(corte) + "; sistole; " + str(exp+1) + "; " + str(TP) + "; " + str(TN) + "; " + str(FP) + "; " + str(FN) + ";"
                    else:
                        print str(pat+1) + "; " + str(corte) + "; diastole; " + str(exp+1) + "; " + str(TP) + "; " + str(TN) + "; " + str(FP) + "; " + str(FN) + ";"



main()