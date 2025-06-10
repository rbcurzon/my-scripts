import re
import sys
import time
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.firefox.options import Options

def main():
    if len(sys.argv) != 2:
        print("Usage: python scrape_chapter_2.py <URL>")
        sys.exit(1)

    URL = sys.argv[1]

    output_dir = URL.split('/')[-3]
    file_name = URL.split("/")[-2] + URL.split("/")[-1] + ".txt"

    options = Options()
    options.add_argument("--headless")
    browser = webdriver.Firefox(options=options)
    browser.get(URL)

    rendered_page = browser.page_source

    time.sleep(2)


    soup = BeautifulSoup(rendered_page, "html.parser")

    book_chapter_texts = soup.select(".verse-chapter-wrapper")
    
    with open(output_dir + "/" + file_name, "w", encoding="utf-8") as file:
        for book_chapter_text in book_chapter_texts:
            text = re.sub(r"\d", '', book_chapter_text.getText(strip=True))
            file.write(text + " ")
            
    browser.close()
    browser.quit()

    print(f"{output_dir} chapter {URL.split('/')[-1]} is saved to {output_dir}/{file_name}")

if __name__ == "__main__":
    main()

