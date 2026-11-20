# Books to Scrape → Supabase

A small Python scraper for the educational catalog at [books.toscrape.com](https://books.toscrape.com/). It collects a limited number of books and upserts them into a Supabase `public.books` table. The default limit is 10, and repeated runs update matching books by `source_url`.

## Setup

1. Install Python 3.9 or later and dependencies:

   ```sh
   python -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt
   ```

2. In Supabase, open **SQL Editor**, run [`schema.sql`](./schema.sql), and verify that `public.books` appears in **Table Editor**.
3. Copy `.env.example` to `.env`. In Supabase **Project Settings → API**, get the Project URL and the publishable key (or legacy anon key), and put them in `.env` as `SUPABASE_URL` and `SUPABASE_KEY`. Do not put a service-role/secret key in `.env` that could be committed or exposed.

The supplied SQL enables row-level security and grants the `anon` role access for this public educational dataset. For real or private data, remove that broad policy and use a server-side secret key stored only in a protected environment, or define narrower policies.

## Check connection and run

Check that the configured key can read the table:

```sh
python scraper.py --check-connection
```

Then scrape and save up to 10 books:

```sh
python scraper.py
```

To select a different limit:

```sh
python scraper.py --limit 8
```

Verify the inserted rows in Supabase **Table Editor → books**, or run:

```sql
select title, price, rating, source_url, scraped_at
from public.books
order by id desc
limit 10;
```

## Launch the interface

The Streamlit interface lets you trigger a scrape and browse, search, filter, and sort the books stored in Supabase:

```sh
streamlit run app.py
```

Open the local URL printed in the terminal (usually `http://localhost:8501`). Keep `.env` in this project folder so the interface can connect to Supabase. The interface uses the same scraper and database table as the command-line workflow.

## Schema and “schema”

The database schema is the table's structure: its columns, types, constraints, and access policies. `schema.sql` creates that structure before the scraper writes data. The scraper's field names and types correspond to these columns; `source_url` is unique so that upserts don't create duplicates.

## Local tests

Tests use generated listing HTML and mocked Supabase calls; they do not visit the website or need Supabase credentials:

```sh
python -m unittest discover -s tests -v
```
