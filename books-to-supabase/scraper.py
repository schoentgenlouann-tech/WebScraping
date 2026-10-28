from __future__ import annotations

import argparse
import os
import re
import sys
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv
from supabase import Client, create_client

BASE_URL = "https://books.toscrape.com/"
RATING_VALUES = {"One": 1, "Two": 2, "Three": 3, "Four": 4, "Five": 5}
USER_AGENT = "BooksToScrapeCatalog/1.0 (educational use)"


def parse_listing(html: str, page_url: str = BASE_URL) -> tuple[list[dict], str | None]:
    soup = BeautifulSoup(html, "html.parser")
    books = []
    for item in soup.select("article.product_pod"):
        title_link = item.select_one("h3 a")
        price = item.select_one(".price_color")
        availability = item.select_one(".availability")
        image = item.select_one(".image_container img")
        rating = item.select_one(".star-rating")
        if not (title_link and price and availability and image and rating):
            continue

        books.append(
            {
                "title": title_link.get("title", title_link.get_text(strip=True)),
                "price": float(re.sub(r"[^0-9.]", "", price.get_text(strip=True))),
                "availability": " ".join(availability.get_text(" ", strip=True).split()),
                "rating": RATING_VALUES.get(
                    next((name for name in rating.get("class", []) if name in RATING_VALUES), "")
                ),
                "product_url": urljoin(page_url, title_link.get("href", "")),
                "image_url": urljoin(page_url, image.get("src", "")),
                "source_url": urljoin(page_url, title_link.get("href", "")),
            }
        )

    next_link = soup.select_one("li.next a")
    next_url = urljoin(page_url, next_link.get("href", "")) if next_link else None
    return books, next_url


def scrape_books(limit: int, session: requests.Session | None = None) -> list[dict]:
    if limit < 1:
        raise ValueError("limit must be at least 1")
    client = session or requests.Session()
    client.headers.update({"User-Agent": USER_AGENT})
    page_url: str | None = BASE_URL
    books: list[dict] = []

    while page_url and len(books) < limit:
        response = client.get(page_url, timeout=20)
        response.raise_for_status()
        page_books, page_url = parse_listing(response.text, page_url)
        books.extend(page_books[: limit - len(books)])
    return books


def get_supabase_client() -> Client:
    url = os.getenv("SUPABASE_URL")
    key = os.getenv("SUPABASE_KEY")
    if not url or not key:
        raise RuntimeError("Set SUPABASE_URL and SUPABASE_KEY in the environment or .env file.")
    return create_client(url, key)


def check_supabase_connection(client: Client) -> None:
    client.table("books").select("id").limit(1).execute()


def save_books(client: Client, books: list[dict]) -> None:
    if books:
        client.table("books").upsert(books, on_conflict="source_url").execute()


def main() -> int:
    load_dotenv()
    parser = argparse.ArgumentParser(description="Scrape books.toscrape.com into Supabase.")
    parser.add_argument("--limit", type=int, default=10, help="Maximum books to scrape (default: 10).")
    parser.add_argument(
        "--check-connection",
        action="store_true",
        help="Check Supabase access by reading one row from the books table.",
    )
    args = parser.parse_args()

    try:
        supabase = get_supabase_client()
    except RuntimeError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1

    if args.check_connection:
        check_supabase_connection(supabase)
        print("Supabase connection OK: read from public.books.")
        return 0

    try:
        books = scrape_books(args.limit)
    except (requests.RequestException, ValueError) as exc:
        print(f"Scrape failed: {exc}", file=sys.stderr)
        return 1
    if not books:
        print("No books found; nothing was written.", file=sys.stderr)
        return 1
    save_books(supabase, books)
    print(f"Upserted {len(books)} books into public.books.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
