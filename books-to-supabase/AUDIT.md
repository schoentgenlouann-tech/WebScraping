# Publication Audit

- **Audit date:** 2026-11-20
- **Repository:** `schoentgenlouann-tech/WebScraping`
- **Branch and commit reviewed:** `main` at `9a83dd6`
- **Scope:** Committed files and the current working tree. This was a read-only review; project code was not executed.

## Summary

No high-confidence secret values or personal data were found in the committed project files or accessible Git history. The local `.env` is ignored and is not tracked. The committed `.env.example` contains placeholders.

There is an important, intentional-but-broad database access policy. Follow-up cleanup removed non-SQL instructions from the schema and added an ignore rule for Streamlit secrets.

## Findings and recommended actions

### 1. Anonymous users can modify the books table — decision required

In [`schema.sql`](./schema.sql#L14), the `anon` role is granted `SELECT`, `INSERT`, and `UPDATE`. The policy at [`schema.sql`](./schema.sql#L18) applies to all operations without row restrictions. A client with the project URL and publishable key can therefore read, insert, or update rows.

The README identifies this as intended for a public educational dataset. If public modification is acceptable for this disposable class project, no change is required. Otherwise, restrict anonymous access and perform writes through a trusted server-side component using credentials that are never committed or exposed to browsers. The policy was not changed because this decision affects whether the current scraper can write using the anon key.

### 2. Non-SQL text in local `schema.sql` — resolved

The accidental setup instructions were removed from [`schema.sql`](./schema.sql). The schema now contains SQL only.

### 3. Local `.env.example` is deleted — optional

The working tree still has `books-to-supabase/.env.example` deleted, but the committed repository has the placeholder template and the README documents how to create `.env` manually. No fix is required for setup; restore the template only if you want to keep it in your local checkout.

### 4. Ignore Streamlit secrets — resolved

The [`.gitignore`](./.gitignore#L6) now excludes `.streamlit/secrets.toml` in addition to `.env`, `.venv`, Python bytecode, and common caches. No Streamlit secrets file was tracked.

## Checks that passed

- `.env` is ignored, not tracked in the current tree, and does not appear in accessible Git history.
- The committed `.env.example` contains placeholder values.
- A scan of committed text files found no known private-key or high-confidence token patterns.
- The README covers project purpose, data collection and persistence, user interaction, setup, learning, limitations, and external dependencies.
- Dependencies are declared in [`requirements.txt`](./requirements.txt).

## Additional consideration

A previously shared screenshot showed a Supabase publishable key. This key type is intended for public clients and is not a service-role secret. However, combined with the broad anonymous write policy described above, anyone with the project URL and publishable key can modify the table. No key value is included in this report.

## Not verified

- The local `.env` contents were not inspected, so the exact credential type and value were not verified.
- The live Supabase project's current RLS policies and settings were not independently checked.
- No dependency-advisory scan was run. Project tests were not run because they execute project code, which the audit prompt prohibited.
- The repository alone cannot prove the provenance of code or independently confirm the statement that no external snippets were copied.

No credential values are recorded in this report.
