import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import re

# URL искомой веб-страницы
target_url = 'https://cyberleninka.ru/'

# Счетчики для отслеживания количества сохраненных страниц и общего количества слов
page_count = 0
total_word_count = 0


def is_url(text):
    url_pattern = re.compile(r'https?://(?:[-\w.]|(?:%[\da-fA-F]{2}))+')
    return bool(re.match(url_pattern, text))


def extract_text(html):
    soup = BeautifulSoup(html, 'html.parser')
    text = soup.get_text()

    # Заменяем неразрывные пробелы на обычные пробелы
    text_without_nbsp = text.replace('\xa0', ' ')

    # Удаляем большие пробелы и переносы строк
    cleaned_text = ' '.join(text_without_nbsp.split())

    return cleaned_text


# Создаем файл index.txt для записи информации о сохраненных страницах
with open('index.txt', 'w', encoding='utf-8') as index_file:
    while page_count < 100:
        # Отправляем GET-запрос к странице
        response = requests.get(target_url)

        # Проверяем успешность запроса
        if response.status_code == 200:
            # Используем BeautifulSoup для парсинга HTML
            soup = BeautifulSoup(response.content, 'html.parser')

            # все ссылки на странице
            links = soup.find_all('a')

            # Флаг для отслеживания, была ли найдена новая дочерняя страница
            new_page_found = False

            # Перебираем найденные ссылки
            for link in links:
                # Получаем URL ссылки
                href = link.get('href')

                # Проверяем, является ли ссылка абсолютной и находится ли на том же домене

                # Формируем абсолютный URL дочерней страницы
                child_url = urljoin(target_url, href)

                # Переходим по дочерней странице
                if is_url(child_url):
                    response_child = requests.get(child_url)
                    # Переходим по дочерней странице

                    # Проверяем успешность запроса к дочерней странице
                    if response_child.status_code == 200:
                        # Получаем текстовое содержимое страницы
                        child_content = extract_text(response_child.text)

                        # Проверяем количество слов на странице (примерно)
                        word_count = len(child_content.split())

                        if word_count >= 1000:
                            page_count += 1
                            print('page %s downloaded' %page_count)
                            total_word_count += word_count

                            # Записываем текстовое содержимое в файл с уникальным именем
                            file_name = 'pages/' + f'page_{page_count}.txt'
                            with open(file_name, 'w', encoding='utf-8') as file:
                                file.write(child_content)

                                # Записываем информацию о странице в index.txt
                            index_file.write(f'{file_name}: {child_url}\n')

                            new_page_found = True

                        if page_count >= 10:
                            break  # Выход из цикла после сохранения 100 страниц

            else:
                print('Ошибка при получении дочерней страницы:', response_child.status_code)

        if not new_page_found:
            break  # Прерываем цикл, если не было найдено новых дочерних страниц

print(f'Сохранено {page_count} страниц с общим количеством слов {total_word_count}')
