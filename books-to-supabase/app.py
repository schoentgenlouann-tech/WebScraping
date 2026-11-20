import requests
import streamlit as st
from dotenv import load_dotenv
from httpx import HTTPError
from postgrest.exceptions import APIError

from scraper import get_supabase_client, save_books, scrape_books

load_dotenv()


def show_error(action: str, error: Exception) -> None:
    if not isinstance(error, APIError):
        st.error(f"{action}: {error}")
        return

    st.error(f"{action} (Supabase error {error.code}): {error.message}")
    if str(error.code) == "521":
        st.warning(
            "Supabase's host is unavailable (Cloudflare 521). Check the project status "
            "in the Supabase dashboard; if it is paused, resume it, then retry."
        )
    elif str(error.code) in {"401", "403"}:
        st.info("Supabase denied the request. Check the publishable key and table access policies.")
    else:
        st.info("Check the Supabase table, schema, and access policies.")


st.set_page_config(page_title="Books to Scrape", page_icon="📚", layout="wide")
st.title("Books to Scrape")
st.caption("Scrape the educational catalog and explore the books saved in Supabase.")

with st.sidebar:
    st.header("Scrape catalog")
    scrape_limit = st.slider("Books to collect", min_value=1, max_value=100, value=10)
    if st.button("Scrape and save", type="primary", use_container_width=True):
        try:
            supabase = get_supabase_client()
            with st.spinner(f"Collecting up to {scrape_limit} books..."):
                new_books = scrape_books(scrape_limit)
                if not new_books:
                    st.warning("The scraper did not find any books.")
                else:
                    save_books(supabase, new_books)
                    st.success(f"Saved {len(new_books)} books to Supabase.")
        except (requests.RequestException, HTTPError, APIError, RuntimeError, ValueError) as exc:
            show_error("Could not scrape and save books", exc)

    st.divider()
    st.caption("Data source: [Books to Scrape](https://books.toscrape.com/)")

try:
    response = (
        get_supabase_client()
        .table("books")
        .select("title, price, availability, rating, product_url, image_url, source_url, scraped_at")
        .order("title")
        .limit(1000)
        .execute()
    )
    books = response.data or []
except (APIError, HTTPError, RuntimeError) as exc:
    show_error("Could not load books from Supabase", exc)
    st.stop()

if not books:
    st.info("No books have been saved yet. Use **Scrape and save** in the sidebar to get started.")
    st.stop()

st.subheader("Catalog")
search_term = st.text_input("Search by title", placeholder="For example, A Light in the Attic")
filter_col, sort_col = st.columns(2)
with filter_col:
    minimum_rating = st.selectbox(
        "Minimum rating",
        [0, 1, 2, 3, 4, 5],
        format_func=lambda value: "Any" if value == 0 else f"{value}+ stars",
    )
with sort_col:
    sort_order = st.selectbox("Sort by", ["Title (A-Z)", "Price (low to high)", "Rating (high to low)"])

filtered_books = [
    book
    for book in books
    if search_term.casefold() in book["title"].casefold()
    and (book.get("rating") or 0) >= minimum_rating
]
if sort_order == "Price (low to high)":
    filtered_books.sort(key=lambda book: book["price"])
elif sort_order == "Rating (high to low)":
    filtered_books.sort(key=lambda book: book.get("rating") or 0, reverse=True)
else:
    filtered_books.sort(key=lambda book: book["title"].casefold())

average_price = (
    sum(float(book["price"]) for book in filtered_books) / len(filtered_books)
    if filtered_books
    else 0
)
average_rating = (
    sum(book.get("rating") or 0 for book in filtered_books) / len(filtered_books)
    if filtered_books
    else 0
)
metric_col, price_col, rating_col = st.columns(3)
metric_col.metric("Books shown", len(filtered_books))
price_col.metric("Average price", f"£{average_price:.2f}")
rating_col.metric("Average rating", f"{average_rating:.1f} / 5")

if not filtered_books:
    st.info("No books match those filters.")
else:
    for start in range(0, len(filtered_books), 3):
        card_columns = st.columns(3)
        for column, book in zip(card_columns, filtered_books[start : start + 3]):
            with column:
                with st.container(border=True):
                    if book.get("image_url"):
                        st.image(book["image_url"], width=130)
                    st.markdown(f"**{book['title']}**")
                    st.write(f"£{float(book['price']):.2f} · {book.get('rating') or 'Unrated'} / 5")
                    st.caption(book.get("availability") or "Availability unknown")
                    st.link_button("View book", book["product_url"], use_container_width=True)

st.caption(f"Showing {len(filtered_books)} of {len(books)} books. Data is read from your Supabase table.")
