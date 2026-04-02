# Trace Agent

**Trace Agent** is a small [Model Context Protocol (MCP)](https://modelcontextprotocol.io/) server that runs on **AWS Lambda**. It helps track personal spending: turn receipt photos into structured data, store expenses in **PostgreSQL**, query history, summarize spending by month, and compare totals to per-category monthly budgets.

The HTTP entry point is `lambda_handler` in `main.py`, wired through [`awslabs-mcp-lambda-handler`](https://pypi.org/project/awslabs-mcp-lambda-handler/) so compatible clients can call registered tools over the Lambda event format (including API Gateway–style payloads).

## Features

- **Receipt parsing** — Sends a base64 image to **Claude** (`claude-opus-4-6`) and returns JSON: date, merchant, category, total, and line items.
- **Persistence** — Inserts and queries rows in Postgres; schema is created automatically on startup (see `db.py`).
- **Budgets** — Upsert a monthly limit per category and compare actual spend for a given `YYYY-MM` month.

## MCP tools

| Tool | Role |
|------|------|
| `extract_receipt` | `image_base64` + optional `media_type` → parsed receipt fields. |
| `save_expense` | Persist `date`, `merchant`, `category`, `total`, `items`. |
| `get_expenses` | Optional filters: `start_date`, `end_date`, `category`. |
| `get_summary` | Totals and per-category breakdown for a month (`YYYY-MM`). |
| `set_budget` | Set or update `monthly_limit` for a `category`. |
| `check_budget` | Spend vs budget for `category` and `month` (`YYYY-MM`). |

## Requirements

- Python **3.11+**
- A **PostgreSQL** database reachable from Lambda (connection string via env).
- An **Anthropic API key** with access to the configured model (used by the official SDK).

## Configuration

Environment variables (e.g. Lambda console, `.env` for local experiments):

| Variable | Purpose |
|----------|---------|
| `DATABASE_URL` | PostgreSQL connection string used by `psycopg2`. |
| `ANTHROPIC_API_KEY` | Required for `extract_receipt` (read by `anthropic` client). |

`main.py` loads environment variables with `python-dotenv` when present.

## Database schema

Defined in `init_db()` inside `db.py`:

- **`expenses`** — `date`, `merchant`, `category`, `total`, `items` (JSON), timestamps.
- **`budgets`** — unique `category`, `monthly_limit`.

## Local setup

Install dependencies from `pyproject.toml` (for example with `pip install -e .` or `uv sync`), set `DATABASE_URL` and `ANTHROPIC_API_KEY`, then deploy or invoke the `lambda_handler` with an MCP-compatible Lambda/API Gateway integration. The handler normalizes events that omit `body` (e.g. simple health checks) before delegating to the MCP runtime.

## Project layout

- `main.py` — MCP server registration and `lambda_handler`.
- `db.py` — Connection helper and schema initialization.
- `tools/extract.py` — Vision + JSON extraction.
- `tools/expenses.py` — Save, list, monthly summary.
- `tools/budget.py` — Budget upsert and spend check.
