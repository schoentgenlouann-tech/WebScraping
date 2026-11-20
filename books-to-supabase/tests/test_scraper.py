import os
import unittest
from unittest.mock import Mock, patch

from scraper import get_supabase_write_client, parse_listing, save_books, scrape_books


def listing_html(count=6):
    cards = []
    for number in range(count):
        cards.append(
            f"""
            <article class="product_pod">
              <p class="star-rating Three"></p>
              <h3><a href="book-{number}.html" title="Book {number}">Book {number}</a></h3>
              <div class="image_container"><img src="../media/book-{number}.jpg"></div>
              <p class="price_color">£{number + 1}.00</p>
              <p class="availability">In stock</p>
            </article>
            """
        )
    return "<html><ol class='row'>" + "".join(cards) + "</ol></html>"


class ScraperTests(unittest.TestCase):
    @patch("scraper.create_client")
    def test_write_client_uses_server_side_key(self, create_client):
        environment = {
            "SUPABASE_URL": "https://example.supabase.co",
            "SUPABASE_WRITE_KEY": "test-server-side-key",
        }
        with patch.dict(os.environ, environment, clear=True):
            client = get_supabase_write_client()

        create_client.assert_called_once_with(
            "https://example.supabase.co",
            "test-server-side-key",
        )
        self.assertIs(client, create_client.return_value)

    def test_write_client_requires_server_side_key(self):
        with patch.dict(
            os.environ,
            {"SUPABASE_URL": "https://example.supabase.co", "SUPABASE_KEY": "public-key"},
            clear=True,
        ):
            with self.assertRaisesRegex(RuntimeError, "SUPABASE_WRITE_KEY"):
                get_supabase_write_client()

    def test_parse_listing_returns_six_observations(self):
        books, next_url = parse_listing(listing_html(), "https://books.toscrape.com/catalogue/page-1.html")

        self.assertEqual(len(books), 6)
        self.assertIsNone(next_url)
        self.assertEqual(books[0]["title"], "Book 0")
        self.assertEqual(books[0]["price"], 1.0)
        self.assertEqual(books[0]["rating"], 3)
        self.assertEqual(
            books[0]["source_url"],
            "https://books.toscrape.com/catalogue/book-0.html",
        )

    def test_parse_listing_finds_next_page(self):
        books, next_url = parse_listing(
            "<li class='next'><a href='page-2.html'>next</a></li>",
            "https://books.toscrape.com/catalogue/page-1.html",
        )

        self.assertEqual(books, [])
        self.assertEqual(next_url, "https://books.toscrape.com/catalogue/page-2.html")

    def test_save_books_upserts_by_source_url(self):
        table = Mock()
        table.upsert.return_value.execute.return_value = None
        client = Mock()
        client.table.return_value = table
        books = [{"source_url": "https://books.toscrape.com/book.html"}]

        save_books(client, books)

        client.table.assert_called_once_with("books")
        table.upsert.assert_called_once_with(books, on_conflict="source_url")

    def test_scrape_to_supabase_upserts_six_observations(self):
        response = Mock(text=listing_html())
        session = Mock()
        session.headers = {}
        session.get.return_value = response
        table = Mock()
        client = Mock()
        client.table.return_value = table

        books = scrape_books(6, session=session)
        save_books(client, books)

        self.assertEqual(len(books), 6)
        table.upsert.assert_called_once_with(books, on_conflict="source_url")


if __name__ == "__main__":
    unittest.main()
