from PIL import Image, ImageDraw, ImageFont
import csv
import numpy as np  # linear algebra
import pandas as pd  # data processing, CSV file I/O (e.g. pd.read_csv)


# минусы
def generate_images(num_images):
    images = []
    for _ in range(num_images):
        width, height = 28, 28
        background_color = (255, 255, 255)  # White color in RGB
        image = Image.new("L", (width, height), 0)
        draw = ImageDraw.Draw(image)
        symbol_width = 20
        symbol_height = 4
        x = (width - symbol_width) / 2
        y = (height - symbol_height) / 2
        symbol_color = (0, 0, 0)
        draw.rectangle([x, y, x + symbol_width, y + symbol_height], fill=255)
        images.append(np.array(image))

    return images


# Input data files are available in the read-only "../input/" directory
# For example, running this (by clicking run or pressing Shift+Enter) will list all files under the input directory

import os

for dirname, _, filenames in os.walk('kaggle/'):
    for filename in filenames:
        print(os.path.join(dirname, filename))

train_data = pd.read_csv("kaggle/train.csv")
# train_data.head()


test_data = pd.read_csv("kaggle/test.csv")
# test_data.head()


length = test_data.shape[1]
width = int(np.sqrt(length))

print("train shape :", train_data.shape)
print("test shape :", test_data.shape)

print("digits are ", width, " by ", width)

import matplotlib.pyplot as plt

train_data = train_data.sample(frac=1)

train_labels = train_data['label']
del train_data['label']

# добавляем минусы
arr = generate_images(4000)
arr = np.array(arr)
arr = arr.reshape(4000, arr.shape[1] * arr.shape[1])

train_data_array = np.array(train_data)

print(train_data_array.shape)

train_data = np.concatenate((train_data_array, arr))

train_labels = np.concatenate((train_labels, [10] * 4000))
# 

print('train data :', train_data.shape)
print('train labels :', train_labels.shape)

train_data = np.array(train_data).reshape((train_data.shape[0], width, width, 1))
test_data = np.array(test_data).reshape((test_data.shape[0], width, width, 1))

train_data = train_data.astype('float32') / 255
test_data = test_data.astype('float32') / 255

print('-- Data Prepared')

from keras.utils import to_categorical


train_labels = to_categorical(train_labels)

print('-- Labels Prepared')

x_val = train_data[:1]

# train_data = train_data[:40000]

y_val = train_labels[:1]

# train_labels = train_labels[:40000]

print('-- Validation set Created')

from keras import models
from keras import layers
from keras import regularizers

model = models.Sequential()
model.add(layers.Conv2D(32, (3, 3), activation='relu', input_shape=(28, 28, 1)))
model.add(layers.MaxPooling2D((2, 2)))
model.add(layers.Dropout(0.2))
model.add(layers.Conv2D(64, (3, 3), activation='relu'))
model.add(layers.MaxPooling2D((2, 2)))
model.add(layers.Dropout(0.2))
model.add(layers.Conv2D(64, (3, 3), activation='relu'))

model.add(layers.Flatten())
model.add(layers.Dense(512, kernel_regularizer=regularizers.l2(0.001), activation='relu'))
model.add(layers.Dropout(0.2))
model.add(layers.Dense(64, kernel_regularizer=regularizers.l2(0.001), activation='relu'))
model.add(layers.Dropout(0.2))
model.add(layers.Dense(11, activation='softmax'))

model.compile(optimizer='rmsprop', loss='categorical_crossentropy', metrics=['accuracy'])

print("-- Model created")

epochs = 20
fit = model.fit(train_data, train_labels, epochs=epochs, batch_size=64, validation_data=(x_val, y_val))

model.save("digit_recognition_model")

print("-- Model saved")

epochs_range = range(1, epochs + 1)

acc = fit.history['accuracy']
val_acc = fit.history['val_accuracy']

plt.plot(epochs_range, acc, 'bo', label='Training acc')
plt.plot(epochs_range, val_acc, 'b', label='Validation acc')

plt.title('Training and validation accuracy')

plt.xlabel('Epochs')
plt.ylabel('Loss')
plt.legend()
plt.show()

epochs_range = range(1, epochs + 1)

loss_values = fit.history['loss']
val_loss_values = fit.history['val_loss']

plt.plot(epochs_range, loss_values, 'bo', label='Training loss')
plt.plot(epochs_range, val_loss_values, 'b', label='Validation loss')

plt.title('Training and validation loss')

plt.xlabel('Epochs')
plt.ylabel('Loss')
plt.legend()
plt.show()

result = model.predict(test_data)
result = [np.argmax(i) for i in result]
print("-- Predicted")

output = pd.DataFrame({'ImageId': range(1, len(test_data) + 1), 'Label': result})
