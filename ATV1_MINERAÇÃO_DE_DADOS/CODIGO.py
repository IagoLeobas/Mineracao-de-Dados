# -*- coding: utf-8 -*-
"""Atv1.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/19iDhBnM_yvfstRUae-IwIuC5sk41kf1N
"""

import pandas as pd

video = pd.read_csv("/content/drive/MyDrive/vgsales.csv")

video.head(n=30)

print(video.shape)

video.isnull().any().any()

video = video.dropna(axis=0)

print(video.shape)

groupiago = video[(video['Platform'] == 'Wii') | (video['Platform'] == 'PS3') | (video['Platform'] == 'X360')]

groupiago.shape

plt.style.use('dark_background')
genreSales = groupiago.groupby(['Genre','Platform']).Global_Sales.sum()
genreSales.unstack().plot(kind='bar',stacked=True,  colormap= 'Blues', 
                          grid=False, figsize=(13,11))
plt.title('Comparação de Vendas por Gênero nos Consoles da 7º Geração')
plt.ylabel('Vendas')