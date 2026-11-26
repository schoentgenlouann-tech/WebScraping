# Publication Remediation

- **Date:** 2026-11-20
- **Repository:** `schoentgenlouann-tech/WebScraping`
- **Implementation commit:** `9eeae2f` on `main`

## Changes made

- Updated [`schema.sql`](./schema.sql) to revoke anonymous table privileges and grant anonymous users read access only. The previous all-operations policy is replaced by a read policy.
- Split Supabase clients in [`scraper.py`](./scraper.py) and [`app.py`](./app.py): reads use `SUPABASE_KEY`; scraper and dashboard writes require a separate `SUPABASE_WRITE_KEY`.
- Added placeholder configuration for both keys in [`.env.example`](./.env.example). No actual credentials are included.
- Added `.streamlit/secrets.toml` to [`.gitignore`](./.gitignore).
- Updated [`README.md`](./README.md) with the key requirements, migration instructions, and server-side handling warning.
- Added tests confirming writes require the separate server-side key.

## Validation

- All 6 unit tests passed.
- Python syntax checks passed for the app and scraper.
- `pip check` reported no broken requirements.
- `python scraper.py --check-connection` succeeded using the anonymous read key.
- A one-book scrape/save attempt failed with HTTP 401, `Invalid API key`. The configured `SUPABASE_WRITE_KEY` is not currently accepted by Supabase. No key value is recorded here.

## Remaining steps

1. Replace `SUPABASE_WRITE_KEY` in the ignored local `.env` with a valid server-side service-role/secret key for the same Supabase project. Do not share or commit it.
2. Apply [`schema.sql`](./schema.sql) in the Supabase SQL Editor. The hosted database policy has not been changed by this repository update; the dashboard requires an authenticated session.
3. Restart Streamlit, rerun `python scraper.py --check-connection`, and test **Scrape and save** after steps 1 and 2. The write path has not yet been verified successfully.
4. Re-run a dependency-advisory scan and upgrade packages when patched releases are available from the configured package index.

The local `.env` was not inspected or included in this report.
