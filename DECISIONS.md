# DECISIONS — localizer (fork of bilingual_book_maker)

Newest first. One entry per decision: date · who · decision · why · source.

- **2026-10-30 · Claude (Niko: "help me troubleshoot some errors from github")** — Upstream's three inherited
  workflows stop running on push. "Publish docs" (mkdocs gh-deploy) fails: github-actions[bot] has no write
  access and the fork has no Pages site. "CI" fails: the typos spell check reads the Finnish manuscripts in
  books/ as typos, and black --check wants 15 upstream files reformatted. Both failed identically on the previous
  push (2025-12-23); the 2026-10-30 push (the Gemini key scrub, 11c19ec) only re-triggered them. docs.yaml and
  make_test_ebook.yaml are now workflow_dispatch only; release.yaml (tags) is untouched.
