import requests
import argparse
import sys
import re
import os
from bs4 import BeautifulSoup

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python scrape_chapter.py <URL> <output_file>")
        sys.exit(1)

    parser = argparse.ArgumentParser(description="Scrape chapter titles from a Bible.is Webpage and save on text file.")
    parser.add_argument("url", help="URL of the Bible.is webpage to scrape.")
    parser.add_argument("output_file", help="Path to the output text file.")

    args = parser.parse_args()

    page = requests.get(args.url)

    soup = BeautifulSoup(page.content, "html.parser")

    sample = soup.find_all("span", class_="align-left")

    title = (args.url.split("/")[-2] + args.url.split("/")[-1])

    print("Processing: ", title)

    with open(os.path.join(args.output_file, title + ".txt"), "w", encoding="utf-8") as file:
        for i in range(len(sample)):
            file.write(re.sub("\d", '', sample[i].get_text()))

    print(f"Chapter titles saved to {args.output_file}")