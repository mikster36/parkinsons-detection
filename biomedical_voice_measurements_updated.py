# -*- coding: utf-8 -*-
"""model4.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1ftxuGlgijaZHhdWgG9Ky3-2zTD1ce-Qo
"""

import numpy as np
import pandas as pd
import os, sys
from sklearn.preprocessing import MinMaxScaler
from xgboost import XGBClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

from google.colab import drive
drive.mount('/content/drive')

pathData = "/content/drive/MyDrive/Parkinsons2022Fall/parkinsons.csv"
df = pd.read_csv(pathData)

df.head()

#DataFlair - Get the features and labels
features=df.loc[:,df.columns!='status'].values[:,1:]
labels=df.loc[:,'status'].values

#DataFlair - Scale the features to between -1 and 1
scaler=MinMaxScaler((-1,1))
x=scaler.fit_transform(features) #x' = (x-min) / (max-min)
y=labels

#DataFlair - Split the dataset
x_train,x_test,y_train,y_test=train_test_split(x, y, test_size=0.2, random_state=7)

#DataFlair - Train the model
model=XGBClassifier()
model.fit(x_train,y_train)

# DataFlair - Calculate the accuracy
y_pred=model.predict(x_test)
print(accuracy_score(y_test, y_pred)*100)

y_trainPred= model.predict(x_train)
print(accuracy_score(y_train, y_trainPred)*100)