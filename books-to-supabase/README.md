# Books to Scrape → Supabase

A Python web scraper and Streamlit dashboard for collecting and exploring the educational catalog at [books.toscrape.com](https://books.toscrape.com/). Scraped records are saved to a Supabase `public.books` table.

## Purpose

This project collects a configurable number of books from Books to Scrape, stores their catalog details in Supabase, and provides a local web interface for browsing the saved records. It also includes a command-line workflow for running the scraper and checking the database connection.

## Data collection

The scraper sends HTTP GET requests to the Books to Scrape catalog. It parses the listing-page HTML with Beautiful Soup, follows pagination when needed, and extracts each book's title, price, availability, rating, product URL, and image URL. The default limit is 10 books per run; set a different limit with `--limit`.

## Data persistence

Book records are stored in the Supabase table `public.books`. The table also records the source URL and scrape timestamp. `source_url` is unique, and the scraper upserts by that field so repeated runs update existing records instead of making duplicates.

The Supabase URL and publishable (or legacy anon) key are read from a local `.env` file. The supplied schema enables row-level security but grants anonymous access for this public educational dataset. Do not use this broad policy for private or production data, and never put a service-role/secret key in the app or commit it to Git.

## User interaction

The Streamlit dashboard lets someone:

- Set a scrape limit and scrape/save books.
- Browse saved books with their image, price, rating, and availability.
- Search by title, filter by minimum rating, and sort by title, price, or rating.
- Open a book's source page.

The command-line workflow can also check Supabase access, scrape the default 10 books, or scrape a chosen number.

## Setup

Requirements: Python 3.9 or later and a Supabase project.

1. From this directory, create and activate a virtual environment and install dependencies:

   ```sh
   python -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt
   ```

2. In your Supabase project's **SQL Editor**, run [`schema.sql`](./schema.sql). Confirm that `public.books` appears in **Table Editor**.
3. Create a `.env` file in this directory with your project URL and publishable key (or legacy anon key):

   ```dotenv
   SUPABASE_URL=https://your-project-id.supabase.co
   SUPABASE_KEY=your-publishable-key
   ```

   Keep `.env` private and do not use a secret or service-role key.
4. Verify the connection:

   ```sh
   python scraper.py --check-connection
   ```

### Run the scraper

Scrape and save up to 10 books:

```sh
python scraper.py
```

Choose another limit:

```sh
python scraper.py --limit 8
```

### Run the interface

```sh
streamlit run app.py
```

Open the local URL printed by Streamlit, usually `http://localhost:8501`. Leave the terminal running while you use the dashboard.

### Run tests

The unit tests use generated HTML and mocked Supabase calls; they do not scrape the website or require Supabase credentials:

```sh
python -m unittest discover -s tests -v
```

## Learning and approach

This project demonstrates how to turn HTML pages into structured records, save them to a hosted database, and build a small interactive interface on top of that data. One challenge was that the source provides HTML rather than a ready-made data feed. The scraper handles this by selecting book elements from each listing page, normalizing values such as star ratings and relative links, and following the site's next-page link. Using a unique source URL for database upserts also makes repeated runs safe from duplicate rows.

## Limitations and external code

- The scraper depends on the current page structure of Books to Scrape; a site redesign could require selector changes.
- Each run collects only the requested number of books. The dashboard allows up to 100 per run and displays up to 1,000 records from Supabase.
- The dashboard is local and has no user accounts or per-user data separation. The database policy is intentionally permissive for this educational dataset.
- Supabase or the source website may be temporarily unavailable.
- No external code snippets are copied into the project. It uses the third-party Python packages listed in [`requirements.txt`](./requirements.txt); Books to Scrape is the source of the collected data.
