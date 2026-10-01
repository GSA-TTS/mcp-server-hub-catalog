# SAM.gov MCP Server

> **Status:** Pilot / proof of concept. Not intended for production use.

## Overview

The SAM.gov MCP server exposes [SAM.gov](https://sam.gov) — the U.S.
government's System for Award Management — as a set of MCP tools. It combines
two SAM.gov public APIs in a single server:

- **Get Opportunities API** — pre-award notices (solicitations, sources sought,
  award notices, special notices, combined synopsis/solicitations, etc.).
- **Contract Awards API** — executed contract actions and their modifications.

The server lets an AI application search contracting opportunities, read full
opportunity details and descriptions, search awarded contracts, and retrieve
individual contracts or entire contract families — all through natural-language
requests routed through the obot MCP gateway.

- **Data source:** [SAM.gov Get Opportunities Public API](https://open.gsa.gov/api/get-opportunities-public-api/)
  and [SAM.gov Contract Awards API](https://open.gsa.gov/api/contract-awards/)
- **Source repository:** [GSA-TTS/sam-gov-mcp-server](https://github.com/GSA-TTS/sam-gov-mcp-server)
- **Runtime:** `containerized` — hosted by the gateway from the public image
  `ghcr.io/gsa-tts/mcp-server-sam-gov` (`:8080/mcp`, health at `/health`).
  The container has no public route; it is reachable only through the gateway.
- **Server user type:** `singleUser` — each user gets their own isolated
  instance and supplies their own SAM.gov public API key.

## Authentication model

Unlike the keyless, public-API servers in this catalog, SAM.gov requires a
**personal public API key** issued from a SAM.gov account. This server therefore
uses `serverUserType: singleUser`. There are **two distinct credentials on two
different hops** — do not conflate them:

| Credential | Hop | Who supplies / enforces it |
|------------|-----|----------------------------|
| Gateway/transport auth (Obot API key) | client → gateway → this server | The **Obot gateway**. The `containerized` server has no public route, so the gateway is the only caller and it enforces access. |
| `SAM_GOV_API_KEY` | this server → `api.sam.gov` | Declared in the catalog entry as a **required, sensitive** top-level `env` field. For a `singleUser` deployment, the gateway prompts **each user** for their own key and injects it as an environment variable into **their own** container instance. |

Get a free key by signing in at <https://sam.gov> and opening
**Account Details > Public API Key**. Users are prompted for it when they enable
the server; it is stored securely and used only by their own instance.

> **Why `singleUser` (not `multiUser`)?** The other public-data catalog servers
> wrap keyless APIs and share one gateway-hosted instance (`multiUser`). SAM.gov
> requires a per-user upstream credential and enforces per-key rate limits, so
> each user must get an isolated instance — exactly the case `singleUser` exists
> for.

## Tools

### Opportunities

| Tool | Description |
|------|-------------|
| `search_opportunities` | Search pre-award notices with filters: posted-date range (required, max 1 year), procurement type, NAICS code, set-aside type, agency, place of performance (state/zip), title keywords, solicitation number, and response-deadline range. Returns summarized results with pagination info. |
| `get_opportunity_details` | Get full details for a single opportunity by notice ID — contacts, award info, place of performance, office address, and resource links. |
| `get_opportunity_description` | Fetch the full text description of an opportunity (served from a separate `/v1/noticedesc` endpoint). |

### Contract Awards

| Tool | Description |
|------|-------------|
| `search_contract_awards` | Search awarded contracts with filters: date signed, fiscal year, dollars obligated, NAICS code, awardee name/UEI, CAGE, contracting agency, set-aside type, place of performance, and free text. Returns a summarized list with pagination info. |
| `get_contract_details` | Get the full contract record for a single award by its PIID, optionally a specific modification/transaction. |
| `get_contract_family` | Get the full contract family for a PIID — base award plus all modifications — via PIID aggregation. |

## Conventions

- **Date format:** all dates use `MM/DD/YYYY`.
- **Opportunities date-range limits:** the `posted_from`/`posted_to` and
  response-deadline (`rdlfrom`/`rdlto`) ranges cannot exceed 1 year.
- **Procurement type codes** (`ptype`): `u`=Justification, `p`=Pre-solicitation,
  `a`=Award Notice, `r`=Sources Sought, `s`=Special Notice, `o`=Solicitation,
  `g`=Sale of Surplus, `k`=Combined Synopsis/Solicitation, `i`=Intent to Bundle.
- **Set-aside filter:** accepts a single value (e.g. `SBA`, `8A`, `HZC`,
  `SDVOSBC`, `WOSB`).
- **Pagination:** opportunities use `limit` (1–1000, default 25) and `offset`
  (0-indexed); contract awards use `limit` (1–100, default 25) and `offset`.
- **Contract-award ranges:** date ranges use `[MM/DD/YYYY,MM/DD/YYYY]` and dollar
  ranges use `[lower,upper]` (numbers, no commas). Multi-value identifiers are
  separated with `~` (max 100).

## Example prompts

- "Find open IT solicitations set aside for small business posted in the last 30 days."
- "Show me sources-sought notices for NAICS 541512 in California."
- "Get the full description for notice ID <noticeId>."
- "Find contract awards to UEI <uei> signed in FY2024 over $1M."
- "Show the full contract family for PIID <piid>."

## References

- [SAM.gov](https://sam.gov)
- [Get Opportunities Public API](https://open.gsa.gov/api/get-opportunities-public-api/)
- [Contract Awards API](https://open.gsa.gov/api/contract-awards/)
- [Source repository](https://github.com/GSA-TTS/sam-gov-mcp-server)
- [Model Context Protocol](https://modelcontextprotocol.io/)
