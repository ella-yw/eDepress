import os
import numpy as np
import pandas as pd
import tensorflow as tf
from keras.models import Model
import matplotlib.pyplot as plt
from keras.models import load_model
from keras.utils import to_categorical
from keras.layers.embeddings import Embedding
from keras.preprocessing.text import Tokenizer
from outputs import plot_clr, plot_auroc, plot_cm
from sklearn.model_selection import train_test_split
from keras.preprocessing.sequence import pad_sequences
from keras.callbacks import ModelCheckpoint, CSVLogger, ReduceLROnPlateau
from keras.layers import Dense, Conv1D, MaxPooling1D, Flatten, Input, Dropout, Activation

np.random.seed(7)

classes = ["Depression", "Non-Depression"]

text, labels = [], []

for depressed in list(pd.read_csv("Depression_Data.csv", header = None)[3]):
    text.append(depressed); labels.append(0)
for normal in list(pd.read_csv("Normal_Data.csv", header = None)[3]):
    text.append(normal); labels.append(1)

t = Tokenizer(); t.fit_on_texts(text)

max_length = 500

text = pad_sequences(sequences=t.texts_to_sequences(text), maxlen=max_length)
labels = to_categorical(np.asarray(labels))

word_index = t.word_index
print('Found %s unique tokens.' % len(word_index))

X_train, X_test, y_train, y_test = train_test_split(text, labels, test_size=0.25)

"""
mu, sigma1, sigma2 = 0, 0.1, 0.15

noise1 = np.random.normal(mu, sigma1, X_train.shape) 
noise2 = np.random.normal(mu, sigma2, X_train.shape) 
noise3 = np.random.normal(mu, sigma2, X_train.shape) 

X_train_with_noise = X_train + noise1 + noise2 + noise3

X_train = np.concatenate((X_train, X_train_with_noise), axis=0)
y_train = np.concatenate((y_train, y_train), axis=0)
"""

embeddings_index = {}

f = open("glove.6B/glove.6B.100d.txt", encoding="utf8")
for line in f: embeddings_index[line.split()[0]] = np.asarray(line.split()[1:], dtype='float32')
f.close()

print('Loaded %s word vectors.' % len(embeddings_index))

embedding_matrix = np.zeros((len(word_index) + 1, 100))
for word, i in word_index.items():
    embedding_vector = embeddings_index.get(word)
    if embedding_vector is not None: embedding_matrix[i] = embedding_vector
    
embedding_layer = Embedding(len(word_index) + 1, 100, weights=[embedding_matrix], input_length=max_length, trainable=False) # Setting trainable=False to prevent the weights from being updated during training
sequence_input = Input(shape=(max_length,), dtype='int32')
embedded_sequences = embedding_layer(sequence_input)

x = Conv1D(128, len(classes), activation='relu')(embedded_sequences)
x = MaxPooling1D(1)(x)
x = Dropout(0.3)(x)
x = Conv1D(256, 1, activation='relu')(x)
x = MaxPooling1D(1)(x)
x = Dropout(0.3)(x)
x = Conv1D(256, 1, activation='relu')(x)
x = MaxPooling1D(1)(x)
x = Dropout(0.3)(x)
x = Conv1D(128, 1, activation='relu')(x)
x = MaxPooling1D(1)(x)
x = Dropout(0.3)(x)

x = Flatten()(x)
x = Dropout(0.3)(x)

x = Dense(128, activation='relu')(x)
x = Dropout(0.3)(x)
x = Dense(len(classes))(x) # 2 Outputs: "Depression" & "Non-Depression"

preds = Activation(tf.nn.softmax)(x)

model = Model(sequence_input, preds)
model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['acc'])

checkpoint = ModelCheckpoint("text_model.hdf5", monitor='val_acc', verbose=1, save_weights_only=False, save_best_only=True)
csv_logger = CSVLogger("text_history.csv", separator=',', append=False)
reduce_lr = ReduceLROnPlateau(monitor='val_acc', factor=0.5, patience=4, verbose=1, mode='max', min_lr=0.0001)
    
history = model.fit(X_train, y_train, validation_data=(X_test, y_test), 
                    epochs=5, batch_size=20, callbacks=[checkpoint, csv_logger, reduce_lr])

model = load_model("text_model.hdf5")

y_pred = model.predict(X_test)
predictions, actuals = [], []
for i in range(len(y_pred)): 
    predictions.append(np.where(y_pred[i] == np.max(y_pred[i]))[0][0])
    actuals.append(np.where(y_test[i] == np.max(y_test[i]))[0][0])
    
plot_cm(predictions, actuals, classes, normalize=True, cmap=plt.cm.BuPu, figsz=(7,7), title="Confusion Matrix")
plt.savefig("text_cm.png", dpi=200, format='png', bbox_inches='tight', pad_inches=0.5); plt.close();

plot_auroc(y_pred, y_test, classes, title = 'Area Under the Reciever Operating Characteristics')
plt.savefig("text_auroc.png", dpi=200, format='png', bbox_inches='tight', pad_inches=0.5); plt.close();

plot_clr(predictions, actuals, classes, cmap='RdBu', figsz=(30,15), title = 'Classification Report')
plt.savefig("text_clr.png", dpi=200, format='png', bbox_inches='tight', pad_inches=0.25); plt.close();

fig = plt.figure(figsize=(9, 10))

import sklearn.metrics as sm
acc = str(round(sm.accuracy_score(predictions, actuals)*100, 3)); kappa = str(round(sm.cohen_kappa_score(predictions, actuals), 3))
fig.suptitle("\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n" + "*** ACCURACY = "+acc+"% | COHEN'S KAPPA = "+kappa+" ***", fontsize=17.5, fontweight="bold")
#import math, scipy.stats as ss
#rmse = str(round(math.sqrt(sm.mean_squared_error(predictions, actuals)), 3)); prc = str(round(ss.pearsonr(predictions, actuals), 3))
#fig.suptitle("\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n" + "*** RMSE = "+rmse+" | PEARSON'S CORRELATION = "+prc+" ***", fontsize=17.5, fontweight="bold")

fig.add_subplot(221); plt.imshow(plt.imread("text_cm.png")); plt.axis('off'); os.remove("text_cm.png")
fig.add_subplot(222); plt.imshow(plt.imread("text_auroc.png")); plt.axis('off'); os.remove("text_auroc.png")
fig.add_subplot(212); plt.imshow(plt.imread("text_clr.png")); plt.axis('off'); os.remove("text_clr.png")

plt.subplots_adjust(top = 1, bottom = 0, right = 1, left = 0, hspace = 0, wspace = 0)

plt.savefig("text_output_derivations.png", dpi=700, format='png'); plt.close();