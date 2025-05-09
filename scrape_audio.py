# create a script

if __name__ == "__main__":
    import sys
    import time
    from pathlib import Path
    import requests
    from bs4 import BeautifulSoup
    from selenium import webdriver
    from selenium.webdriver.common.by import By
    from selenium.webdriver.firefox.options import Options

    if len(sys.argv) != 2:
        print("Usage: python audio_scrapper.py <URL>")
        sys.exit(1)
    

    URL = sys.argv[1]

    options = Options()
    options.add_argument("--headless")
    browser = webdriver.Firefox(options=options)
    browser.get(URL)

    time.sleep(3)

    rendered_page = browser.page_source

    soup = BeautifulSoup(rendered_page, "html.parser")

    book_chapter_text = soup.find(class_="book-chapter-text").get("title")

    audio_player_src = soup.find("video", class_="audio-player").get("src")

    # output
    p = Path("")
    # Download audio
    audio_page = requests.get(audio_player_src)
    with open(book_chapter_text.replace(' ', '') + ".mp3", "wb") as file:
        file.write(audio_page.content)

    browser.close()
    browser.quit()