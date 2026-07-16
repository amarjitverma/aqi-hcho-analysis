\# Model Architecture



\## Overview



This document describes the architecture of each deep learning model used in the project.



\## LSTM Model



\### Architecture

Input (seq\_length, n\_features)

↓

LSTM(128, return\_sequences=True)

↓

Dropout(0.3)

↓

LSTM(64)

↓

Dropout(0.3)

↓

Dense(64, activation='relu')

↓

Dropout(0.2)

↓

Dense(1)





\### Parameters

\- lstm\_units: 128

\- dropout\_rate: 0.3

\- learning\_rate: 0.001



\## CNN-LSTM Model



\### Architecture

Input (seq\_length, height, width, channels)

↓

TimeDistributed(Conv2D(64, 3x3))

↓

TimeDistributed(MaxPooling2D(2x2))

↓

TimeDistributed(Conv2D(128, 3x3))

↓

TimeDistributed(MaxPooling2D(2x2))

↓

TimeDistributed(Flatten)

↓

LSTM(128)

↓

Dropout(0.3)

↓

LSTM(64)

↓

Dropout(0.3)

↓

Dense(64, activation='relu')

↓

Dropout(0.2)

↓

Dense(1)



\### Parameters

\- conv\_filters: 64

\- lstm\_units: 128

\- learning\_rate: 0.001



\## ConvLSTM Model



\### Architecture

Input (seq\_length, height, width, channels)

↓

ConvLSTM2D(64, kernel\_size=3, padding='same')

↓

BatchNormalization

↓

ConvLSTM2D(32, kernel\_size=3, padding='same')

↓

BatchNormalization

↓

ConvLSTM2D(16, kernel\_size=3, padding='same')

↓

BatchNormalization

↓

Dense(64, activation='relu')

↓

Dropout(0.2)

↓

Dense(1)





\### Parameters

\- filters: 64

\- kernel\_size: 3

\- lstm\_units: 128



\## Transformer Model



\### Architecture

Input (seq\_length, n\_features)

↓

Dense(d\_model)

↓

MultiHeadAttention(n\_heads)

↓

Add + LayerNormalization

↓

FeedForward (d\_model \* 2 → d\_model)

↓

Add + LayerNormalization

↓

GlobalAveragePooling1D

↓

Dense(64, activation='relu')

↓

Dropout(0.2)

↓

Dense(1)





\### Parameters

\- d\_model: 128

\- n\_heads: 8

\- n\_layers: 4

\- learning\_rate: 0.001





