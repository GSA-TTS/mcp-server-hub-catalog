# CDC PLACES MCP Server

> **Status:** Pilot / proof of concept. Not intended for production use. Always
> verify critical health data against official CDC sources.

## Overview

The CDC PLACES MCP server exposes the
[CDC PLACES dataset](https://www.cdc.gov/places/index.html) as MCP tools. PLACES
provides model-based estimates for chronic disease risk factors, health
outcomes, and clinical preventive service use across US geographic areas — all
50 states, the District of Columbia, counties, census tracts, ZCTAs, and 500 of
the largest US cities and census places.

The server lets an AI application look up health measures for specific locations
and compute summary statistics across geographic areas, through natural-language
requests routed through the obot MCP gateway.

- **Data source:** [CDC PLACES API (data.cdc.gov)](https://www.cdc.gov/places/index.html)
- **Source repository:** [GSA-TTS/cdc-places-mcp-server](https://github.com/GSA-TTS/cdc-places-mcp-server)
- **Gateway endpoint:** `https://cdc-places-mcp-server.app.cloud.gov/mcp`
- **Authentication:** None required — queries the public CDC PLACES API.
- **Latest data:** PLACES Release 2025 (2023 BRFSS data for most measures);
  releases 2020–2025 (PLACES) and 2016–2019 (500 Cities).

## Tools

### `get_cdc_places_data`

Fetch health data for a specific measure, location, and time period.

| Parameter | Type | Description |
|-----------|------|-------------|
| `year` | string | Year of the data release (e.g. `"2023"`, `"2022"`). |
| `measureid` | enum | Health measure identifier (e.g. `CSMOKING`, `DIABETES`, `OBESITY`). |
| `geo` | literal | Geographic level: `state`, `county`, `census`, `zcta`, or `places`. |
| `datavaluetypeid` | literal | `CrdPrv` (crude prevalence) or `AgeAdjPrv` (age-adjusted prevalence). |
| `locationname` | string (optional) | Location name (e.g. `"Wayne"` for Wayne County). |

Example: *"Get smoking rates for Wayne County, Michigan in 2023."*

### `area_summary_stats`

Calculate summary statistics across multiple geographic areas within a scope.

| Parameter | Type | Description |
|-----------|------|-------------|
| `geo_scope` | literal | `counties_in_state`, `tracts_in_county`, or `places_in_state`. |
| `state_code` | string | Two-letter state abbreviation (e.g. `CA`, `MI`). |
| `year` | string | Year of the data release. |
| `measureid` | enum | Health measure identifier. |
| `datavaluetypeid` | literal | `CrdPrv` or `AgeAdjPrv`. |
| `county` | string (optional) | County name (required for `tracts_in_county` scope). |

**Returns:** count, mean, min, Q1, median, Q3, and max, with location
attribution for the point statistics.

Example: *"Get obesity statistics across all counties in California for 2023."*

## Supported health measures (45 total)

The server supports 45 measures across 6 categories:

- **Health Outcomes (13):** ARTHRITIS, BPHIGH, CANCER, CASTHMA, CHD, COPD,
  DEPRESSION, DIABETES, HIGHCHOL, KIDNEY, OBESITY, STROKE, TEETHLOST
- **Health Risk Behaviors (4):** BINGE, CSMOKING, LPA, SLEEP
- **Health Status (3):** GHLTH, MHLTH, PHLTH
- **Prevention (10):** ACCESS2, BPMED, CERVICAL, CHECKUP, CHOLSCREEN,
  COLON_SCREEN, COREM, COREW, DENTAL, MAMMOUSE
- **Disability (8):** HEARING, VISION, COGNITION, MOBILITY, SELFCARE, INDEPLIVE,
  DISABILITY
- **Health-Related Social Needs (7):** ISOLATION, FOODSTAMP, FOODINSECU,
  HOUSINSECU, SHUTUTILITY, LACKTRPT, EMOTIONSPT, LONELINESS

*New in the 2025 release:* the LONELINESS measure.

## Data limitations

- Some measures are collected only in odd years (BPHIGH, HIGHCHOL, CHOLSCREEN,
  BPMED) or only in even years (TEETHLOST, SLEEP, DENTAL, MAMMOUSE, etc.).
- Some measures were discontinued after specific releases (KIDNEY after 2023;
  CERVICAL, COREM, COREW after 2023).
- Estimates are model-based; verify critical figures against official CDC
  sources.

## Example prompts

- "What are the diabetes rates in Los Angeles County for 2023?"
- "Show me obesity statistics across all counties in Texas."
- "Compare smoking rates between Wayne County, Michigan and Cook County,
  Illinois."
- "Get summary statistics for depression across all census tracts in Worcester
  County, Massachusetts."

## References

- [CDC PLACES dataset](https://www.cdc.gov/places/index.html)
- [CDC PLACES Data Dictionary](https://data.cdc.gov/500-Cities-Places/PLACES-Data-Dictionary/wb67-qxck)
- [Source repository](https://github.com/GSA-TTS/cdc-places-mcp-server)
- [Model Context Protocol](https://modelcontextprotocol.io/)
