# Regulations.gov MCP Server

> **Status:** Pilot / proof of concept. Not intended for production use.

## Overview

The Regulations.gov MCP server exposes
[Regulations.gov](https://www.regulations.gov) — the official U.S. federal
portal for public participation in the rulemaking process — as a set of MCP
tools. Regulations.gov aggregates federal regulatory documents, public comments,
and dockets from all federal agencies.

The server lets an AI application search documents (Rules, Proposed Rules,
Notices, and Other), read individual documents (including the extracted text of
attached PDFs), search and read public comments, and browse the dockets that
group a rulemaking action together — all through natural-language requests
routed through the obot MCP gateway.

- **Data source:** [Regulations.gov API v4](https://open.gsa.gov/api/regulationsgov/)
- **Source repository:** [GSA-TTS/mcp-server-regulations-gov](https://github.com/GSA-TTS/mcp-server-regulations-gov)
- **Runtime:** `containerized` — hosted by the gateway from the public image
  `ghcr.io/gsa-tts/mcp-server-regulations-gov` (`:8080/mcp`, health at `/health`).
  The container has no public route; it is reachable only through the gateway.
- **Server user type:** `singleUser` — each user gets their own isolated
  instance and supplies their own Regulations.gov (api.data.gov) API key.

## Authentication model

Unlike the keyless, public-API servers in this catalog, Regulations.gov requires
a **personal API key** issued through [api.data.gov](https://api.data.gov/). This
server therefore uses `serverUserType: singleUser`. There are **two distinct
credentials on two different hops** — do not conflate them:

| Credential | Hop | Who supplies / enforces it |
|------------|-----|----------------------------|
| Gateway/transport auth (Obot API key) | client → gateway → this server | The **Obot gateway**. The `containerized` server has no public route, so the gateway is the only caller and it enforces access. |
| `REGULATIONS_GOV_API_KEY` | this server → `api.regulations.gov` | Declared in the catalog entry as a **required, sensitive** top-level `env` field. For a `singleUser` deployment, the gateway prompts **each user** for their own key and injects it as an environment variable into **their own** container instance. |

Get a free key at <https://api.data.gov/signup/>. Users are prompted for it when
they enable the server; it is stored securely and used only by their own
instance.

> **Why `singleUser` (not `multiUser`)?** The other public-data catalog servers
> wrap keyless APIs and share one gateway-hosted instance (`multiUser`).
> Regulations.gov requires a per-user upstream credential and enforces per-key
> rate limits, so each user must get an isolated instance — exactly the case
> `singleUser` exists for.

## Tools

The server registers the following tools. The typical workflow is search
dockets → search documents within a docket → read documents and their public
comments.

### Documents

| Tool | Description |
|------|-------------|
| `regulations_search_documents` | Search Rules, Proposed Rules, Notices, and Other documents by keyword, agency, docket, date range, and type. Returns paginated results in Markdown or JSON. Results are capped at 5,000 per query sequence — narrow with date ranges or `docket_id` for larger sets. |
| `regulations_get_document` | Get full metadata for a specific document. With `download_content=True`, discovers all attached PDF file URLs, downloads them, and extracts the full text. |

### Comments

| Tool | Description |
|------|-------------|
| `regulations_search_comments` | Search public comments by keyword, agency, docket, or the document object being commented on (`comment_on_id`). Personally identifiable information is never returned by the API. |
| `regulations_get_comment` | Get the full text and metadata for a single comment. With `include_attachments=True`, lists each attachment's title, format, size, and download URL. |

### Dockets

| Tool | Description |
|------|-------------|
| `regulations_search_dockets` | Search dockets — the top-level unit grouping documents and comments for a rulemaking or nonrulemaking action — by keyword, agency, type, and date range. |
| `regulations_get_docket` | Get full metadata for a single docket including agency, type, RIN, program, keywords, and modification date. |

## Conventions

- **IDs** follow the agency docket convention, e.g. dockets like
  `EPA-HQ-OAR-2021-0257` and documents/comments like
  `EPA-HQ-OAR-2021-0257-0542`.
- **Date formats** are `YYYY-MM-DD` for all date-range filters.
- **Sorting** uses a field name, prefixed with `-` for descending
  (e.g. `-postedDate`, `-modifyDate`).
- **Pagination:** `page_size` (1–250, default 20) and `page_number` (starts at
  1). Responses include pagination metadata.
- **Response format:** every tool accepts `response_format` of `markdown`
  (human-readable, default) or `json` (raw API response).

## Rate limits

- Standard endpoints follow the
  [api.data.gov rate limits](https://api.data.gov/docs/rate-limits/).
- Comment endpoints are limited to **50 requests/minute** and
  **500 requests/hour**.
- A maximum of **5,000 results** is returned per sequential query — use date
  range filters for large datasets.

## Example prompts

- "Find EPA proposed rules about air quality from 2024."
- "Show me the dockets on methane emissions."
- "What public comments were submitted on docket EPA-HQ-OAR-2021-0257?"
- "Get the full text of document FDA-2009-N-0501-0012."
- "Read comment EPA-HQ-OAR-2021-0257-0542 and list its attachments."
- "List recently modified NHTSA rulemaking dockets."

## References

- [Regulations.gov](https://www.regulations.gov)
- [Regulations.gov API documentation](https://open.gsa.gov/api/regulationsgov/)
- [Register for a free API key (api.data.gov)](https://api.data.gov/signup/)
- [Source repository](https://github.com/GSA-TTS/mcp-server-regulations-gov)
- [Model Context Protocol](https://modelcontextprotocol.io/)
