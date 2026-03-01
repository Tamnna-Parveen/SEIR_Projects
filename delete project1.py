# Step 1: Take URL from Command Line
import sys
import requests
import re
from bs4 import BeautifulSoup
from collections import Counter


def fetch_page(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")

    if soup.title and soup.title.string:
        title = soup.title.string
    else:
        title = "No Title"

    body = soup.get_text()

    links = []
    for link in soup.find_all("a"):
        href = link.get("href")
        if href:
            links.append(href)

    return title, body, links


def main():
   
    if len(sys.argv) != 2:
        print("Usage: python scraper.py <URL>")
        sys.exit(1)

url = sys.argv[1]

title, body, links = fetch_page(url)


print("\nTitle:", title)
print("\nBody:",body)
print("\nLinks found:")
for link in links:
    print(link)

if __name__ == "__main__":
    main()
