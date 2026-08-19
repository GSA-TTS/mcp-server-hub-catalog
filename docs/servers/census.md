# Census MCP Server

> **Status:** Pilot / proof of concept. Not intended for production use.

## Overview

The Census MCP server exposes U.S. Census Bureau American Community Survey
(ACS) 5-Year Estimates as an MCP tool for NEPA environmental analysis. Given a
latitude/longitude and a buffer radius, it identifies the counties intersecting
the region of interest (ROI) and returns their socioeconomic indicators — the
kind of data used to establish socioeconomic baseline conditions in a NEPA
analysis — all through natural-language requests routed through the obot MCP
gateway.

- **Data source:** [U.S. Census Bureau American Community Survey (ACS) 5-Year Estimates](https://www.census.gov/programs-surveys/acs)
- **Source repository:** [GSA-TTS/nepa-mcp](https://github.com/GSA-TTS/nepa-mcp)
  (a fork of [pnnl/nepa-mcp](https://github.com/pnnl/nepa-mcp); the Census
  server is containerized additively under `docker/census/`).
- **Runtime:** `containerized` — hosted by the gateway from the public image
  `ghcr.io/gsa-tts/mcp-server-census` (`:8080/mcp`, health at `/health`).
  The container has no public route; it is reachable only through the gateway.
- **Authentication:** Per-user **Census API key** (`CENSUS_API_KEY`). This is a
  `singleUser` server — each user supplies their own free key, injected into
  their own isolated instance at runtime.

## Setup

Register for a free Census API key at
[api.census.gov/data/key_signup.html](https://api.census.gov/data/key_signup.html).
When you enable the server in the gateway, you will be prompted for the key; it
is stored securely and used only by your own isolated instance. It is never
baked into the image.

## Design principles

The server returns compact, decision-oriented **evidence**, not raw Census API
payloads:

- Results are keyed to the counties that intersect the ROI buffer and returned
  as a Markdown summary.
- Optional industry/occupation detail is off by default and bounded by `top_n`
  to keep responses context-window friendly.

## Tools

The server registers the following tool.

| Tool | Description |
|------|-------------|
| `get_acs_socioeconomic_indicators_in_roi` | Query ACS socioeconomic indicators for the counties within a buffered ROI. Returns economic indicators (income, poverty, unemployment) and labor statistics per county as a Markdown summary, optionally including top industries/occupations. |

## Parameters

### `get_acs_socioeconomic_indicators_in_roi`

| Parameter | Description |
|-----------|-------------|
| `latitude` | Latitude in decimal degrees (WGS84), valid range -90 to 90. |
| `longitude` | Longitude in decimal degrees (WGS84), valid range -180 to 180. |
| `buffer_miles` | Optional. Buffer distance in miles, valid range 0.1 to 100.0 (default 25). |
| `include_industries` | Optional. Include top industries/occupations data (default false). |
| `top_n` | Optional. Number of top industries/occupations per county, valid range 1 to 10 (default 2). |

## Example prompts

- "What are the socioeconomic baseline conditions within 25 miles of 39.06, -108.55?"
- "Show income, poverty, and unemployment for counties near latitude 38.5, longitude -109.5."
- "Include the top 3 industries and occupations per county for this ROI."

## References

- [U.S. Census Bureau American Community Survey](https://www.census.gov/programs-surveys/acs)
- [Census API key signup](https://api.census.gov/data/key_signup.html)
- [Source repository](https://github.com/GSA-TTS/nepa-mcp)
- [Upstream project (PNNL)](https://github.com/pnnl/nepa-mcp)
- [Model Context Protocol](https://modelcontextprotocol.io/)
