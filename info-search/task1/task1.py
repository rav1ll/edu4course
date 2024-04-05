import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import re

# URL искомой веб-страницы
target_url = 'https://bookscafe.net/'


# Счетчики для отслеживания количества сохраненных страниц и общего количества слов


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


page_count = 0
total_word_count = 0
pages_to_visit = [target_url]
max_pages=100
min_words=1000

def download_page(pages_to_visit, max_pages,min_words):
    visited = set()
    page_count = 0

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
    }

    while pages_to_visit and page_count < max_pages:

        current_url = pages_to_visit.pop(0)
        if current_url in visited:
            continue

        try:
            response = requests.get(current_url, headers=headers)
            soup = BeautifulSoup(response.content, 'html.parser')

            child_content = extract_text(response.content)
            word_count = len(child_content.split())

            if word_count >= min_words:
                print(f'Downloading: {page_count, current_url}')

                with open(f"pages/page_{page_count}.txt", "w", encoding="utf-8") as file:
                    file.write(child_content)

                with open("index.txt", "a", encoding="utf-8") as index_file:
                    index_file.write(f"{page_count}: {current_url}\n")

                page_count += 1

            for link in soup.find_all('a'):
                href = link.get('href')
                if href and href.startswith('http'):
                    pages_to_visit.append(href)

            visited.add(current_url)



        except Exception as e:
            print(f"Error downloading {current_url}: {e}")

    print(f"downloaded {page_count} pages.")


download_page(pages_to_visit,max_pages,min_words)
