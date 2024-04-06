from collections import defaultdict
import os
import json


# Функция для чтения токенизированных слов из файла
def read_tokens_from_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read().split()


# Путь к папке с файлами
folder_path = '../task2/processed_pages'

# Создаем инвертированный список терминов
inverted_index = defaultdict(list)

# Читаем токенизированные слова из каждого файла в папке
for file_name in os.listdir(folder_path):
    file_path = os.path.join(folder_path, file_name)
    tokens = read_tokens_from_file(file_path)
    for term in set(tokens):  # Используем set для уникальных токенов
        inverted_index[term].append(file_name)

# Преобразуем множества в списки перед сохранением
for term, file_names in inverted_index.items():
    inverted_index[term] = list(set(file_names))

# Сортируем индекс по алфавиту
sorted_index = dict(sorted(inverted_index.items(), key=lambda x: x[0]))


# # Сохраняем индекс в файл
# with open('inverted_index.json', 'w',encoding='utf-8') as file:
#     json.dump(sorted_index, file, indent=4, ensure_ascii=False,)
# print('inverted index saved')





def boolean_search(query, sorted_index):
    query = query.split()
    result = set()

    all_tokens = set().union(*[set(files) for files in sorted_index.values()])
    for i in range(0, len(query)):
        word = query[i]
        if i == 0:
            if word[0] == '!':
                result = all_tokens.difference(set(sorted_index[word[1::]]))
            else:
                result = set(sorted_index[word])

        if word == '&':
            next_word = query[i + 1]

            if next_word[0] == '!':

                set_with_next_word_pages = set(sorted_index.get(next_word[1::], []))
                all_pages_without_next_word_pages = all_tokens.difference(set_with_next_word_pages)

                result = result.intersection(all_pages_without_next_word_pages)
            else:

                result = result.intersection(sorted_index.get(next_word, []))

        elif word == '|':

            next_word = query[i + 1]
            if next_word[0] == '!':
                set_with_next_word_pages = set(sorted_index.get(next_word[1::], []))
                all_pages_without_next_word_pages = all_tokens.difference(set_with_next_word_pages)
                result = result.union(all_pages_without_next_word_pages)
            else:
                result = result.union(sorted_index.get(next_word, []))

        if i + 1 == len(query):
            res = list(result)
            for ind in range(len(res)):
                res[ind] = res[ind][10:-4:]

    return sorted(res)


# Примеры булевых запросов
queries = [
    'жанр & публиковать | животное',
    'жанр & !публиковать | !животное',
    'жанр | публиковать | животное',
    'жанр | !публиковать | !животное',
    'жанр & публиковать & животное'
]

for query in queries:
    print(f"Результат для запроса '{query}': \n {boolean_search(query, sorted_index)} \n")
