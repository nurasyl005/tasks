import requests
from bs4 import BeautifulSoup
import csv
import time

BASE_URL = "https://ru.wikipedia.org/wiki/Категория:Животные_по_алфавиту"
LETTERS = [chr(code) for code in range(ord('А'), ord('Я') + 1)]
OUTPUT_FILE = "beasts.csv"

def count_animals_for_letter(letter):
    url = f"{BASE_URL}/{letter}"
    count = 0

    while url:
        response = requests.get(url)
        if response.status_code != 200:
            print(f"Ошибка при загрузке {url}")
            break

        soup = BeautifulSoup(response.text, "html.parser")
        category_group = soup.find("div", class_="mw-category")

        if category_group:
            count += len(category_group.find_all("li"))

        # Переход на следующую страницу, если есть
        next_link = soup.find("a", text="Следующая страница")
        if next_link and 'href' in next_link.attrs:
            url = "https://ru.wikipedia.org" + next_link['href']
            time.sleep(0.5)  # задержка, чтобы не нагружать сервер
        else:
            url = None

    return count

def main():
    with open(OUTPUT_FILE, "w", newline='', encoding="utf-8") as csvfile:
        writer = csv.writer(csvfile)
        for letter in LETTERS:
            print(f"Обрабатывается буква: {letter}")
            count = count_animals_for_letter(letter)
            writer.writerow([letter, count])

    print(f"\nГотово! Результат сохранён в {OUTPUT_FILE}")

if __name__ == "__main__":
    main()
