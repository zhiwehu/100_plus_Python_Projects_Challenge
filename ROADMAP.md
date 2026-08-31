# 2026 Roadmap

This roadmap is intentionally practical: each project should be small enough to finish, useful enough to understand why it exists, and teach a focused set of Python skills.

## Season 2 — Projects 016–030

| # | Project | Main skills | Possible AI upgrade |
|---:|---|---|---|
| 016 | Smart File Organizer | pathlib, shutil, argparse, logging | classify files by content instead of extension |
| 017 | Duplicate File Finder | hashing, pathlib, generators | suggest which duplicates are safe to remove |
| 018 | Batch Image Resizer | Pillow, CLI, filesystem | smart crop / image description |
| 019 | PDF Toolkit | PDF parsing, merge/split, CLI | summarize and classify PDFs |
| 020 | Markdown Notes Search | text search, indexing, pathlib | semantic search over notes |
| 021 | Website Change Monitor | requests/httpx, hashing, scheduling | explain meaningful page changes |
| 022 | Web Scraper | BeautifulSoup, HTTP, parsing | extract structured information with an LLM |
| 023 | REST API Client | requests/httpx, JSON, auth | natural-language API requests |
| 024 | FastAPI Todo API | FastAPI, validation, REST | turn notes into tasks |
| 025 | SQLite Personal Database | sqlite3, SQL, CRUD | natural-language database queries |
| 026 | CSV / Excel Analyzer | pandas, openpyxl, statistics | ask questions about a dataset |
| 027 | Data Dashboard | pandas, matplotlib / web UI | generate explanations for trends |
| 028 | Local Speech to Text | audio, ASR, streaming basics | local transcription + cleanup |
| 029 | Chat with Your Documents | chunking, embeddings, retrieval | local/cloud RAG |
| 030 | Build Your First AI Agent | tools, state, structured output | multi-tool agent workflow |

## Suggested Format for New Projects

Each project should try to contain:

1. **What are we building?**
2. **Requirements**
3. **What will we practice?**
4. **Basic implementation**
5. **How to run it**
6. **Exercises / ideas to extend it**
7. **Better version** (when useful)
8. **AI Upgrade** (optional)

## Ground Rules

- Prefer standard-library solutions when they teach the concept clearly.
- Avoid unnecessary frameworks in beginner projects.
- Do not add AI simply because it is fashionable; the AI upgrade should solve a real limitation of the basic version.
- New projects should include a reproducible environment and clear run command.
- Add tests when the core logic can be tested without UI, camera, or external services.
- Keep API keys in environment variables; never commit secrets.

## Longer-Term Levels

After project 030, the challenge will continue across these themes:

- Python Basics
- Useful Scripts
- Files & Automation
- Web & APIs
- Data & Visualization
- Images / Audio / Video
- AI with Python
- AI Agents / Real Apps

The final number may go beyond 100. The point is to keep building useful things rather than stopping exactly at project 100.
