# Grants.gov MCP Server

> **Status:** Pilot / proof of concept. Not intended for production use.

## Overview

The Grants.gov MCP server exposes [Grants.gov](https://www.grants.gov/) — the
U.S. government's central repository for federal grant opportunities — as a set
of MCP tools. Grants.gov aggregates grant postings from all federal agencies,
covering forecasted, open, closed, and archived opportunities.

The server lets an AI application search opportunities by keyword, agency, or
status, apply eligibility and funding-category filters, paginate large result
sets, and retrieve full opportunity details including award amounts, contact
information, and eligibility requirements — all through natural-language requests
routed through the obot MCP gateway.

- **Data source:** [Grants.gov API](https://www.grants.gov/api/)
- **Source repository:** [HHS/mcp-server-grants-gov](https://github.com/HHS/mcp-server-grants-gov)
- **Runtime:** `containerized` — hosted by the gateway from the public image
  `ghcr.io/gsa-tts/mcp-server-grants-gov` (`:8080/mcp`, health at `/health`).
  The container has no public route; it is reachable only through the gateway.
- **Authentication:** None required — queries the public Grants.gov API.

## Tools

The server registers the following tools.

### Search & discovery

| Tool | Description |
|------|-------------|
| `grants_gov_search_opportunities` | Primary search tool. Queries the Grants.gov search2 API for opportunities matching the given criteria. Supports full-text keyword search and filtering by agency, status, eligibility type, and funding category. Returns paginated results in Markdown or JSON. |
| `grants_gov_fetch_opportunity` | Fetches full details for a single opportunity by its numeric ID. Includes synopsis, eligibility, award ceiling and floor, expected number of awards, cost-sharing requirements, funding instruments, activity categories, ALN numbers, contact info, and attachment folder names. |

## Search parameters (`grants_gov_search_opportunities`)

| Parameter | Type | Description |
|-----------|------|-------------|
| `keyword` | string | Full-text search across opportunity titles and descriptions |
| `opp_num` | string | Exact opportunity number lookup (e.g. `HHS-2024-ACF-OCC-0181`) |
| `agencies` | list | Agency code filters (e.g. `['HHS', 'NSF', 'DOE']`) |
| `opp_statuses` | list | Status filters: `forecasted`, `posted`, `closed`, `archived` |
| `eligibilities` | list | Eligibility code filters |
| `funding_categories` | list | Funding category code filters (e.g. `['ED', 'HL']`) |
| `aln` | string | Assistance Listing Number filter (e.g. `93.268`) |
| `rows` | integer | Results per page, 1–100 (default: 25) |
| `start_record` | integer | 1-indexed pagination offset (default: 1) |
| `response_format` | enum | `markdown` or `json` (default: `markdown`) |

## Fetch parameters (`grants_gov_fetch_opportunity`)

| Parameter | Type | Description |
|-----------|------|-------------|
| `opportunity_id` | integer | Numeric opportunity ID (e.g. `289999`). Use `grants_gov_search_opportunities` to find IDs. |
| `response_format` | enum | `markdown` (formatted summary) or `json` (raw API response) |

## Example prompts

- "Find open HHS grants related to maternal health"
- "Show me all posted NSF education grants"
- "What grants are available for small businesses in rural areas?"
- "Get full details for opportunity HHS-2024-ACF-OCC-0181"
- "List forecasted NIH grants in the health category"
- "Show me the second page of results for climate grants"
- "What is the award ceiling for opportunity 289999?"

## References

- [Grants.gov](https://www.grants.gov/)
- [Grants.gov API documentation](https://www.grants.gov/api/)
- [Source repository](https://github.com/HHS/mcp-server-grants-gov)
- [Model Context Protocol](https://modelcontextprotocol.io/)
