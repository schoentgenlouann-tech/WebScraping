# Post-Remediation Sanitized Audit

- **Audit date:** 2026-11-21
- **Repository:** `schoentgenlouann-tech/WebScraping`
- **Project:** `books-to-supabase`
- **Scope:** Repository files and committed remediation history relevant to publication safety

This report summarizes the changes made after the first publication audit. It is intentionally sanitized: no API keys, credentials, environment-variable values, personal data, or private configuration details are included.

## What was checked

The follow-up review checked:

- The Git-tracked project files and recent committed changes
- Supabase configuration examples and environment handling
- Database SQL, including privileges and row-level security
- Anonymous and server-side read/write responsibilities
- Secret-ignore rules
- Project documentation and setup instructions
- Unit-test coverage for the write-key separation
- Recorded validation results and known remaining setup steps

The live Supabase project was not accessed or modified. Local environment files and secret values were not inspected.

## Issues found in the first audit

### Anonymous database writes

The initial database configuration allowed anonymous access beyond reads. This could permit clients using the public/anonymous key to modify book data.

### Mixed responsibility for Supabase clients

The read and write paths did not clearly separate public read access from privileged server-side writes.

### Configuration and secret handling concerns

The project needed an explicit template for both read and write credentials, plus clear rules that server-side credentials must not be exposed or committed.

### Documentation gaps

The setup instructions needed to explain database migration, key separation, test coverage, and the live verification steps that remain incomplete.

## Fixes made after the first audit

### Database access restriction

- Updated [`schema.sql`](./schema.sql) to enable row-level security.
- Revoked broad anonymous table privileges.
- Granted anonymous users `SELECT` access only.
- Replaced anonymous read/insert policy behavior with an anonymous read-only policy.
- Removed setup instructions that had accidentally been mixed into the SQL file.

### Separation of read and write credentials

- Updated [`scraper.py`](./scraper.py) and [`app.py`](./app.py) so reads use the public read key.
- Required a separate server-side write key for CLI and dashboard writes.
- Added checks and tests confirming that the write path requires the server-side key.

### Secret handling

- Kept the local `.env` file outside tracked Git files.
- Restored [`.env.example`](./.env.example) with placeholders only.
- Added `.streamlit/secrets.toml` to [`.gitignore`](./.gitignore).
- Added warnings not to commit or expose the privileged write key.

### Documentation and process disclosure

- Updated [`README.md`](./README.md) with setup, key, migration, and verification guidance.
- Added [`SETUP_GUIDE.md`](./SETUP_GUIDE.md) with numbered local setup and verification steps.
- Added [`DISCLOSURE_OF_OPEN_WORK.md`](./DISCLOSURE_OF_OPEN_WORK.md) to clearly identify incomplete and unverified work.
- Expanded [`REMEDIATION.md`](./REMEDIATION.md) with the fixes, validation performed, and remaining steps.

## Validation performed

Repository-level and follow-up validation reported:

- All 6 unit tests passed.
- Python syntax checks passed for the application and scraper.
- Dependency integrity checks reported no broken requirements.
- The read connection check succeeded using the configured public read key.
- Tracked configuration examples contain placeholders rather than actual credentials.
- No high-confidence secret or private-key pattern was found in the tracked text files reviewed.

These checks do not prove that the hosted database is configured correctly or that live writes succeed.

## Remaining limitations

### Live write credentials

A recorded one-book scrape/save attempt failed with an invalid-key response. The server-side write credential currently used for that attempt was not accepted, and no successful hosted write has been demonstrated.

### Hosted database migration

The updated [`schema.sql`](./schema.sql) has not been applied to the live Supabase project. Repository changes do not modify hosted policies automatically.

### End-to-end verification

The following work remains:

1. Replace the invalid or missing local write credential with a valid server-side credential for the same Supabase project.
2. Apply the updated SQL migration in the hosted project's SQL editor.
3. Confirm the live table and row-level-security policies.
4. Rerun the connection check.
5. Successfully save a test record.
6. Confirm that the record appears in the Streamlit dashboard.

Until these steps are completed, the live write path and dashboard data flow should be considered unverified.

## Security conclusions

The repository now demonstrates clearer read/write separation and read-only anonymous database intent. However, repository configuration alone does not establish that the hosted Supabase project is correctly secured or functioning.

No credential values or secret details are published in this report. All remaining sensitive configuration must stay outside source control and must be managed locally or through an authorized secret manager.
