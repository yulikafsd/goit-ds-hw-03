import json
import requests
from bs4 import BeautifulSoup

from client import db


def get_urls(soup):
    return [
        "https://quotes.toscrape.com" + a["href"]
        for a in soup.select("a[href^='/author']")
    ]


def parse_author(url):

    html_doc = requests.get(url)
    soup = BeautifulSoup(html_doc.text, "lxml")

    fullname = soup.find("h3", class_="author-title").text.strip()
    born_date = soup.find("span", class_="author-born-date").text.strip()
    born_location = soup.find("span", class_="author-born-location").text.strip()
    description = soup.find("div", class_="author-description").text.strip()

    return {
        "fullname": fullname,
        "born_date": born_date,
        "born_location": born_location,
        "description": description,
    }


def get_authors(authors_urls):
    authors = []

    # Loop authors pages, getting text from them
    for url in authors_urls:
        author = parse_author(url)
        authors.append(author)

    return authors


def save_authors_to_json(authors):

    try:
        with open("./src/scrap_db/authors.json", "r", encoding="utf-8") as f:
            existing_authors = json.load(f)
    except FileNotFoundError:
        existing_authors = []

    for author in authors:
        if author not in existing_authors:
            existing_authors.append(author)

    with open("./src/scrap_db/authors.json", "w", encoding="utf-8") as f:
        json.dump(existing_authors, f, indent=4)


def get_next_page_url(soup):
    next_button = soup.find("li", class_="next")
    if next_button:
        next_page_url = next_button.find("a").get("href")
        return ("").join(["https://quotes.toscrape.com", next_page_url])
    return None


def scrape_quotes(start_url):
    current_url = start_url
    while current_url:

        # Get html doc, transform to lxml, handle with BS4
        html_doc = requests.get(current_url)
        soup = BeautifulSoup(html_doc.text, "lxml")

        # Find all authors on page
        authors_urls = get_urls(soup)
        authors = get_authors(authors_urls)
        save_authors_to_json(authors)

        print(f"Scraped: {current_url}")
        current_url = get_next_page_url(soup)


if __name__ == "__main__":
    start_url = "https://quotes.toscrape.com/"
    scrape_quotes(start_url)

    with open("./src/scrap_db/authors.json", "r", encoding="utf-8") as f:
        authors_data = json.load(f)
        for author in authors_data:
            db.authors.update_one(
                {"fullname": author["fullname"]}, {"$set": author}, upsert=True
            )
