import re
import sys
from bs4 import BeautifulSoup
import requests

if __name__ == "__main__":
    # print("To run this script, please use the command 'python3 scraper.py' in the terminal.")

    if (len(sys.argv) < 2):
        print("Please provide the URL as a command line argument.")
        sys.exit(1)

    URL = sys.argv[1]


    page = requests.get(URL)

    if page.status_code != 200:
        print(f"Failed to retrieve the page. Status code: {page.status_code}")
        sys.exit(1)

    page = BeautifulSoup(page.content, "html.parser")

    results = page.find_all("span", class_="align-left")

    texts = []

    for result in results:  
        row = re.sub(r'\d', '', result.text).strip()
        print(row)
