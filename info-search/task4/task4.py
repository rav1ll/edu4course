import json
import os
import math
from collections import defaultdict
import xlsxwriter
import pandas as pd


# расчет TF
def tf_count(page):
    tf_text = defaultdict(int)
    for word in page:
        tf_text[word] += 1
    word_count = sum(tf_text.values())
    return {word: round(count / word_count, 6) for word, count in tf_text.items()}


# расчет IDF
def idf_count(doc_collection):
    idf_text = defaultdict(lambda: 0)

    total_docs = len(doc_collection)
    for text in doc_collection.values():
        for word in set(text):
            idf_text[word] += 1
    return {word: round(math.log10(total_docs / count), 6) for word, count in idf_text.items()}


# расчет tf-idf
def tf_idf_count(tf, idf):
    tf_idf_text = defaultdict(lambda: {})
    for document_name, tf_values in tf.items():
        tf_idf_text[document_name] = defaultdict(lambda: {})
        for word in tf_values:
            tf_idf_text[document_name][word] = '{:f}'.format(tf_values[word] * idf[word])
    return tf_idf_text


# Путь к папке с текстовыми файлами
path = '../task2/processed_pages'

if __name__ == '__main__':
    # Чтение файлов

    doc_collection = {}
    for file in os.listdir(path):
        with open(os.path.join(path, file), 'r', encoding='utf-8') as f:
            doc_collection[file] = f.read().split()
    # TF для каждого документа
    tf = defaultdict(lambda: {})

    for item in doc_collection:
        tf[item] = tf_count(doc_collection[item])

    # IDF для коллекции документов
    idf = idf_count(doc_collection)

    # TF-IDF для каждого документа
    tf_idf = tf_idf_count(tf, idf)

    # Запись csv и json с TF
    with open(file='../task4/results/tf.json', mode='w', encoding='utf-8') as tf_file:
        json.dump(tf, tf_file, indent=4, separators=(',', ': '), ensure_ascii=False, )
    tf_dataframe = pd.DataFrame(tf).fillna(0).round(6)
    tf_dataframe.to_csv('../task4/results/tf.csv', encoding='utf-8')
    print("create tf files")

    # Запись csv и json с IDF
    with open(file='../task4/results/idf.json', mode='w', encoding='utf-8') as idf_file:
        json.dump(idf, idf_file, indent=4, separators=(',', ': '), ensure_ascii=False, )
    idf_dataframe = pd.DataFrame(idf.items(), columns=['word', 'idf']).set_index('word')
    idf_dataframe.to_csv('../task4/results/idf.csv', encoding='utf-8')
    print("create idf files")

    # Запись csv и json с TF-IDF
    with open(file='../task4/results/tf_idf.json', mode='w', encoding='utf-8') as tf_idf_file:
        dct_to_write = defaultdict(lambda: {})
        for doc, tf_idf_vals in tf_idf.items():
            dct_to_write[doc] = tf_idf[doc]
        json.dump(dct_to_write, tf_idf_file, indent=4, separators=(',', ': '), ensure_ascii=False, )
    tf_idf_values = []
    for doc, words in tf_idf.items():
        for word, value in words.items():
            tf_idf_values.append({'page': doc, 'word': word, 'tf-idf': value})
    tf_idf_dataframe = pd.DataFrame(tf_idf_values)
    tf_idf_df_pivot = tf_idf_dataframe.pivot(index='word', columns='page', values='tf-idf').fillna(0).round(6)
    tf_idf_df_pivot.to_csv('../task4/results/tf_idf.csv', encoding='utf-8')
    print("create tf-idf files")
