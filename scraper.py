import sys
import requests
from bs4 import BeautifulSoup


def fetch_soup(url):
    response = requests.get(url)
    return BeautifulSoup(response.text, "html.parser")


def extract_title(soup):
    if soup.title and soup.title.string:
        return soup.title.string.strip()
    return "No Title"


def extract_body(soup):
    return soup.get_text(separator=" ", strip=True)


def extract_links(soup):
    links = []
    for link in soup.find_all("a"):
        href = link.get("href")
        if href:
            links.append(href)
    return links


def main():
    if len(sys.argv) == 2:
        url = sys.argv[1]

        soup = fetch_soup(url)

        title = extract_title(soup)
        body = extract_body(soup)
        links = extract_links(soup)

        print("\nTitle:", title)
        print("\nBody:", body)
        print("\nLinks found:")
        for link in links:
            print(link)

    else:
        print("Usage:")
        print("python scraper.py <URL>")
        sys.exit(1)


if __name__ == "__main__":
    main()