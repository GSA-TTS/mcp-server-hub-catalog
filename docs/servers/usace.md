# NEPA USACE MCP Server

> **Status:** Pilot / proof of concept. Not intended for production use.

## Overview

The USACE MCP server exposes U.S. Army Corps of Engineers (USACE) regulatory
data as a set of MCP tools built for Section 404 Clean Water Act compliance and
jurisdictional screening in NEPA analyses. Given a latitude/longitude and a
buffer radius, it identifies the USACE district with regulatory jurisdiction
over a region of interest (ROI) and the applicable wetland delineation regions
and subregions, all through natural-language requests routed through the obot
MCP gateway.

> **Not to be confused with** the separate [USACE IWR River Mile Markers](usace_iwr.md)
> catalog entry (`obot-usace-iwr`), which locates navigable-river mile markers.
> This entry (`obot-nepa-usace`, image `mcp-server-nepa-usace`) is the NEPA
> fork's regulatory/jurisdiction server and exposes a different tool set.

- **Data source:** U.S. Army Corps of Engineers regulatory ArcGIS services
  (districts and wetland delineation regions/subregions).
- **Source repository:** [GSA-TTS/nepa-mcp](https://github.com/GSA-TTS/nepa-mcp)
  (a fork of [pnnl/nepa-mcp](https://github.com/pnnl/nepa-mcp); the USACE server
  is containerized additively under `docker/usace/`).
- **Runtime:** `containerized` — hosted by the gateway from the public image
  `ghcr.io/gsa-tts/mcp-server-nepa-usace` (`:8080/mcp`, health at `/health`).
  The container has no public route; it is reachable only through the gateway.
- **Authentication:** None required — queries the public USACE services.

## Design principles

The server returns compact, decision-oriented **evidence**, not raw ArcGIS
payloads:

- Each tool returns a Markdown summary keyed to the ROI.
- The analysis tool combines district, region, and subregion data into a
  one-shot Section 404 jurisdictional screen.

## Tools

The server registers the following tools.

| Tool | Description |
|------|-------------|
| `get_usace_regulatory_district` | USACE district with jurisdiction over the ROI (name, abbreviation, division, website). |
| `get_usace_wetland_regions_in_roi` | Broad USACE Regional Supplement wetland delineation regions within the ROI. |
| `get_usace_wetland_subregions_in_roi` | Finer MLRA-based wetland subregions nested under the Regional Supplement regions. |
| `analyze_usace_jurisdiction` | One-shot Section 404 jurisdictional analysis combining district, region, and subregion data. |

## Parameters

All four tools take the same parameters.

| Parameter | Description |
|-----------|-------------|
| `latitude` | Latitude in decimal degrees (WGS84), valid range -90 to 90. |
| `longitude` | Longitude in decimal degrees (WGS84), valid range -180 to 180. |
| `buffer_miles` | Optional. Buffer distance in miles, valid range 0.1 to 100.0 (default 25). |

## Example prompts

- "Which USACE district regulates the area within 25 miles of 38.9, -77.0?"
- "What wetland delineation region applies near latitude 30.3, longitude -97.7?"
- "Run a Section 404 jurisdictional analysis for this site."

## References

- [USACE Regulatory Program](https://www.usace.army.mil/Missions/Civil-Works/Regulatory-Program-and-Permits/)
- [Section 404 of the Clean Water Act](https://www.epa.gov/cwa-404)
- [USACE Wetland Delineation Regional Supplements](https://www.usace.army.mil/Missions/Civil-Works/Regulatory-Program-and-Permits/reg_supp/)
- [Source repository](https://github.com/GSA-TTS/nepa-mcp)
- [Upstream project (PNNL)](https://github.com/pnnl/nepa-mcp)
- [Model Context Protocol](https://modelcontextprotocol.io/)
