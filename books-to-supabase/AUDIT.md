# Publication Audit

- **Audit date:** 2026-11-20
- **Repository:** `schoentgenlouann-tech/WebScraping`
- **Branch and commit reviewed:** `main` at `6ac5f89`
- **Scope:** Committed files and the current working tree. This was a read-only review; project code was not executed.

## Summary

No high-confidence secret values or personal data were found in the committed project files or accessible Git history. The local `.env` is ignored and is not tracked. The committed `.env.example` contains placeholders.

There is an important, intentional-but-broad database access policy, plus two uncommitted local changes that should be reviewed before they are included in a future commit.

## Findings and recommended actions

### 1. Anonymous users can modify the books table

In [`schema.sql`](./schema.sql#L14), the `anon` role is granted `SELECT`, `INSERT`, and `UPDATE`. The policy at [`schema.sql`](./schema.sql#L18) applies to all operations without row restrictions. A client with the project URL and publishable key can therefore read, insert, or update rows.

The README identifies this as intended for a public educational dataset. Keep it only if public modification is acceptable. For protected data, restrict anonymous access and perform writes through a trusted server-side component using credentials that are never committed or exposed to browsers.

### 2. Local `schema.sql` contains non-SQL text

At audit time, the working-tree copy of [`schema.sql`](./schema.sql) had non-SQL setup instructions appended after the SQL. This change was uncommitted and was not in the reviewed commit. Running the entire modified file in Supabase SQL Editor would fail. Remove or relocate the prose to the README before running or committing the modified SQL.

### 3. Local `.env.example` is deleted

At audit time, Git showed `books-to-supabase/.env.example` deleted in the working tree; the reviewed commit still contains the placeholder template. Restore it if the deletion was accidental, or intentionally keep the deletion. The README also documents how to create `.env` manually.

### 4. Optional ignore-rule improvement

[`.gitignore`](./.gitignore) excludes `.env`, `.venv`, Python bytecode, and common caches. It does not exclude `.streamlit/secrets.toml`. No such file was tracked during this audit; add an ignore rule if Streamlit secrets files are introduced.

## Checks that passed

- `.env` is ignored, not tracked in the current tree, and does not appear in accessible Git history.
- The committed `.env.example` contains placeholder values.
- A scan of committed text files found no known private-key or high-confidence token patterns.
- The README covers project purpose, data collection and persistence, user interaction, setup, learning, limitations, and external dependencies.
- Dependencies are declared in [`requirements.txt`](./requirements.txt).

## Not verified

- The local `.env` contents were not inspected, so the exact credential type and value were not verified.
- The live Supabase project's current RLS policies and settings were not independently checked.
- No dependency-advisory scan was run. Project tests were not run because they execute project code, which the audit prompt prohibited.
- The repository alone cannot prove the provenance of code or independently confirm the statement that no external snippets were copied.

No credential values are recorded in this report.
