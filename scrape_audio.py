# create a script
import sys
import time
import logging
import sys
from pprint import pprint
from enum import Enum
from pathlib import Path
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.firefox.options import Options

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

class AudioEnum(str, Enum):
    """
    Enum for download audio options.
    """
    URL = sys.argv[1]
    OUTPUT_DIR = str(Path(sys.argv[1]).parent.parent.name)
    FILE_NAME = str(Path(URL).parent.name) + str(Path(URL).name) + ".mp3"

def main():
    if len(sys.argv) != 2:
        print("Usage: python audio_scrapper.py <URL>")
        sys.exit(1)
    
    options = Options()
    options.add_argument("--headless")
    browser = webdriver.Firefox(options=options)
    browser.get(AudioEnum.URL.value)

    time.sleep(3)

    rendered_page = browser.page_source
    soup = BeautifulSoup(rendered_page, "html.parser")
    book_chapter_text = soup.find(class_="book-chapter-text").get("title")
    audio_player_src = soup.find("video", class_="audio-player").get("src")

    logging.info(f"Book Chapter Text: {book_chapter_text}")
    logging.info(f"Audio Player Source: {audio_player_src}")

    audio_page = requests.get(audio_player_src)
    output_dir = Path(AudioEnum.OUTPUT_DIR.value)
    output_dir.mkdir(parents=True, exist_ok=True)
    
    with open(output_dir / AudioEnum.FILE_NAME.value, "wb") as file:
        file.write(audio_page.content)
        logging.info(f"Downloaded {file.name} succesfully", )

    browser.close()
    browser.quit()

if __name__ == "__main__":
    main()