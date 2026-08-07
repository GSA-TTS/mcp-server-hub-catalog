# EIA Open Data MCP Server

> **Status:** Pilot / proof of concept. Not intended for production use.

## Overview

The EIA Open Data MCP server exposes the U.S. Energy Information Administration
(EIA) [Open Data API v2](https://www.eia.gov/opendata/) as a set of MCP tools.
The EIA API is a recursive tree covering all 17 EIA datasets — electricity,
natural gas, petroleum, coal, nuclear outages, CO2 emissions, renewables, and
the energy outlooks (AEO/IEO/STEO).

The server exposes four generic, path-driven tools that mirror the API's
uniform workflow — browse the tree to a leaf dataset, discover its facets and
valid columns, then query rows — giving agents full coverage of the API surface
without hard-coding hundreds of endpoints.

- **Data source:** [EIA Open Data API v2](https://api.eia.gov/v2)
- **Source repository:** [GSA-TTS/mcp-server-eia](https://github.com/GSA-TTS/mcp-server-eia)
- **Runtime:** `containerized` — hosted by the gateway from the public image
  `ghcr.io/gsa-tts/mcp-server-eia` (`:8080/mcp`, health at `/health`).
  The container has no public route; it is reachable only through the gateway.
- **Server user type:** `singleUser` — each user gets their own isolated
  instance and supplies their own EIA API key.

## Authentication model

Unlike the other (keyless, public-API) servers in this catalog, EIA requires a
**personal API key**. This server therefore uses `serverUserType: singleUser`.
There are **two distinct credentials on two different hops** — do not conflate
them:

| Credential | Hop | Who supplies / enforces it |
|------------|-----|----------------------------|
| Gateway/transport auth (Obot API key) | client → gateway → this server | The **Obot gateway**. The `containerized` server has no public route, so the gateway is the only caller and it enforces access. The server sets no FastMCP `auth` provider. |
| `EIA_API_KEY` | this server → `api.eia.gov` | Declared in the catalog entry as a **required, sensitive** `containerizedConfig.env` field. For a `singleUser` deployment, the gateway prompts **each user** for their own key and injects it as an environment variable into **their own** container instance. |

Get a free key at <https://www.eia.gov/opendata/register.php>. Users are
prompted for it when they enable the server; it is stored securely and used only
by their own instance.

> **Why `singleUser` (not `multiUser`)?** The other catalog servers wrap public,
> keyless APIs and share one gateway-hosted instance (`multiUser`). EIA requires
> a per-user upstream credential, so each user must get an isolated instance —
> exactly the case `singleUser` exists for.

## Tools

The server registers the following tools. The EIA API is a recursive tree: a
GET on a route returns **either** child routes (an intermediate node) **or**
leaf metadata (a queryable dataset). The typical workflow is browse → list
facets → get facet options → get data.

### Discovery

| Tool | Description |
|------|-------------|
| `eia_browse_routes` | Explore the dataset tree from any path (empty string = the 17 top-level datasets). At a leaf, returns dataset metadata: available frequencies, facet ids, valid `data` columns, and the covered date range. Primary discovery tool. |
| `eia_list_facets` | List the facet ids a dataset can be filtered by (e.g. `stateid`, `sectorid`, `fueltypeid`). |
| `eia_get_facet_options` | List the valid option values for a single facet, so filters use real ids. |

### Query

| Tool | Description |
|------|-------------|
| `eia_get_data` | Query dataset rows with column selection, facet filters, frequency, date range, sorting, and pagination. Returns structured JSON with pagination metadata (`total`, `offset`, `length`, `returned`, `has_more`, `next_offset`). |

## Conventions

- **Routes** are slash paths without a `v2/` prefix, e.g.
  `electricity/retail-sales`.
- **Date formats** depend on frequency: `2020` (annual), `2020-01` (monthly),
  `2020-01-01` (daily), `2020-01-01T00` (hourly).
- **Facets** are passed as `{facet_id: [values]}`; **sort** as
  `[{"column": ..., "direction": "asc"|"desc"}]`.
- **Pagination:** `length` (page size, max 5000) and `offset`; reuse the
  `next_offset` returned by the previous `eia_get_data` response.
- Always confirm valid `data` columns via `eia_browse_routes` before calling
  `eia_get_data`, or the API may return empty rows.

## Example prompts

- "List the top-level EIA datasets, then show the columns and frequencies for electricity retail sales."
- "What can I filter the electricity/retail-sales dataset by?"
- "Get monthly residential electricity price for California from 2020 to 2023."
- "Show annual U.S. total energy CO2 emissions for the last 10 years."

## References

- [EIA Open Data](https://www.eia.gov/opendata/)
- [EIA API v2 endpoint](https://api.eia.gov/v2)
- [Register for a free EIA API key](https://www.eia.gov/opendata/register.php)
- [Source repository](https://github.com/GSA-TTS/mcp-server-eia)
- [Model Context Protocol](https://modelcontextprotocol.io/)
