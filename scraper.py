import sys
import requests
import re
from bs4 import BeautifulSoup
from collections import Counter


def fetch_page(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")

    title = soup.title.string if soup.title and soup.title.string else "No Title"
    body = soup.get_text()

    links = []
    for link in soup.find_all("a"):
        href = link.get("href")
        if href:
            links.append(href)

    return title, body, links


def get_word_frequencies(text):
    words = re.findall(r'[a-zA-Z0-9]+', text.lower())
    return Counter(words)


def polynomial_hash(word):
    p = 53
    m = 2**64
    hash_value = 0
    p_power = 1

    for ch in word:
        hash_value = (hash_value + ord(ch) * p_power) % m
        p_power = (p_power * p) % m

    return hash_value


def compute_simhash(freq_dict):
    vector = [0] * 64

    for word, freq in freq_dict.items():
        h = polynomial_hash(word)
        for i in range(64):
            if h & (1 << i):
                vector[i] += freq
            else:
                vector[i] -= freq

    simhash = 0
    for i in range(64):
        if vector[i] > 0:
            simhash |= (1 << i)

    return simhash


def count_common_bits(hash1, hash2):
    x = hash1 ^ hash2
    diff_bits = bin(x).count('1')
    return 64 - diff_bits


def main():

    if len(sys.argv) == 2:
        url = sys.argv[1]
        title, body, links = fetch_page(url)

        print("\nTitle:", title)
        print("\nBody:", body)
        print("\nLinks found:")

        for link in links:
            print(link)
        
    elif len(sys.argv) == 3:
        url1 = sys.argv[1]
        url2 = sys.argv[2]

        title1, body1, links1 = fetch_page(url1)
        title2, body2, links2 = fetch_page(url2)

        freq1 = get_word_frequencies(body1)
        freq2 = get_word_frequencies(body2)

        simhash1 = compute_simhash(freq1)
        simhash2 = compute_simhash(freq2)

        print("\nTitle1:", title1)
        print("\nTitle2:", title2)

        print("\nbody1:",body1)
        print("\nbody2:",body2)

        print("\nlinks1:")
        for link in links1:
            print(link)

        print("\nlinks2:")
        for link in links2:
            print(link)

        print("\nSimHash value of first document:", simhash1)
        print("SimHash value of second document:", simhash2)

        common_bits = count_common_bits(simhash1, simhash2)
        print("Common bits in SimHash:", common_bits)

    else:
        print("Usage:")
        print("For single URL: python scraper.py <URL>")
        print("For two URLs: python scraper.py <URL1> <URL2>")
        sys.exit(1)


if __name__ == "__main__":
    main()