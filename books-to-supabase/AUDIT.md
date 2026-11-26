# Publication Audit

- **Audit date:** 2026-11-20
- **Repository:** `schoentgenlouann-tech/WebScraping`
- **Baseline reviewed:** `main` at `12d94e5`
- **Scope:** Committed files and remediation changes in the working tree. Project code was not executed as part of the audit.

## Summary

No high-confidence secret values or personal data were found in the committed project files or accessible Git history. The local `.env` is ignored and is not tracked. The committed `.env.example` contains placeholders.

The repository changes now use read-only anonymous access and a separate server-side write key. The SQL migration has not been applied to the live Supabase project. Follow-up cleanup also removed non-SQL instructions from the schema and added an ignore rule for Streamlit secrets.

## Findings and recommended actions

### 1. Anonymous write access — addressed in repository; live migration required

The updated [`schema.sql`](./schema.sql#L14) revokes anonymous privileges and grants `SELECT` only. Its policy at [`schema.sql`](./schema.sql#L18) allows anonymous reads. CLI and Streamlit writes now use a separate `SUPABASE_WRITE_KEY`.

These changes do not alter the hosted database automatically. Apply the updated schema in Supabase SQL Editor and configure `SUPABASE_WRITE_KEY` in the local `.env` or server-side secret manager before scraping. Never commit or expose this key.

### 2. Non-SQL text in local `schema.sql` — resolved

The accidental setup instructions were removed from [`schema.sql`](./schema.sql); the file now contains SQL only.

### 3. Configuration example — resolved

The [`.env.example`](./.env.example) template has been restored with placeholders for the read and write keys. Replace placeholders only in the ignored local `.env`, never in the tracked example.

### 4. Ignore Streamlit secrets — resolved

The [`.gitignore`](./.gitignore#L6) excludes `.streamlit/secrets.toml` in addition to `.env`, `.venv`, Python bytecode, and common caches. No Streamlit secrets file was tracked.

## Checks that passed

- `.env` is ignored, not tracked in the current tree, and does not appear in accessible Git history.
- The `.env.example` contains placeholders, not actual credentials.
- A scan of committed text files found no known private-key or high-confidence token patterns.
- The README covers project purpose, data collection and persistence, user interaction, setup, learning, limitations, and external dependencies.
- Dependencies are declared in [`requirements.txt`](./requirements.txt).
- During the follow-up remediation, all six unit tests passed and Python syntax checks passed for the app and scraper.

## Additional consideration

A previously shared screenshot showed a Supabase publishable key. This key type is intended for public clients and is not a service-role secret. Until the updated schema is applied to the hosted project, the previous anonymous write policy may still be active. No key value is included in this report.

## Not verified

- The local `.env` contents were not inspected, so the exact credential type and value were not verified.
- The live Supabase project's current RLS policies and settings were not independently checked or changed.
- The local `.env` was not inspected; the presence or validity of `SUPABASE_WRITE_KEY` is unverified.
- No dependency-advisory scan was run during the original audit. Project tests were not run during that read-only audit; they were run separately to validate follow-up code changes.
- The repository alone cannot prove the provenance of code or independently confirm the statement that no external snippets were copied.

No credential values are recorded in this report.

## Follow-up validation — 2026-11-26

The audit follow-up added explicit test coverage for use of the public read key and corrected the dashboard's guidance for rejected write requests. Validation results:

- All 7 unit tests pass; Python syntax checks and `pip check` pass.
- The live anonymous read connection succeeds.
- A live one-record scrape/save attempt still fails with HTTP 401 (`Invalid API key`). A successful hosted write has not been demonstrated.
- A dependency advisory scan of the installed environment reported 84 known vulnerability records across 12 packages. The configured package index did not offer all fixed releases reported by the scanner, so dependency remediation remains open.
- The live database migration remains unverified and must be applied in the Supabase project; repository changes alone do not update hosted policies.

No secrets were read, recorded, or included in this follow-up.
