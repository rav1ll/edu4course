import json
import os
import nltk
from nltk.corpus import stopwords
from pymorphy2 import MorphAnalyzer
import os

import pandas as pd

from sklearn.metrics.pairwise import cosine_similarity
from collections import Counter
import math

# # Загрузка стоп-слов для русского языка
# nltk.download('stopwords')
# nltk.download('punkt')
# stop_words = set(stopwords.words('russian'))
# Инициализация pymorphy2
morph = MorphAnalyzer()


def query_to_vector(query, idf):
    tokens = nltk.word_tokenize(query.lower())  # Токенизация и приведение к нижнему регистру
    lemmatized_tokens = [morph.parse(token)[0].normal_form for token in tokens]  # Лемматизация
    words = [word for word in lemmatized_tokens if word.strip() and word not in [' ', '\n']]

    word_count = Counter(words)

    query_length = len(words)
    query_vector = {}

    for word, count in word_count.items():
        word_tf = count / query_length

        word_idf = idf.get(word)
        if not word_idf:
            word_idf = 0
        query_vector[word] = word_tf * word_idf

    return query_vector




def vector_search(queries, tf_idf, idf, top_n):
    results = []
    with open('../task5/out.txt', 'w') as txt_file:
        for query in queries:
            query_vector = query_to_vector(query, idf)
            scores = {}

            for doc, doc_vector in tf_idf.items():
                scores[doc] = compute_cosine_similarity(doc_vector, query_vector)

            sorted_scores = sorted(scores.items(), key=lambda x: x[1], reverse=True)
            txt_file.write(f"Запрос: '{query}'\n")
            for doc, score in sorted_scores[:top_n]:  # Меняйте N для разного количества документов

                res = f"{doc} : {round(score, 7)}\n"
                txt_file.write(res)
                results.append({"Query": query, "Document": doc, "Score": score})

            txt_file.write("\n")

def compute_cosine_similarity(doc_vector, query_vector):
    # создаем векторы со всеми словами из документа и запроса + вектор слов документа
    all_words = list(set(doc_vector.keys()).union(set(query_vector.keys())))
    doc_vector = [doc_vector.get(word, 0) for word in all_words]
    query_vector = [query_vector.get(word, 0) for word in all_words]

    res = cosine_similarity([doc_vector], [query_vector])[0][0]
    return res



# кол-во документов в конечном рейтинге
top_n = 12
if __name__ == '__main__':
    processed_pages_path = '../task2/processed_pages'
    doc_collection = {}
    for file in os.listdir(processed_pages_path):
        with open(os.path.join(processed_pages_path, file), 'r', encoding='utf-8') as f:
            doc_collection[file] = f.read().split()

    with open('../task4/results/tf.json', 'r', encoding='UTF-8') as f:
        tf = json.load(f)

    with open('../task4/results/idf.json', 'r', encoding='UTF-8') as f:
        idf = json.load(f)

    with open('../task4/results/tf_idf.json', 'r', encoding='UTF-8') as f:
        tf_idf = json.load(f)

    # Предполагаем, что tf_idf и idf уже вычислены, и total_docs - общее количество документов
    queries = ["ошибкаааааа", "ошибкаааааа племя", "ошибкаааааа племя французский"]

    vector_search(queries, tf_idf, idf, top_n)
    print('поиск выполнен')
