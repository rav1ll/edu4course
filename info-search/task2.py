
import nltk
from nltk.corpus import stopwords
from pymorphy2 import MorphAnalyzer
import os


# # Загрузка стоп-слов для русского языка
nltk.download('stopwords')
nltk.download('punkt')
stop_words = set(stopwords.words('russian'))
# Инициализация pymorphy2
morph = MorphAnalyzer()

def preprocess_text(text):
    tokens = nltk.word_tokenize(text.lower())  # Токенизация и приведение к нижнему регистру
    lemmatized_tokens = [morph.parse(token)[0].normal_form for token in tokens]  # Лемматизация
    filtered_tokens = [token for token in lemmatized_tokens if token.isalnum() and token not in stop_words]  # Удаление стоп-слов и пунктуации
    return filtered_tokens


# Путь к папке с текстовыми файлами
folder_path = 'pages/'
proc_path = 'processed_pages/'
# Получаем список файлов в папке
files = os.listdir(folder_path)

for file_name in files:
    if file_name.endswith('.txt'):  # Проверяем, что файл имеет расширение .txt
        file_path = os.path.join(folder_path, file_name)

        with open(file_path, 'r', encoding='utf-8') as file:
            text = file.read()
            try:
                processed_text = preprocess_text(text)
            except:
                print('не удалось обработать файл', file_name)
            # Делаем что-то с обработанным текстом, например, сохраняем его в новый файл
            output_file_path = os.path.join(proc_path, f'processed_{file_name}')
            with open(output_file_path, 'w', encoding='utf-8') as output_file:
                output_file.write(' '.join(processed_text))

            print(f'Файл {file_name} обработан и сохранен как processed_{file_name}')
