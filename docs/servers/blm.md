# NEPA BLM MCP Server

> **Status:** Pilot / proof of concept. Not intended for production use.

## Overview

The BLM MCP server exposes U.S. Bureau of Land Management (BLM) geospatial data
used in NEPA environmental screening as a set of MCP tools. Given a
latitude/longitude and a buffer radius, it screens a region of interest (ROI)
against three BLM datasets — approved land use plans, designated wilderness
areas, and National Monuments / National Conservation Areas — all through
natural-language requests routed through the obot MCP gateway.

The datasets are published as
[Esri ArcGIS REST FeatureServers](https://services1.arcgis.com/KbxwQRRfWyEYLgp4/arcgis/rest/services)
hosted by BLM.

- **Data sources:**
  - [BLM National Approved Land Use Plans (2022)](https://services1.arcgis.com/KbxwQRRfWyEYLgp4/arcgis/rest/services/BLM_Natl_Land_Use_Plans_Approved_2022/FeatureServer)
  - [BLM National NLCS Wilderness Areas](https://services1.arcgis.com/KbxwQRRfWyEYLgp4/arcgis/rest/services/BLM_Natl_NLCS_Wilderness_Areas_Polygons/FeatureServer)
  - [BLM National NLCS National Monuments & National Conservation Areas](https://services1.arcgis.com/KbxwQRRfWyEYLgp4/arcgis/rest/services/BLM_Natl_NLCS_National_Monuments_National_Conservation_Areas_Polygons/FeatureServer)
- **Source repository:** [GSA-TTS/nepa-mcp](https://github.com/GSA-TTS/nepa-mcp)
  (a fork of [pnnl/nepa-mcp](https://github.com/pnnl/nepa-mcp); the BLM server
  is containerized additively under `docker/blm/`).
- **Runtime:** `containerized` — hosted by the gateway from the public image
  `ghcr.io/gsa-tts/mcp-server-nepa-blm` (`:8080/mcp`, health at `/health`).
  The container has no public route; it is reachable only through the gateway.
- **Authentication:** None required — queries the public BLM ArcGIS services.

## Design principles

The server returns compact, decision-oriented **evidence**, not raw ArcGIS
payloads:

- Each tool returns a Markdown summary that lists the intersecting features with
  their key attributes and adds a short NEPA compliance note.
- Only named `outFields` are requested from the upstream service, keeping
  responses stable and minimal.
- Polygon areas are normalized to square miles; wilderness designation dates are
  converted from ArcGIS epoch-millisecond timestamps to ISO `YYYY-MM-DD`.

## Tools

The server registers the following tools.

| Tool | Description |
|------|-------------|
| `get_blm_land_use_plans_in_roi` | Identify BLM approved land use plans (RMPs/MFPs) intersecting the ROI. Returns plan name, status, ROD date/year, admin state, NEPA number, and ePlanning links for conformance checks per 43 CFR 1610.5. |
| `get_blm_wilderness_areas_in_roi` | Identify BLM designated wilderness areas (Wilderness Act of 1964) intersecting the ROI. Returns name, NLCS ID, designation date, and area. Supports Extraordinary Circumstances screening. |
| `get_blm_national_monuments_in_roi` | Identify BLM National Monuments and National Conservation Areas (NCAs) intersecting the ROI. Returns name, NLCS ID, admin state, and area — special designations carrying management restrictions. |

## Parameters

All three tools take the same parameters.

| Parameter | Description |
|-----------|-------------|
| `latitude` | Latitude in decimal degrees (WGS84), valid range -90 to 90. |
| `longitude` | Longitude in decimal degrees (WGS84), valid range -180 to 180. |
| `buffer_miles` | Optional. Buffer distance in miles, valid range 0.1 to 100.0 (default 25). |

## Example prompts

- "What BLM land use plans apply within 25 miles of 39.06, -108.55?"
- "Are there any BLM wilderness areas near latitude 38.5, longitude -109.5?"
- "List BLM National Monuments and NCAs within 50 miles of this site."

## References

- [BLM National ArcGIS REST services](https://services1.arcgis.com/KbxwQRRfWyEYLgp4/arcgis/rest/services)
- [43 CFR 1610.5 — Land use plan conformance](https://www.ecfr.gov/current/title-43/subtitle-B/chapter-II/subchapter-A/part-1600)
- [Source repository](https://github.com/GSA-TTS/nepa-mcp)
- [Upstream project (PNNL)](https://github.com/pnnl/nepa-mcp)
- [Model Context Protocol](https://modelcontextprotocol.io/)
