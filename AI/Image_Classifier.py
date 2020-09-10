import os
import cv2
import keras
import random
import numpy as np
import matplotlib.pyplot as plt
from scipy import ndimage, ndarray
from keras.utils import to_categorical
from skimage import transform, util, exposure
from keras.models import load_model, Sequential
from outputs import plot_clr, plot_auroc, plot_cm
from keras.callbacks import ModelCheckpoint, CSVLogger
from keras.layers import Dense, Convolution2D, MaxPooling2D, Flatten, Dropout

np.random.seed(7)

classes = ["Depression", "Non-Depression"]

def augmentations(image_array: ndarray):
    v_min, v_max = np.percentile(image_array, (0.2, 99.8))
    return (image_array,
            transform.rotate(image_array, random.uniform(-50, 50)),
            exposure.rescale_intensity(image_array, in_range=(v_min, v_max)),
            util.random_noise(image_array),
            ndimage.gaussian_filter(image_array, 2),
            exposure.adjust_log(image_array),
            exposure.adjust_sigmoid(image_array),
            #color.rgb2gray(image_array), (FOR COLORED IMAGES)
            #np.invert(image_array), (FOR COLORED IMAGES)
            exposure.adjust_gamma(image_array, gamma=0.4, gain=0.9),
            image_array[:, ::-1],
            image_array[::-1, :])
   
#ImagesTrainOriginal, LabelsTrainOriginal, ImagesValOriginal, LabelsValOriginal = [], [], [], []
ImagesTrainAugmented, LabelsTrainAugmented, ImagesValAugmented, LabelsValAugmented = [], [], [], []

training_partition = 0.8; img_size = 64;

for label, img_folder in {0: "Depression Images/", 1: "Normal Images/"}.items():
    
    cnt = 0;
    
    for filename in os.listdir(img_folder):
         
        try:
            if cnt < (training_partition * len(os.listdir(img_folder))):
                
                image = transform.resize(cv2.imread(img_folder + "\\" + filename), (img_size, img_size), mode='constant')
                image = image.reshape(image.shape[0], image.shape[1], 3)
                
                try:
                    encoded_label = to_categorical(label, num_classes=2)
                    
                    #ImagesTrainOriginal.append(image); LabelsTrainOriginal.append(encoded_label)
                    ImagesTrainAugmented.append(image); LabelsTrainAugmented.append(encoded_label)
                        
                    ori, rot, exp, noi, gau, log, sig, gam, ver, hor = augmentations(image)
                    ImagesTrainAugmented.append(rot); LabelsTrainAugmented.append(encoded_label)
                    ImagesTrainAugmented.append(exp); LabelsTrainAugmented.append(encoded_label)
                    ImagesTrainAugmented.append(noi); LabelsTrainAugmented.append(encoded_label)
                    ImagesTrainAugmented.append(gau); LabelsTrainAugmented.append(encoded_label)
                    ImagesTrainAugmented.append(log); LabelsTrainAugmented.append(encoded_label)
                    ImagesTrainAugmented.append(sig); LabelsTrainAugmented.append(encoded_label)
                    ImagesTrainAugmented.append(gam); LabelsTrainAugmented.append(encoded_label)
                    ImagesTrainAugmented.append(ver); LabelsTrainAugmented.append(encoded_label) 
                    ImagesTrainAugmented.append(hor); LabelsTrainAugmented.append(encoded_label)
                        
                    print("[Training, "+str(cnt)+", "+str(filename)+", "+img_folder.split(" ")[0]+" Images]"); cnt +=1;
                
                except ValueError:
                    pass
            else:
                
                image = transform.resize(cv2.imread(img_folder + "\\" + filename), (img_size, img_size), mode='constant')
                image = image.reshape(image.shape[0], image.shape[1], 3)
                
                try:
                    encoded_label = to_categorical(label, num_classes=2)
                    
                    #ImagesValOriginal.append(image); LabelsValOriginal.append(encoded_label)
                    ImagesValAugmented.append(image); LabelsValAugmented.append(encoded_label)
                    
                    print("[Validation, "+str(cnt)+", "+str(filename)+", "+img_folder.split(" ")[0]+" Images]"); cnt +=1;
                
                except ValueError:
                    pass
                
        except FileNotFoundError:
            pass

randomize_train = np.arange(len(ImagesTrainAugmented))
np.random.shuffle(randomize_train)
randomize_test = np.arange(len(ImagesValAugmented))
np.random.shuffle(randomize_test)

X_train = np.array(ImagesTrainAugmented).astype(np.float)[randomize_train]   
X_test = np.array(ImagesValAugmented).astype(np.float)[randomize_test] 
y_train = np.array(LabelsTrainAugmented).astype(np.float)[randomize_train]   
y_test = np.array(LabelsValAugmented).astype(np.float)[randomize_test] 

cnn_model = Sequential()

cnn_model.add(Convolution2D(filters = 1024, kernel_size = (3, 3), input_shape = (img_size, img_size, 3), activation = 'relu'))
cnn_model.add(MaxPooling2D(pool_size = (2, 2)))

cnn_model.add(Convolution2D(filters = 512, kernel_size = (3, 3), activation = 'relu'))
cnn_model.add(MaxPooling2D(pool_size = (2, 2)))

cnn_model.add(Convolution2D(filters = 256, kernel_size = (3, 3), activation = 'relu'))
cnn_model.add(MaxPooling2D(pool_size = (1, 1)))

cnn_model.add(Convolution2D(filters = 128, kernel_size = (3, 3), activation = 'relu'))
cnn_model.add(MaxPooling2D(pool_size = (1, 1)))
cnn_model.add(Dropout(0.167))
    
cnn_model.add(Flatten())

cnn_model.add(Dense(units = 256, activation = 'relu', kernel_initializer='normal'))

cnn_model.add(Dense(units = 128, activation = 'relu', kernel_initializer='normal'))

cnn_model.add(Dense(units = 256, activation = 'relu', kernel_initializer='normal'))
cnn_model.add(Dropout(0.125))

cnn_model.add(Dense(units = 64, activation = 'relu', kernel_initializer='normal'))

cnn_model.add(Dense(units = len(classes), activation = 'softmax', kernel_initializer='uniform'))

cnn_model.compile(loss='categorical_crossentropy', optimizer=keras.optimizers.Adam(lr=0.0000000001), metrics=['accuracy'])

mcp = ModelCheckpoint('image_model.hdf5', monitor="val_acc", verbose=1, save_best_only=True, save_weights_only=False)
csv_logger = CSVLogger('image_history.csv', append=False, separator=',')
cnn_model.fit(X_train, y_train, validation_data=(X_test, y_test), batch_size = 1, epochs = 10, callbacks=[mcp, csv_logger])

model = load_model("image_model.hdf5")

y_pred = model.predict(X_test)
predictions, actuals = [], []
for i in range(len(y_pred)): 
    predictions.append(np.where(y_pred[i] == np.max(y_pred[i]))[0][0])
    actuals.append(np.where(y_test[i] == np.max(y_test[i]))[0][0])
    
plot_cm(predictions, actuals, classes, normalize=True, cmap=plt.cm.BuPu, figsz=(7,7), title="Confusion Matrix")
plt.savefig("image_cm.png", dpi=200, format='png', bbox_inches='tight', pad_inches=0.5); plt.close();

plot_auroc(y_pred, y_test, classes, title = 'Area Under the Reciever Operating Characteristics')
plt.savefig("image_auroc.png", dpi=200, format='png', bbox_inches='tight', pad_inches=0.5); plt.close();

plot_clr(predictions, actuals, classes, cmap='RdBu', figsz=(30,15), title = 'Classification Report')
plt.savefig("image_clr.png", dpi=200, format='png', bbox_inches='tight', pad_inches=0.25); plt.close();

fig = plt.figure(figsize=(9, 10))

import sklearn.metrics as sm
acc = str(round(sm.accuracy_score(predictions, actuals)*100, 3)); kappa = str(round(sm.cohen_kappa_score(predictions, actuals), 3))
fig.suptitle("\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n" + "*** ACCURACY = "+acc+"% | COHEN'S KAPPA = "+kappa+" ***", fontsize=17.5, fontweight="bold")
#import math, scipy.stats as ss
#rmse = str(round(math.sqrt(sm.mean_squared_error(predictions, actuals)), 3)); prc = str(round(ss.pearsonr(predictions, actuals), 3))
#fig.suptitle("\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n" + "*** RMSE = "+rmse+" | PEARSON'S CORRELATION = "+prc+" ***", fontsize=17.5, fontweight="bold")

fig.add_subplot(221); plt.imshow(plt.imread("image_cm.png")); plt.axis('off'); os.remove("image_cm.png")
fig.add_subplot(222); plt.imshow(plt.imread("image_auroc.png")); plt.axis('off'); os.remove("image_auroc.png")
fig.add_subplot(212); plt.imshow(plt.imread("image_clr.png")); plt.axis('off'); os.remove("image_clr.png")

plt.subplots_adjust(top = 1, bottom = 0, right = 1, left = 0, hspace = 0, wspace = 0)

plt.savefig("image_output_derivations.png", dpi=700, format='png'); plt.close();