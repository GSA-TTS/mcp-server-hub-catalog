# NEPA EPA AQS MCP Server

> **Status:** Pilot / proof of concept. Not intended for production use.

## Overview

The EPA AQS MCP server exposes the U.S. Environmental Protection Agency Air
Quality System (AQS) as a set of MCP tools built for NEPA/EIS air quality
baseline assessments. Given a latitude/longitude and a buffer radius, it
identifies criteria-pollutant monitoring stations, retrieves annual air quality
statistics, and screens observed values against selected National Ambient Air
Quality Standards (NAAQS) — all through natural-language requests routed through
the obot MCP gateway.

- **Data source:** [EPA Air Quality System (AQS) API](https://aqs.epa.gov/aqsweb/documents/data_api.html)
- **Source repository:** [GSA-TTS/nepa-mcp](https://github.com/GSA-TTS/nepa-mcp)
  (a fork of [pnnl/nepa-mcp](https://github.com/pnnl/nepa-mcp); the EPA AQS
  server is containerized additively under `docker/epa_aqs/`).
- **Runtime:** `containerized` — hosted by the gateway from the public image
  `ghcr.io/gsa-tts/mcp-server-nepa-epa-aqs` (`:8080/mcp`, health at `/health`).
  The container has no public route; it is reachable only through the gateway.
- **Authentication:** Per-user **EPA AQS credentials** (`EPA_AQS_EMAIL` and
  `EPA_AQS_API_KEY`). This is a `singleUser` server — each user supplies their
  own free registration, injected into their own isolated instance at runtime.

## Setup

Register for free EPA AQS API access at
[aqs.epa.gov/data/api/signup](https://aqs.epa.gov/data/api/signup). You will
receive an email/API-key pair. When you enable the server in the gateway, you
will be prompted for both; they are stored securely and used only by your own
isolated instance. They are never baked into the image.

## Design principles

The server returns compact, decision-oriented **evidence**, not raw AQS
payloads:

- Results are returned as Markdown summaries keyed to the monitors and
  pollutants in the ROI.
- Annual statistics include screening comparisons against selected NAAQS values
  for baseline context.

## Tools

The server registers the following tools.

| Tool | Description |
|------|-------------|
| `get_epa_aqs_air_quality_monitors` | Identify EPA air quality monitoring stations within the ROI, with operational dates and measured pollutants. |
| `get_epa_aqs_annual_air_quality` | Annual air quality statistics (means, maximums) for criteria pollutants in the ROI, with NAAQS screening comparisons. |
| `analyze_epa_aqs_air_quality_baseline` | One-shot baseline analysis combining monitor discovery, annual statistics, and NAAQS screening into a single report. |

## Parameters

| Parameter | Description |
|-----------|-------------|
| `latitude` | Latitude in decimal degrees (WGS84), valid range -90 to 90. |
| `longitude` | Longitude in decimal degrees (WGS84), valid range -180 to 180. |
| `buffer_miles` | Optional. Buffer distance in miles, valid range 0.1 to 100.0 (default 25). |
| `year` | Optional (monitors tool). Year to query for active monitors (default current year). |
| `begin_year` / `end_year` | Optional (annual/baseline tools). Year range to query (default last year). |
| `pollutants` | Optional. Subset of {PM2.5, PM10, Ozone, NO2, SO2, CO} (default all). |

## Example prompts

- "What air quality monitors are within 25 miles of 34.05, -118.24?"
- "Get annual PM2.5 and Ozone statistics near latitude 39.7, longitude -104.9 for 2020-2022."
- "Run an air quality baseline analysis for this site with NAAQS screening."

## References

- [EPA Air Quality System (AQS) API documentation](https://aqs.epa.gov/aqsweb/documents/data_api.html)
- [EPA AQS API signup](https://aqs.epa.gov/data/api/signup)
- [National Ambient Air Quality Standards (NAAQS)](https://www.epa.gov/criteria-air-pollutants/naaqs-table)
- [Source repository](https://github.com/GSA-TTS/nepa-mcp)
- [Upstream project (PNNL)](https://github.com/pnnl/nepa-mcp)
- [Model Context Protocol](https://modelcontextprotocol.io/)
