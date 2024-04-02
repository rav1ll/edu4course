#%%
from PIL import Image, ImageDraw, ImageFont
import csv
import matplotlib.pyplot as plt
import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)


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


arr = generate_images(100)

plt.imshow(arr[0], cmap=plt.cm.binary) 
arr = np.array(arr)
print('arr data :', arr.shape)
print(arr.shape)
arr = arr.reshape(100, arr.shape[1] * arr.shape[1])
print(arr.shape)
# num = np.array(arr[0])
# num = num.astype('float32') / 255

# num1 = np.reshape(num, (-1, 28, 28, 1))
# print(num1.shape)

data = pd.read_csv("kaggle/train.csv")
train_data = data.sample(frac = 1) 


train_labels = train_data['label']
del train_data['label']

train_data_array = np.array(train_data)

import matplotlib.pyplot as plt 
import random



print(train_data_array.shape)

train_data = np.concatenate((train_data_array, arr))

train_labels = np.concatenate((train_labels, [10] * 100))
train_labels = np.array(train_labels)


print('train data :',train_data.shape)
print('train labels :',train_labels.shape)


train_data = np.array(train_data).reshape((train_data.shape[0], 28, 28, 1))

train_data = train_data.astype('float32') / 255




print('-- Data Prepared')




# Преобразуйте изображения и метки в формат, подходящий для обучения
# images = [np.array(eval(image)) for image in images]  # Преобразование строкового представления в массивы NumPy
# labels = labels.astype(int)  # Преобразование меток в целые числа

# Пример добавления нового изображения и метки в базу данных
new_image = np.array([[0, 0, 0, ...]])  # Замените это на ваше новое изображение
new_label = 10  # Новая метка для нового символа

# Добавление нового изображения и метки в базу данных
# images = np.concatenate((images, [new_image]))
# labels = np.concatenate((labels, [new_label]))


# %%
