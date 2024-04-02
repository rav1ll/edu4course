# %%
from keras.models import load_model
import numpy as np
import matplotlib.pyplot as plt

import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)

def getAnswer():
    model = load_model('./digit_recognition_model/')
    print('-- Model loaded')

    num = pd.read_csv("nums.csv")
    num.head()

    num = np.array(num)
    num = num.astype('float32') / 255

    num1 = np.reshape(num, (-1, 28, 28, 1))

    print("-- Data Prepared")

    result = model.predict(num1)
    result = [np.argmax(i) for i in result]

    print("-- Predicted")

    print('Number:')
    final_result = ""
    for n in result:
        if n == 10:
            final_result += "-"
        else:
            final_result += str(n)
    print(final_result)


