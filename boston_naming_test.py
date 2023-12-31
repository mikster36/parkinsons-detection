# -*- coding: utf-8 -*-
"""boston_naming_test.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1HvKgo6DA0K00J-VHkNTMmNBbABCaf6My

**Imports**
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
import tensorflow as tf
from sklearn import neighbors, svm
from sklearn.preprocessing import StandardScaler
import seaborn as sns
from matplotlib.ticker import PercentFormatter

"""**Data Preprocessing**

Note: 0 is Parkinson's, 1 is Healthy
"""

boston_naming_test_csv = "https://gist.githubusercontent.com/mikster36/19747bcb0585112b200e1071c08a3cfa/raw/961f9cc2b5af2862f83ffc70cd0592aa6465e3c9/Modified_Boston_Naming_Test.csv"
participant_status_csv = "https://gist.githubusercontent.com/mikster36/bf6b3265b74f67b219f1aeccc5da683b/raw/2e6dbd8072330b92ba0d04ff74b238434ec732ad/Participant_Status.csv"
bnt_df = pd.read_csv(boston_naming_test_csv)
ps_df = pd.read_csv(participant_status_csv)
ps_df = ps_df[["PATNO", "COHORT"]]
ps_df = ps_df[ps_df["COHORT"] <= 2]
bnt_df = bnt_df[["PATNO", "MBSTNSCR", "MBSTNCRC", "MBSTNCRR"]]
bnt_df = bnt_df[bnt_df['MBSTNCRR'] <= 60]
bnt_df.dropna(inplace=True)

#Decide whether to drop test version column or fill blanks with default test version

ps_df.head()

patient_dict = dict(zip(ps_df.values[:,0], ps_df.values[:,1]))
def patient_to_label(patient_number):
  if patient_number not in patient_dict:
    return -1;
  else:
    return patient_dict.get(patient_number);

labels = bnt_df["PATNO"].apply(lambda x: patient_to_label(x))
data = bnt_df[labels != -1]
data = data.drop(columns=["PATNO"])
labels = labels[labels != -1]
labels -= 1
print(data)
print(labels)

"""**Data Visualization**"""

plt.hist(data[labels == 0]["MBSTNSCR"], bins=25, alpha=0.5, label="Diagnosed")
plt.hist(data[labels == 1]["MBSTNSCR"], bins=25, alpha=0.75, label="Control")
plt.xlabel("Number of Spontaneously Correct Responses")
plt.ylabel("Number of Patients")
plt.legend()
plt.show()

plt.hist(data[labels == 0]["MBSTNCRR"], bins=25, alpha = 0.5, density=True)
plt.hist(data[labels == 1]["MBSTNCRR"], bins=25, alpha = 0.75, density=True)
plt.gca().yaxis.set_major_formatter(PercentFormatter(1))

plt.hist(data[labels == 0]["MBSTNCRC"], bins=25, alpha = 0.5, density=True)
plt.hist(data[labels == 1]["MBSTNCRC"], bins=25, alpha = 0.75, density=True)
plt.gca().yaxis.set_major_formatter(PercentFormatter(1))

sns.histplot(data[labels == 0]["MBSTNCRC"])
sns.histplot(data[labels == 1]["MBSTNCRC"])

"""**Model + Testing**"""

scaler = StandardScaler() #Standardizing data (mean = 0, SD = 1)
scaler.fit(data)
data = scaler.transform(data)

train_X, test_X, train_Y, test_Y = train_test_split(data, labels, random_state=2, test_size=0.2)

print(data.shape, train_X.shape, test_X.shape)

model = svm.SVC(kernel='rbf', gamma=.1)

model.fit(train_X, train_Y)

X_test_prediction = model.predict(test_X)
test_data_accuracy = accuracy_score(test_Y, X_test_prediction)
print('Accuracy score of test data: ', test_data_accuracy)

model2 = neighbors.KNeighborsClassifier(n_neighbors=37, weights='distance')

model2.fit(train_X, train_Y)

X_test_prediction = model2.predict(test_X)
test_data_accuracy = accuracy_score(test_Y, X_test_prediction)
print('Accuracy score of test data: ', test_data_accuracy)