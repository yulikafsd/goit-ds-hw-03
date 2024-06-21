import requests
from bs4 import BeautifulSoup

from client import db


def parse_quotes(soup):
    # Create list for quotes json
    quotes = []

    # Find all quotes elements in lxml with bs4
    quote_elements = soup.find_all("div", class_="quote")

    # Loop quotes, getting text from them
    for quote_element in quote_elements:
        quote_text = quote_element.find("span", class_="text").text
        author_text = quote_element.find("small", class_="author").text
        tags_text_list = [tag.text for tag in quote_element.find_all("a", class_="tag")]
        quotes.append(
            {"quote": quote_text, "author": author_text, "tags": tags_text_list}
        )

    return quotes


def save_quotes_to_db(quotes):
    for quote in quotes:
        db.quotes.update_one({"quote": quote["quote"]}, {"$set": quote}, upsert=True)


def get_next_page_url(soup):
    next_button = soup.find("li", class_="next")
    if next_button:
        next_page_url = next_button.find("a").get("href")
        return ("").join(["https://quotes.toscrape.com", next_page_url])
    return None


def scrape_quotes(start_url):
    current_url = start_url
    while current_url:

        # Get html doc, transform to lxml, handle with BS4 and add to db
        html_doc = requests.get(current_url)
        soup = BeautifulSoup(html_doc.text, "lxml")
        quotes = parse_quotes(soup)
        save_quotes_to_db(quotes)
        print(f"Scraped: {current_url}")
        current_url = get_next_page_url(soup)


if __name__ == "__main__":
    start_url = "https://quotes.toscrape.com/"
    scrape_quotes(start_url)
