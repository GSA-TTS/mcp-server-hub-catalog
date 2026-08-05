# NIH RePORTER MCP Server

> **Status:** Pilot / proof of concept. Not intended for production use.

## Overview

The NIH RePORTER MCP server exposes the
[NIH RePORTER](https://reporter.nih.gov/) grant database as a set of MCP tools.
RePORTER is the NIH's public repository of federally funded biomedical research
projects, including award amounts, principal investigators, institutions,
abstracts, and NIH institute/center attribution.

The server lets an AI application search NIH-funded projects, summarize funding
portfolios, rank top-funded PIs and institutions, and render interactive
dashboards and tables — all through natural-language requests routed through the
obot MCP gateway.

- **Data source:** [NIH RePORTER API](https://api.reporter.nih.gov/)
- **Source repository:** [GSA-TTS/mcp-server-nih-reporter](https://github.com/GSA-TTS/mcp-server-nih-reporter)
- **Runtime:** `containerized` — hosted by the gateway from the public image
  `ghcr.io/gsa-tts/mcp-server-nih-reporter` (`:8080/mcp`, health at `/health`).
  The container has no public route; it is reachable only through the gateway.
- **Authentication:** None required — queries the public RePORTER API.

## Tools

The server registers the following tools.

### Search & discovery

| Tool | Description |
|------|-------------|
| `find_project_ids` | Primary search tool. Returns a paginated page of project IDs matching search criteria, plus overview statistics (fiscal year, NIH institute, and activity-code distributions) for that page. Use `offset`/`limit` to page through large result sets. |
| `search_spending_categories` | Searches NIH spending categories by plain-English name and returns matching `(id, name)` pairs. Use it to resolve a topic (e.g. "aging", "breast cancer") into the numeric IDs required by the `spending_categories` filter. |
| `get_project_information` | Retrieves specified metadata for projects by project number — award amounts, principal investigators, abstracts, organizations, and other project details. |

### Analysis & summaries

| Tool | Description |
|------|-------------|
| `get_search_preview` | Returns key portfolio statistics by sampling up to 500 matching projects. Fast but approximate for large portfolios — use it first to characterize a search before a full analysis. |
| `get_search_summary` | Fetches **all** matching projects to provide complete, accurate statistics. Use when you need exact totals (e.g. "total funding for cancer research"). Automatically splits queries over 15,000 results into sub-queries; slower for large result sets. |
| `get_top_awarded` | Ranks entities by total funding and project count for a search portfolio. Supports grouping by PI, organization name, NIH institute, activity code, organization state, or funding mechanism. |
| `get_portfolio_crosstab` | Returns a cross-tabulation of grant counts and total funding across any two project dimensions (e.g. fiscal year × activity code) — suitable for stacked bar charts, heatmaps, or tables. |

### Interactive UI

| Tool | Description |
|------|-------------|
| `create_search_dashboard` | Builds a comprehensive dashboard for a search, with key metrics and visualizations (award-amount distribution, institute and activity-code breakdowns). |
| `get_project_table` | Displays matching projects as an interactive, sortable, searchable, paginated table (project number, title, PI, fiscal year, award amount, activity code, institute, organization). Performs the search internally. |

## Search parameters

Most tools accept a `search_params` object. Supported filters include:

- **search term** — free-text search
- **years** — fiscal years to include
- **agencies** — NIH institutes/centers
- **organizations** — grantee institutions
- **pi_name** — principal investigator name
- **po_names** — program officer names
- **award_types** — grant award types
- **spending_categories** — NIH spending category filter

The `spending_categories` filter takes numeric NIH spending category IDs
(Appendix I, FY2024):

```json
{
  "spending_categories": {
    "values": [27, 31],
    "match_all": false
  }
}
```

- `values` — list of NIH spending category numeric IDs.
- `match_all` — `true` requires projects to match **all** listed categories;
  `false` matches **at least one**.

Use `search_spending_categories` to resolve plain-English topics into these IDs.

## Example prompts

- "Who are the top-funded PIs in cancer research?"
- "Which organizations receive the most NIH funding for diabetes grants?"
- "Total NIH funding for aging grants in FY2023."
- "Show me a table of R01 grants for Stanford University."
- "Build a dashboard for opioid-related research funding."

## References

- [NIH RePORTER](https://reporter.nih.gov/)
- [NIH RePORTER API documentation](https://api.reporter.nih.gov/)
- [Source repository](https://github.com/GSA-TTS/mcp-server-nih-reporter)
- [Model Context Protocol](https://modelcontextprotocol.io/)
