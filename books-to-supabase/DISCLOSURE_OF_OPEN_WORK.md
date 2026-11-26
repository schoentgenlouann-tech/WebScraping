# Disclosure of Open Work

**Technical complexity is not a grading criterion.** Disclose incomplete work honestly. We grade how you follow the process and respond to findings, rather than whether the assistant declares your project safe.

## Known incomplete work

- **Supabase writes are not verified.** The most recent one-book scrape/save attempt failed with HTTP 401 (`Invalid API key`); the configured `SUPABASE_WRITE_KEY` was not accepted. Replace it in the local, ignored `.env` with a valid server-side key for the same project. Do not commit or share the key.
- **The live database migration is pending.** The updated [`schema.sql`](./schema.sql) has not been applied to the hosted Supabase project. Apply it in the Supabase SQL Editor and confirm the hosted access policy matches the intended configuration.
- **End-to-end write validation remains.** After configuring the key and applying the migration, rerun the connection check and test **Scrape and save**. A successful write has not yet been demonstrated.
- **Dependency advisories require a follow-up upgrade.** An advisory scan performed on 2026-11-26 found known vulnerabilities in the installed environment. The current package index does not provide every fixed release reported by the scanner, so remediation must be repeated in an environment with access to those releases.

The local `.env` was not inspected, and no credential values are included here. The remediation notes report that all 6 unit tests passed, but those tests do not establish that the hosted write path works.
