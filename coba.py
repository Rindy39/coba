# -*- coding: utf-8 -*-
"""Tugas Mandiri Pertemuan 14_Rindy Rafida_ITS Surabaya.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/10t1Ix8ZIqpSGInENgXHCnAs2pPezId8A
"""

#Latihan 1
# import library pandas
import pandas as pd

# Import library numpy
import numpy as np

# Import library matplotlib untuk visualisasi
import matplotlib.pyplot as plt

# import library for build model 
import tensorflow as tf
from keras.layers import Dense,Dropout,SimpleRNN,LSTM
from keras.models import Sequential
from tensorflow.keras import Sequential

# import library untuk data preprocessing
from sklearn.preprocessing import MinMaxScaler
from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score

# me-non aktifkan peringatan pada python
import warnings
warnings.filterwarnings('ignore')

from google.colab import files
uploade = files.upload()

#Panggil file (load file bernama Stock.csv) dan simpan dalam dataframe
dataset ="Stock.csv"
data = pd.read_csv(dataset)

# tampilkan 5 baris data 
data.head(5)

# Melihat Informasi lebih detail mengenai struktur DataFrame dapat dilihat menggunakan fungsi info()
data.info()

# Kolom 'low' yang akan kita gunakan dalam membangun model
# Slice kolom 'low' 

Low_data = data.iloc[:,3:4].values

# cek output low_data
Low_data

# Visualizing low_data
plt.figure(figsize=(14,10))                 
plt.plot(Low_data,c="red")
plt.title("Microsoft Stock Prices",fontsize=16)
plt.xlabel("Days",fontsize=16)
plt.ylabel("Scaled Price",fontsize=16)
plt.grid()
plt.show()

#LAtihan 2
# Menskalakan data antara 1 dan 0 (scaling) pada low data
scaler = MinMaxScaler(feature_range=(0,1))
Low_scaled = scaler.fit_transform(Low_data)

# Definisikan variabel step dan train 
step_size = 21
train_x = []
train_y = []

# membuat fitur dan lists label
for i in range(step_size,3019):
    train_x.append(Low_scaled[i-step_size:i,0])
    train_y.append(Low_scaled[i,0])

# mengonversi list yang telah dibuat sebelumnya ke array
train_x = np.array(train_x)
train_y = np.array(train_y)

# cek dimensi data dengan function .shape
print(train_x.shape)

# 498 hari terakhir akan digunakan dalam pengujian
# 2500 hari pertama akan digunakan dalam pelatihan
test_x = train_x[2500:]
train_x = train_x[:2500]
test_y = train_y[2500:]
train_y = train_y[:2500]

# reshape data untuk dimasukkan kedalam Keras model
train_x = np.reshape(train_x, (2500, step_size, 1))
test_x = np.reshape(test_x, (498, step_size, 1))

# cek kembali dimensi data yang telah di reshape dengan function .shape
print(train_x.shape)
print(test_x.shape)

#Latihan 3
# Build Model - RNN

# buat varibel penampung model RNN
rnn_model = Sequential()

# Output dari SimpleRNN akan menjadi bentuk tensor 2D (batch_size, 40) dengan Dropout sebesar 0.15
rnn_model.add(SimpleRNN(40,activation="tanh",return_sequences=True, input_shape=(train_x.shape[1],1)))
rnn_model.add(Dropout(0.15))
rnn_model.add(SimpleRNN(40,activation="tanh",return_sequences=True))
rnn_model.add(Dropout(0.15))
rnn_model.add(SimpleRNN(40,activation="tanh",return_sequences=False))
rnn_model.add(Dropout(0.15))
# Add a Dense layer with 1 units.
rnn_model.add(Dense(1))

# menambahkan loss function kedalam model RNN dengan tipe MSE
rnn_model.compile(optimizer="adam",loss="MSE")

# fit the model RNN, dengan epoch 20 dan batch size 25
#import tensorflow.compat.v1 as tf
rnn_model.fit(train_x,train_y,epochs=20,batch_size=25)

# Prediksi Model RNN
rnn_predictions = rnn_model.predict(test_x)
rnn_score = r2_score(test_y,rnn_predictions)

#Score RNN
rnn_score

#LATIHAN 4

# buat varibel penampung model LSTM
lstm_model = Sequential()

# Add a LSTM layer with 40 internal units. dengan Dropout sebesar 0.15
lstm_model.add(LSTM(40,activation="tanh",return_sequences=True, input_shape=(train_x.shape[1],1)))
lstm_model.add(Dropout(0.15))
lstm_model.add(LSTM(40,activation="tanh",return_sequences=True))
lstm_model.add(Dropout(0.15))
lstm_model.add(LSTM(40,activation="tanh",return_sequences=False))
lstm_model.add(Dropout(0.15))
# Add a Dense layer with 1 units.
lstm_model.add(Dense(1))

# menambahkan loss function kedalam model lstm dengan tipe MSE
lstm_model.compile(optimizer="adam",loss="MSE")

# fit lstm model, dengan epoch 20 dan batch size 25
lstm_model.fit(train_x,train_y,epochs=20,batch_size=25)

# Prediksi Model LSTM
lstm_predictions = lstm_model.predict(test_x)
lstm_score = r2_score(test_y,lstm_predictions)

#Cetak Score LSTM
lstm_score

#LATIHAN 5

# Cetak nilai prediksi masing-masing model dengan menggunakan r^2 square
print("R^2 Score of RNN",rnn_score)
print("R^2 Score of LSTM",lstm_score)

# Visualisasi Perbandingan Hasil Model prediksi dengan data original
lstm_predictions = scaler.inverse_transform(lstm_predictions)
rnn_predictions = scaler.inverse_transform(rnn_predictions)
test_y = scaler.inverse_transform(test_y.reshape(-1,1))

plt.figure(figsize=(16,12))
plt.plot(test_y, c="blue",linewidth=2, label="original")
plt.plot(lstm_predictions, c="green",linewidth=2, label="LSTM")
plt.plot(rnn_predictions, c="red",linewidth=2, label="RNN")
plt.legend()
plt.title("PERBANDINGAN",fontsize=20)
plt.grid()
plt.show()

"""Beri Kesimpulan Anda !

Hasil Pengujian Model RNN (Recurrent neural network) dan LSTM (Long Short-Term Memory):

1. RNN untuk membuat prediksi untuk masa depan yang menerapkan model Sequential yang sangat mirip antara RNN dan LSTM.
2. Kemudian proses selanjutnya dengan menguji seberapa baik mereka untuk membuat prediksi yang baik dan Mengevaluasi hasilnya.
3. Model LSTM mungkin kurang baik dalam memprediksi karena LSTM menyimpan informasi dalam memori untuk jangka waktu yang lama, sehingga menghasilkan tingkat akurasi yang kurang baik.
4. Model RNN lebih baik dalam memprediksi dengan pemrosesan data secara sequential.
"""