# Step-by-Step Setup Guide

This guide covers setting up the Books to Scrape scraper and Streamlit dashboard locally with Supabase.

## 1. Prerequisites

- Python 3.9 or later
- A Supabase account and project
- Git, if you are cloning the repository

The project files are in the `books-to-supabase` directory. From the repository root, enter it:

```sh
cd books-to-supabase
```

## 2. Create and activate a Python environment

Create a virtual environment and install the project dependencies:

```sh
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
```

In Windows PowerShell, activate it with:

```powershell
.\.venv\Scripts\Activate.ps1
```

Keep the environment activated for the commands in the rest of this guide.

## 3. Create a Supabase project and collect its settings

Create a project in Supabase, then find its project URL and API keys in the project's API settings.

You will need:

- The project URL, such as `https://your-project-id.supabase.co`
- A publishable key (or legacy anon key) for `SUPABASE_KEY`, used for reads
- A server-side service-role/secret key for `SUPABASE_WRITE_KEY`, used for writes

The write key is privileged. It bypasses row-level security, so use it only in this local server-side `.env` file or a server-side secret manager. Never place it in browser code, commit it, or share it.

## 4. Configure the environment variables

Copy the tracked example file to a local `.env`:

```sh
cp .env.example .env
```

Edit `.env` and replace the placeholders:

```dotenv
SUPABASE_URL=https://your-project-id.supabase.co
SUPABASE_KEY=your-publishable-or-anon-key
SUPABASE_WRITE_KEY=your-server-side-service-role-or-secret-key
```

Do not add quotes unless required by your shell or secret manager. Keep `.env` private; it is intended to stay local and must not be committed.

## 5. Create or update the database table

In the Supabase dashboard, open the project's **SQL Editor**, paste the contents of [`schema.sql`](./schema.sql), and run it. Then open **Table Editor** and confirm that `public.books` exists.

The SQL creates the table if needed, enables row-level security, and grants the anonymous role read-only access. On an existing table, it replaces the previous anonymous read/insert policy with a read-only policy; it does not delete book rows.

## 6. Check the read connection

From this directory, run:

```sh
python scraper.py --check-connection
```

A successful check confirms the configured URL and read key can access Supabase. If it fails, recheck `SUPABASE_URL`, `SUPABASE_KEY`, and that the schema was applied to the same Supabase project.

## 7. Run the tests

The unit tests use generated HTML and mocked Supabase calls, so they do not scrape the website or require working Supabase credentials:

```sh
python -m unittest discover -s tests -v
```

## 8. Scrape and save books

Scrape and save up to 10 books (the default):

```sh
python scraper.py
```

To choose a different maximum:

```sh
python scraper.py --limit 8
```

Writes require a valid `SUPABASE_WRITE_KEY`. Records are upserted using their unique `source_url`, so rerunning the scraper does not create duplicates for the same books.

## 9. Start the dashboard

Run Streamlit:

```sh
streamlit run app.py
```

Open the local address printed in the terminal, usually `http://localhost:8501`. Use **Scrape and save** to collect books, or browse and filter records already in the database. Leave the terminal running while using the dashboard.

## 10. Verify the complete setup

Confirm all of the following:

1. The unit tests pass.
2. `python scraper.py --check-connection` succeeds.
3. A one-book scrape/save succeeds and the record appears in `public.books`.
4. The dashboard can display the saved record.

The last two checks verify the live write and dashboard paths; passing unit tests or the read connection check alone does not verify writes.

## Known outstanding setup items

The latest recorded one-book scrape/save attempt failed with HTTP 401 (`Invalid API key`), so the configured `SUPABASE_WRITE_KEY` was not accepted and successful writes have not yet been verified. The updated database schema was also recorded as not yet applied to the hosted project. Complete steps 3–6 with the correct project and keys, apply the schema, and then repeat the write and dashboard checks in step 10. See [`DISCLOSURE_OF_OPEN_WORK.md`](./DISCLOSURE_OF_OPEN_WORK.md) for the current open-work disclosure.
