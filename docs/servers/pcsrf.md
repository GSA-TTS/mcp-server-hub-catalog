# NEPA NOAA PCSRF MCP Server

> **Status:** Pilot / proof of concept. Not intended for production use.
>
> **Migration status (2026-10-20):** the digest-pinned PCSRF application passed
> cloud.gov startup, internal-only route metadata, port-scoped C2C policy,
> gateway-to-`/health` reachability, and the supplemental public HTTP negative
> probe. Catalog synchronization, authenticated vMCP `tools/list`, a real
> `tools/call`, and external-client verification remain pending.

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
- **Runtime:** an internal cloud.gov application registered as a `remote`
  component and exposed to users through the NEPA NOAA PCSRF vMCP. A
  port-scoped C2C policy permits the gateway to reach `:8080/mcp`; the
  application has no public route.
- **Client access:** authenticated through the gateway at
  `/mcp-connect/<vmcp-id>` with no `/mcp` suffix.
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
- Atlantic salmon EFH/HAPC is not Pacific salmon or PCSRF project data, and
  PCSRF project records describe funded work rather than regulatory
  determinations.

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
