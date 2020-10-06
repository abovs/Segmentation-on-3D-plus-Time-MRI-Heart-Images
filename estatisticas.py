import pandas as pd
import matplotlib.pyplot as plt
import numpy
import numbers
import math
from sklearn import metrics
from scipy.integrate import simps
from numpy import trapz


#le o arquivo gerado pela saida de calcula_slices.py > out.txt
df = pd.read_csv('out.txt', sep=';')

#pega apenas as colunas referentes a matriz de confusao
estat = df[df.columns[4:8]] 

#pega o numero de imagens lidas
tam = int (estat.describe().transpose()['count'][0])

TPF = []
FPF = []
sens = []
espec = []
acc = []
VPP = []
VPN = []

def func(x):
    return (x)
#TP = 0
#TN = 1
#FP`= 2
#FN = 3
for i in range(tam):

	#TPF = TP/(TP+FN)
	#Sensibilidade =  TP/(TP+FN) = TPF
	aux = estat.iat[i,0] / float(estat.iat[i, 0] + estat.iat[i, 3])
	TPF.append(aux)
	sens.append(aux)

	#FPF = FP/(FP+TN)
	aux = estat.iat[i,2] / float(estat.iat[i, 2] + estat.iat[i, 1])
	FPF.append(aux)
	
	#Especificidade = TN/(TN+FP) = (1-FPF)
	aux = float(1-FPF[i])
	espec.append(aux)

	#Acuracia = (TP+TN)/(TP+TN+FP+FN)
	aux = float(estat.iat[i,0] + estat.iat[i,1]) / float(estat.iat[i,0] + estat.iat[i,1] + estat.iat[i,2] + estat.iat[i,3])
	acc.append(aux)

	#Valor Preditivo Positivo = TP/(TP+FP)
	aux = estat.iat[i,0] / float(estat.iat[i,0] + estat.iat[i,2])
	VPP.append(aux)

	#Valor Preditivo Negativo = TN/(TN+FN)
	aux = estat.iat[i,1] / float(estat.iat[i,1] + estat.iat[i,3])
	VPN.append(aux)


#salva informacoes novas num dataframe
df1 = estat.assign(TPF=TPF)
df1 = df1.assign(FPF=FPF)
df1 = df1.assign(Sensibilidade=sens)
df1 = df1.assign(Especificidade=espec)
df1 = df1.assign(Acuracia=acc)
df1 = df1.assign(Preditivo_Positivo=VPP)
df1 = df1.assign(Preditivo_Negativo=VPN)
 


#imprime as colunas de media e desvio padrao do dataframe
print df1.describe().transpose()['mean'][4:]
print df1.describe().transpose()['std'][4:]

