# -*- coding: utf-8 -*-
"""fa+mds+k_meams+neural_network+logistic.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1f5LjsSPUClmRDimNrdeZhyGkYsMWLtxm
"""

from sklearn.metrics import classification_report, confusion_matrix, accuracy_score
from sklearn.model_selection import KFold, cross_val_score
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.neighbors import KNeighborsClassifier
from sklearn.decomposition import FactorAnalysis
from sklearn.preprocessing import StandardScaler
from sklearn.tree import DecisionTreeClassifier
from sklearn.tree import DecisionTreeRegressor
from sklearn.preprocessing import LabelEncoder
from keras.layers import Dense, Activation
from keras.models import Sequential
from sklearn.cluster import KMeans
from sklearn.manifold import MDS
import matplotlib.pyplot as plt
from matplotlib import pyplot
from sklearn import metrics
from numpy import unique
from numpy import where
import seaborn as sns
from time import time
import pandas as pd
import numpy as np

data = pd.read_csv('/content/drive/MyDrive/projeler/Pokemon.csv')
data = data.sample(frac=1)
data = data.reset_index()
data = data.drop('index', axis=1)
print("Data Median: ", data.median())

encoder = LabelEncoder()

labels = encoder.fit_transform(data.iloc[:,12])

data = data.drop('#', axis=1)
data = data.drop('Name', axis=1)
data = data.drop('Type 1', axis=1)
data = data.drop('Type 2', axis=1)
data = data.drop('Legendary', axis=1)

accuracy = []
X = data.iloc[:,:]
y = labels
X = np.array(X)
print("X shape: ", X.shape)

transformer = FactorAnalysis(n_components=2, random_state=0)
X_fa = transformer.fit_transform(X)

fig=plt.figure(figsize=(10, 10))
plt.scatter(X_fa[:,0], X_fa[:,1])
plt.show()

embedding = MDS(n_components=2)
X_mds = embedding.fit_transform(X)

fig=plt.figure(figsize=(10, 10))
plt.scatter(X_mds[:,0], X_mds[:,1])
plt.show()

x_train, x_test, y_train, y_test = train_test_split(X, y, test_size=0.33, random_state=5)
x_train_fa, x_test_fa, y_train_fa, y_test_fa = train_test_split(X_fa, y, test_size=0.33, random_state=5)
x_train_mds, x_test_mds, y_train_mds, y_test_mds = train_test_split(X_mds, y, test_size=0.33, random_state=5)

colors = np.array(['#ff00d0','#FBD039'])
                  # 0==pink  1==yellow 

km = KMeans(n_clusters=2)
cl = km.fit(x_train)
y_p = km.predict(x_test)

fig=plt.figure(figsize=(10, 10))
plt.scatter(x_test[:,0], x_test[:,1], c=colors[y_p])
plt.show()

a_k_1 = accuracy_score(y_test, y_p)

km1 = KMeans(n_clusters=2)
c_fa = km1.fit(x_train_fa)
y_p_fa = km1.predict(x_test_fa)

fig=plt.figure(figsize=(10, 10))
plt.scatter(x_test_fa[:,0], x_test_fa[:,1], c=colors[y_p_fa])
plt.show()

a_k_2 = accuracy_score(y_test_fa, y_p_fa)

km2 = KMeans(n_clusters=2)
c_mds = km2.fit(x_train_mds)
y_p_mds = km2.predict(x_test_mds)

fig=plt.figure(figsize=(10, 10))
plt.scatter(x_test_mds[:,0], x_test_mds[:,1], c=colors[y_p_mds])
plt.show()

a_k_3 = accuracy_score(y_test_mds, y_p_mds)

accuracy.append([a_k_1, a_k_2, a_k_3])

model1 = Sequential()
model1.add(Dense(255, input_dim=8))
model1.add(Activation("relu"))
model1.add(Dense(1))
model1.add(Activation("sigmoid"))

model1.compile(loss='binary_crossentropy', optimizer='sgd', metrics=['accuracy'])

model1.fit(x_train, y_train, batch_size=64, epochs=250, validation_split=0.2)

a_m_1 = model1.evaluate(x=x_test, y=y_test, batch_size=64)[1]

model2 = Sequential()
model2.add(Dense(255, input_dim=2))
model2.add(Activation("relu"))
model2.add(Dense(1))
model2.add(Activation("sigmoid"))

model2.compile(loss='binary_crossentropy', optimizer='sgd', metrics=['accuracy'])

model2.fit(x_train_fa, y_train_fa, batch_size=64, epochs=250, validation_split=0.2)

a_m_2 = model2.evaluate(x=x_test_fa, y=y_test_fa, batch_size=64)[1]

model3 = Sequential()
model3.add(Dense(255, input_dim=2))
model3.add(Activation("relu"))
model3.add(Dense(1))
model3.add(Activation("sigmoid"))

model3.compile(loss='binary_crossentropy', optimizer='sgd', metrics=['accuracy'])

model3.fit(x_train_mds, y_train_mds, batch_size=64, epochs=250, validation_split=0.2)

a_m_3 = model3.evaluate(x=x_test_mds, y=y_test_mds, batch_size=64)[1]

accuracy.append([a_m_1, a_m_2, a_m_3])

lgc = LogisticRegression(penalty='l2').fit(x_train, y_train)
y_pred = lgc.predict(x_test)

a_l_1 = accuracy_score(y_test, y_pred)

lgc1 = LogisticRegression(penalty='l2').fit(x_train_fa, y_train_fa)
y_p_fa = lgc1.predict(x_test_fa)

a_l_2 = accuracy_score(y_test_fa, y_p_fa)

lgc2 = LogisticRegression(penalty='l2').fit(x_train_mds, y_train_mds)
y_p_mds = lgc2.predict(x_test_mds)

a_l_3 = accuracy_score(y_test_mds, y_p_mds)

accuracy.append([a_l_1, a_l_2, a_l_3])

accuracy = np.array(accuracy)
df = pd.DataFrame(data=accuracy, index=["K-Means:", "Neural Networks:", "Logistic Regression:"], columns=["Orjinal", "Factoriel Analiz", "Çok B. Analiz"])
print("Doğruluk Tablosu:")
print(df)