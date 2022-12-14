# -*- coding: utf-8 -*-
"""HeartDiseasePrediction.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1U5XFeNU2Kn05DpGw0YGW1niSCQxVwhIu
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt 
from sklearn.preprocessing import StandardScaler
from sklearn.impute import SimpleImputer
from sklearn.model_selection import train_test_split

from google.colab import drive
drive.mount('/content/drive')

data = pd.read_csv("drive/MyDrive/HeartData/heartData.csv")

data.head()

data.shape

data.info()

data.dropna(axis=0, inplace=True)

data.shape

X = data.drop("TenYearCHD", axis=1)
y = data["TenYearCHD"]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.20)

X_train.head()

from sklearn.model_selection import StratifiedShuffleSplit

split = StratifiedShuffleSplit(n_splits=1, test_size=0.20, random_state=10)

for train_index, test_index in split.split(data, data["TenYearCHD"]):
    strat_train_set = data.iloc[train_index]
    strat_test_set = data.iloc[test_index]

strat_test_set["TenYearCHD"].value_counts()/len(strat_test_set)

strat_train_set["TenYearCHD"].value_counts()/len(strat_train_set)

print(strat_train_set.shape)
print(strat_test_set.shape)

from sklearn.svm import SVC
from sklearn.metrics import f1_score
from sklearn.model_selection import GridSearchCV
from sklearn.metrics import accuracy_score

import seaborn as sns
from sklearn.metrics import confusion_matrix

imp_features = ["age", "totChol", "sysBP", "diaBP", "BMI", "heartRate", "glucose", "male"]

X_train = strat_train_set.drop("TenYearCHD", axis=1)
y_train = strat_train_set["TenYearCHD"]

X_test = strat_test_set.drop("TenYearCHD", axis=1)
y_test = strat_test_set["TenYearCHD"]

#grid search for optimum parameters
Cs = [0.001, 0.01, 0.1, 1, 10]
gammas = [0.001, 0.01, 0.1, 1]
param_grid = {'C': Cs, 'gamma' : gammas}
svm_clf = GridSearchCV(SVC(kernel='rbf', probability=True), param_grid, cv=10)

svm_clf.fit(X_train,y_train)
svm_clf.best_params_



svm_clf = SVC(C=10, gamma=1, probability=True)

svm_clf.fit(X_train, y_train)

p = svm_clf.predict(X_test)

X_train_x = X_train[imp_features]

X_test_x = X_test[imp_features]

svm_clf_x = GridSearchCV(SVC(kernel='rbf', probability=True), param_grid, cv=10)

svm_clf_x.fit(X_train_x, y_train)
svm_clf_x.best_params_

# predictions
svm_predict = svm_clf.predict(X_test)
svm_predict_x = svm_clf_x.predict(X_test_x)

accuracy_score(y_test, svm_predict)

print(svm_predict.shape)
print(svm_predict_x.shape)
print(y_test.shape)

accuracy_score(y_test, svm_predict_x)

cm=confusion_matrix(y_test,p)
conf_matrix=pd.DataFrame(data=cm,columns=['Predicted:0','Predicted:1'],index=['Actual:0','Actual:1'])
plt.figure(figsize = (8,5))
sns.heatmap(conf_matrix, annot=True,fmt='d',cmap="YlGnBu")

y_train.value_counts()

y_test.value_counts()

"""### Scaling the data"""

scaler = StandardScaler()

X_train_scaled = scaler.fit_transform(X_train)
X_train = pd.DataFrame(X_train_scaled)

X_test_scaled = scaler.transform(X_test)
X_test = pd.DataFrame(X_test_scaled)

svm_clf = SVC(C=10, gamma=1, probability=True)

svm_clf.fit(X_train_scaled, y_train)

pred = svm_clf.predict(X_test_scaled)

cm=confusion_matrix(y_test,pred)
conf_matrix=pd.DataFrame(data=cm,columns=['Predicted:0','Predicted:1'],index=['Actual:0','Actual:1'])
plt.figure(figsize = (8,5))
sns.heatmap(conf_matrix, annot=True,fmt='d',cmap="YlGnBu")

scaler = StandardScaler()

X_train_scaled = scaler.fit_transform(X_train_x)
X_train = pd.DataFrame(X_train_scaled)

X_test_scaled = scaler.transform(X_test_x)
X_test = pd.DataFrame(X_test_scaled)

svm_clf = SVC(C=10, gamma=2, probability=True)

svm_clf.fit(X_train, y_train)

pred = svm_clf.predict(X_test_scaled)

cm=confusion_matrix(y_test,pred)
conf_matrix=pd.DataFrame(data=cm,columns=['Predicted:0','Predicted:1'],index=['Actual:0','Actual:1'])
plt.figure(figsize = (8,5))
sns.heatmap(conf_matrix, annot=True,fmt='d',cmap="YlGnBu")

"""### Removing Data Biasing i.e Balancing the data"""

from imblearn.over_sampling import SMOTE
from imblearn.under_sampling import RandomUnderSampler
from imblearn.pipeline import Pipeline
from collections import Counter

data = data.dropna()

imp_features = ["age", "totChol", "sysBP", "diaBP", "BMI", "heartRate", "glucose", "male"]
X = data[imp_features]
y = data.iloc[:,-1]

# the numbers before smote
num_before = dict(Counter(y))

#perform smoting

# define pipeline
over = SMOTE(sampling_strategy=0.8)
under = RandomUnderSampler(sampling_strategy=0.8)
steps = [('o', over), ('u', under)]
pipeline = Pipeline(steps=steps)

# transform the dataset
X_smote, y_smote = pipeline.fit_resample(X, y)


#the numbers after smote
num_after =dict(Counter(y_smote))

print(num_before)

print(num_after)

X_smote.head(1)

n_data = pd.concat([pd.DataFrame(X_smote), pd.DataFrame(y_smote)], axis=1)
n_data.columns = ["age", "totChol", "sysBP", "diaBP", "BMI", "heartRate", "glucose", "male", "TenYearCHD"]
n_data.head()

n_data["TenYearCHD"].value_counts()

X_n = n_data.drop("TenYearCHD",axis=1)
y_n = n_data["TenYearCHD"]

X_train, X_test, y_train, y_test = train_test_split(X_n, y_n, test_size=0.2, random_state=10)

scaler = StandardScaler()
X_scaled_train = scaler.fit_transform(X_train)
X_train = pd.DataFrame(X_scaled_train)

X_scaled_test = scaler.transform(X_test)
X_test = pd.DataFrame(X_scaled_test)

X_train.head(1)

X_test.head(1)

#grid search for optimum parameters
Cs = [0.001, 0.01, 0.1, 1, 10]
gammas = [0.001, 0.01, 0.1, 1]
param_grid = {'C': Cs, 'gamma' : gammas}
svm_clf = GridSearchCV(SVC(kernel='rbf', probability=True), param_grid, cv=10)

svm_clf.fit(X_train,y_train)
svm_clf.best_params_

pred = svm_clf.predict(X_test)
accuracy_score(y_test, pred)

cm=confusion_matrix(y_test,pred)
conf_matrix=pd.DataFrame(data=cm,columns=['Predicted:0','Predicted:1'],index=['Actual:0','Actual:1'])
plt.figure(figsize = (8,5))
sns.heatmap(conf_matrix, annot=True,fmt='d',cmap="YlGnBu")

svm_clf

svm_clf_s = SVC(gamma=1, C=10, random_state=10)

svm_clf_s.fit(X_train, y_train)

pred_s = svm_clf.predict(X_test)

accuracy_score(y_test, pred_s)

cm=confusion_matrix(y_test,pred_s)
conf_matrix=pd.DataFrame(data=cm,columns=['Predicted:0','Predicted:1'],index=['Actual:0','Actual:1'])
plt.figure(figsize = (8,5))
sns.heatmap(conf_matrix, annot=True,fmt='d',cmap="YlGnBu")

f1_score(y_test, pred_s)

"""### Saving the model"""

import pickle

# save the model to disk
filename = 'SVM_final.sav'
pickle.dump(svm_clf_s, open(filename, 'wb'))

#"age", "totChol", "sysBP", "diaBP", "BMI", "heartRate", "glucose", "male", "TenYearCHD"
i = [[61,225,150,95,28.58,65,103,0]]

t = scaler.transform(i)

t

with open('SVM_final.sav', 'rb') as file:
        heart = pickle.load(file)

pred = heart.predict(t)

pred

filename_s = 'Scaler.pkl'
pickle.dump(scaler, open(filename_s, 'wb'))