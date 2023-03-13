# -*- coding: utf-8 -*-
"""Mineração Final.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/10GT-9z-jeboNgTeHo3229dxXhAGVqtTf

Trabalho avaliativo do processo de mineração de dados - parte final

Alunos: Iago Batista Antunes Leobas, Francisco Raphael F. de Araujo, Gabriel Teixeira.

Disciplina: Mineração de Dados

Data: 26/09/2022
"""

import os
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.metrics import accuracy_score, mean_squared_error, r2_score
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report
from sklearn.linear_model import LogisticRegression

from google.colab import drive
drive.mount('/content/drive')

data = pd.read_csv("/content/drive/MyDrive/Colab Notebooks/card_transdata.csv")

"""# Verificação do Dataset e iniciando ações de limpeza caso haja necessidade..."""

data.head()

print(data.shape)

onlycredit = data[(data['used_chip'] == 1.0)]
print(onlycredit.shape)

onlyonline = onlycredit[(onlycredit['online_order'] == 1.0)]
print(onlyonline.shape)

onlyonline.isnull().any().any()

X = onlyonline.drop(['fraud'], axis=1)
Y = onlyonline['fraud']

print(X, Y)

X_train, X_test, Y_train, Y_test = train_test_split(X,Y, test_size=0.2, random_state = 42, stratify=Y)

"""# Imprimindo a acurácia dos testes"""

lr = LogisticRegression(max_iter=1000)
lr.fit(X_train, Y_train)
pred = lr.predict(X_test)
acc = accuracy_score(Y_test, pred)

f'Acurácia:{acc * 100:.2f}'

only_real = onlyonline.fraud
only_total = onlyonline.drop(['fraud'], axis=1)
only_total

"""# Realizando provisões e imprimindo os primeiros 30 resultados"""

pred = lr.predict(only_total)

only_val = pd.DataFrame({'real':only_real, 'previsao':pred})
only_val.head(n=30)

"""# Comparando os valores da previsão com os valores reais"""

only_val.previsao.value_counts()

only_val.real.value_counts()

"""# Histograma da Razão da transação do preço de compra para o preço de compra mediano"""

import plotly.express as px
px.histogram(onlyonline, x = 'ratio_to_median_purchase_price')

data['credit_and_online'] = np.where (
    (data['used_chip'] == 1.0) & (data['used_pin_number'] == 1.0) & (data['online_order'] == 1.0),
    'yes',
    'no'
)

"""# Criando a coluna credit_and_online para facilitar a visualização, dessa forma unindo informações de 3 colunas: "used_chip", "used_pin_number" e "online_order"
"""

data

data2 = data[data.credit_and_online != 'no']
data2

data2 = data2.drop([('used_chip')], axis=1)
data2

data2 = data2.drop([('used_pin_number')], axis=1)
data2

data2 = data2.drop([('online_order')], axis=1)
data2

print(data2.shape)

"""# Resposta para Hipótese 2

"Os usuários geralmente fazem compras online em lugares familiares, ou em casa ou no trabalho, por isso compras realizadas longe de casa ou muito distante da última compra são suspeitas."

# histograma da distância da compra em relação a casa do usuário
"""

import plotly.express as px
px.histogram(onlyonline, x = 'distance_from_home')

"""# histograma da distância da compra em relação a última compra realizada"""

import plotly.express as px
px.histogram(onlyonline, x = 'distance_from_last_transaction')

import matplotlib.pyplot as plt
data2.plot.scatter('distance_from_home', 'distance_from_last_transaction')



"""# Representação com outliers para melhor visualizar os registros que destoam da média de valor médio gasto. 
Dessa forma é notótio que os registros se concentram em até 5 vezes mais o valor médio de compra. 

Respondendo nossa hipótese nº 3 "Usamos o Ratio_to_median_purchase_price que nos revela a mediana do preço médio de compra. Com isso, consideramos que a grande maioria das compras devem ser até 10 vezes o valor de compra médio de cada usuário. Pois assim, conseguimos separar compras que estão distantes do normal das transações."
"""

sns.boxplot(data2['ratio_to_median_purchase_price'])

"""# Arvore de decisão"""

from sklearn.tree import DecisionTreeClassifier

arvore = DecisionTreeClassifier(criterion='entropy')
arvore.fit(X_train, Y_train)

arvore.feature_importances_

from sklearn import tree
figura, eixos = plt.subplots(nrows = 1, ncols = 1, figsize = (10,10))
tree.plot_tree(arvore)

"""# Fase de Associação

Definição das regras: criar a comparação das colunas: used_chip,	used_pin_number, online_order e fraud
"""

import pandas as pd
from mlxtend.frequent_patterns import apriori
from mlxtend.frequent_patterns import association_rules

data3 = data2
data3 = data3.drop([('distance_from_home')], axis=1)
data3 = data3.drop([('distance_from_last_transaction')], axis=1)
data3 = data3.drop([('fraud')], axis=1)
data3 = data3.drop([('credit_and_online')], axis=1)

data3.head()

sThreshold = 0.1
numberOfTransactions = len(data3)
numberOfTransactions

registros = []
for i in range(0, 100):
    registros.append([str(data3.values[i,j]) for j in range(0, 2)])
len(registros)

listOfItems = []

for i in range(len(registros)):
        for j in range(len(registros[i])):
                if(registros[i][j] not in listOfItems):
                    listOfItems.append(registros[i][j])

singleItemFrequency = {}

for item in listOfItems:
    frequency = 0
    for i in range(len(registros)):
        if(item in registros[i]):
            frequency += 1
    singleItemFrequency[item] = frequency
    
print(singleItemFrequency)

supportThreshold = sThreshold / len(registros)
print("Suporte mínimo: ", supportThreshold)

afterCleaning = {}


for key, value in singleItemFrequency.items():
    if(value > supportThreshold):
        afterCleaning[key]= value
        
print (afterCleaning)

def is_in_array(item1, item2, tocheck):
    for i in range(len(tocheck)):
        if item1 in tocheck[i] and item2 in tocheck[i]:
            return True
    return False

itemFrequency = []

for item1 in listOfItems:
    for item2 in listOfItems:
        if(item1 == item2):
            continue
        frequency = 0
        isIn = is_in_array(item1, item2, itemFrequency)
        if (isIn):
            continue
        for i in range(len(registros)):
            if(item1 and item2 in registros[i]):
                frequency += 1
        itemFrequency.append([item1,item2,frequency])
    
print(itemFrequency)

twoItemsAfterCleaning = []


for i in range(len(itemFrequency)):
    if(itemFrequency[i][2] > supportThreshold):
        twoItemsAfterCleaning.append(itemFrequency[i])
print (twoItemsAfterCleaning)

for item in twoItemsAfterCleaning:
    value = singleItemFrequency[item[0]]
    if value <= 0:
        value = 1
    confiance = (item[2]/numberOfTransactions)/value
print ("confiança da comparação da Media Das Compras daquele usuario e se essa transação já ocorreu antes é", confiance)

"""# Algoritmo de Clusterização - KMeans

Utilizaremos nesse processo de agrupamento e análise, as colunas (distance_from_home, distance_from_last_transaction).

Essas colunas foram selecionadas, baseado na hipótese que compras realizada muito distante da casa do cliente e que tambem foi distante da última compra efetuada foge do comum de uma transação não fraudulenta.
"""

V = data2.drop([('ratio_to_median_purchase_price'),('repeat_retailer'),('fraud'),('credit_and_online')], axis=1) #removendo colunas que nao utilizaremos

V = V.iloc[:,[0,1]].values #Deixando somente os dados brutos

V = pd.DataFrame(V) #conversao em data frame para realizar estracao utilizando (sample)

V = V.sample(200) #Extração randomica para retirada de amostra de 200 casos.

print(V.shape) #Confirmacao de tamanho de novo data com amostra de 200

print(V.iloc[0:6,:]) #verificando dados existente separados

"""Após preparação de dados 

# Realizacao de Verificação
"""

from sklearn.cluster import KMeans

import matplotlib.pyplot as plt

kmeans = KMeans(n_clusters=3, init = 'random', random_state = 1)
y_kmeans = kmeans.fit_predict(V)

plt.scatter(V.iloc[:,1], V.iloc[:,0])

kmeans = KMeans(n_clusters = 3, init = 'k-means++', n_init = 10, max_iter = 300) 
pred_y = kmeans.fit_predict(V)

plt.scatter(V.iloc[:,1], V.iloc[:,0], c = pred_y) #posicionamento dos eixos x e y
plt.grid()
plt.xlim(0, 150) #range do eixo x
plt.ylim(0, 400) #range do eixo y
plt.scatter(kmeans.cluster_centers_[:,1],kmeans.cluster_centers_[:,0], s = 70, c = 'red') #posição de cada centroide no gráfico
plt.show()