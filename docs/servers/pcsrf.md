# NEPA NOAA PCSRF MCP Server

> **Status:** Pilot / proof of concept. Not intended for production use.

## Overview

The PCSRF MCP server exposes NOAA Fisheries data centered on the Pacific Coastal
Salmon Recovery Fund (PCSRF) as a set of MCP tools built for ESA Section 7
consultation and Magnuson-Stevens Act compliance screening in NEPA analyses.
Given a latitude/longitude and a buffer radius, it screens a region of interest
(ROI) against NOAA all-species ranges, a NOAA critical-habitat snapshot,
Atlantic salmon EFH/HAPC, and PCSRF salmon-recovery projects — all through
natural-language requests routed through the obot MCP gateway.

- **Data source:** NOAA Fisheries ArcGIS services (species ranges, critical
  habitat, EFH/HAPC, and PCSRF projects).
- **Source repository:** [GSA-TTS/nepa-mcp](https://github.com/GSA-TTS/nepa-mcp)
  (a fork of [pnnl/nepa-mcp](https://github.com/pnnl/nepa-mcp); the PCSRF server
  is containerized additively under `docker/pcsrf/`).
- **Runtime:** `containerized` — hosted by the gateway from the public image
  `ghcr.io/gsa-tts/mcp-server-nepa-noaa-pcsrf` (`:8080/mcp`, health at
  `/health`). The container has no public route; it is reachable only through
  the gateway.
- **Authentication:** None required — queries the public NOAA services.

## Related servers

This server bundles several NOAA datasets around salmon recovery. For focused
single-dataset screening see also the NEPA NOAA Critical Habitat server (West
Coast critical habitat), NEPA EFH (essential fish habitat), and NEPA ESA Ranges
(ESA-listed species ranges).

## Design principles

The server returns compact, decision-oriented **evidence**, not raw ArcGIS
payloads:

- Each tool returns a Markdown summary of the features intersecting the ROI.
- Polygon area is unioned and clipped to the requested point-buffer ROI;
  upstream whole-feature area and line-length attributes remain distinguishable.
- The critical-habitat snapshot is a 2021-09-04 generalized dataset — confirm
  current designations with agency sources before relying on results.

## Tools

The server registers the following tools.

| Tool | Description |
|------|-------------|
| `get_noaa_all_species_ranges_in_roi` | NOAA Fisheries All_Species_Ranges records within the ROI (not PCSRF project data). |
| `get_noaa_critical_habitat_20210904_in_roi` | NOAA critical-habitat snapshot (2021-09-04) for NOAA-managed species within the ROI. |
| `get_atlantic_salmon_efh_hapc_in_roi` | Atlantic salmon EFH/HAPC buffer zones within the ROI (Atlantic, not Pacific, salmon). |
| `get_pcsrf_projects_in_roi` | Pacific Coastal Salmon Recovery Fund restoration/monitoring/habitat projects within the ROI. |

## Parameters

All four tools take the same parameters.

| Parameter | Description |
|-----------|-------------|
| `latitude` | Latitude in decimal degrees (WGS84), valid range -90 to 90. |
| `longitude` | Longitude in decimal degrees (WGS84), valid range -180 to 180. |
| `buffer_miles` | Optional. Buffer distance in miles, valid range 0.1 to 100.0 (default 25). |

## Example prompts

- "What NOAA species ranges are within 25 miles of 45.5, -122.6?"
- "Show designated critical habitat near latitude 47.6, longitude -122.3."
- "Are there PCSRF salmon recovery projects around this site?"

## References

- [Pacific Coastal Salmon Recovery Fund (PCSRF)](https://www.fisheries.noaa.gov/grant/pacific-coastal-salmon-recovery-fund)
- [NOAA Fisheries — Critical Habitat](https://www.fisheries.noaa.gov/national/endangered-species-conservation/critical-habitat)
- [Source repository](https://github.com/GSA-TTS/nepa-mcp)
- [Upstream project (PNNL)](https://github.com/pnnl/nepa-mcp)
- [Model Context Protocol](https://modelcontextprotocol.io/)
