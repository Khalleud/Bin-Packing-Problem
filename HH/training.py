import pandas as pd
import tensorflow as tf
import numpy as np
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split

def save_model(model,filename):
    model.save(filename)

def restore_model(filename):
    return tf.keras.models.load_model(filename)

features = ['n','poid_max','mean','dist_mean_poidMax','division_mean_poidMax','dist_max_poidMax','division_mean_std_poidMax','kurtosis','skewness','std']
training = pd.read_csv('csv/training.csv')
target = training.pop('target')
#le = LabelEncoder()
#le.fit(target)
encode = {'FF':0,'BF':1,'MF':2,'NF':3,'RC':4,'AG2':5}
decode = {0:'FF',1:'BF',2:'MF',3:'NF',4:'RC',5:'AG2'}
target = target.map(encode)
training = training[features]


x_train, x_test, y_train, y_test = train_test_split(training,target,test_size=0.2)



model = tf.keras.Sequential([
     tf.keras.layers.Dense(40,activation=tf.nn.sigmoid,input_shape=[len(training.columns)]),
     tf.keras.layers.Dense(40,activation=tf.nn.sigmoid),
     tf.keras.layers.Dense(max(target)+1,activation=tf.nn.softmax)
])

model.compile(loss='sparse_categorical_crossentropy',optimizer='adam',metrics=['accuracy'])
model.fit(x_train,y_train,epochs=1000)

print(model.evaluate(x_test,y_test))
save_model(model,'models/RNN.pk')