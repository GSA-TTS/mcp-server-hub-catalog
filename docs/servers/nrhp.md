# NEPA NRHP MCP Server

> **Status:** Pilot / proof of concept. Not intended for production use.
>
> **Migration status (2026-10-20):** the digest-pinned NRHP application passed
> cloud.gov startup, internal-only route metadata, port-scoped C2C policy,
> gateway-to-`/health` reachability, and the supplemental public HTTP negative
> probe. Catalog synchronization, authenticated vMCP `tools/list`, a real
> `tools/call`, and external-client verification remain pending.

## Overview

The NRHP MCP server exposes the National Register of Historic Places (NRHP) as
an MCP tool built for Section 106 of the National Historic Preservation Act
(NHPA) and cultural-resource screening in NEPA analyses. Given a
latitude/longitude and a buffer radius, it identifies NRHP-listed historic
properties — including National Historic Landmarks (NHL) — within a region of
interest (ROI), all through natural-language requests routed through the obot
MCP gateway.

The data is served by the National Park Service Cultural Resources ArcGIS
MapServer.

- **Data source:** NPS Cultural Resources ArcGIS MapServer (National Register of
  Historic Places).
- **Source repository:** [GSA-TTS/nepa-mcp](https://github.com/GSA-TTS/nepa-mcp)
  (a fork of [pnnl/nepa-mcp](https://github.com/pnnl/nepa-mcp); the NRHP server
  is containerized additively under `docker/nrhp/`).
- **Runtime:** an internal cloud.gov application registered as a `remote`
  component and exposed to users through the NEPA NRHP vMCP. A port-scoped C2C
  policy permits the gateway to reach `:8080/mcp`; the application has no
  public route.
- **Client access:** authenticated through the gateway at
  `/mcp-connect/<vmcp-id>` with no `/mcp` suffix.
- **Authentication:** None required — queries the public NPS service.

## Design principles

The server returns compact, decision-oriented **evidence**, not raw ArcGIS
payloads:

- Results are returned as a Markdown summary of the NRHP-listed properties
  intersecting the ROI, oriented to Section 106 review.
- Results support early screening but do not replace identification of historic
  properties, eligibility evaluation, effects findings, consultation, or other
  official Section 106 responsibilities.

## Tools

The server registers the following tool.

| Tool | Description |
|------|-------------|
| `get_nrhp_properties_in_roi` | NRHP-listed historic properties (including National Historic Landmarks) within the ROI, from the NPS Cultural Resources service. |

## Parameters

### `get_nrhp_properties_in_roi`

| Parameter | Description |
|-----------|-------------|
| `latitude` | Latitude in decimal degrees (WGS84), valid range -90 to 90. |
| `longitude` | Longitude in decimal degrees (WGS84), valid range -180 to 180. |
| `buffer_miles` | Optional. Buffer distance in miles, valid range 0.1 to 100.0 (default 25). |

## Example prompts

- "What historic properties are listed within 25 miles of 38.9, -77.0?"
- "Screen this site for NRHP properties near latitude 29.95, longitude -90.07."
- "Are there any National Historic Landmarks around this location?"

## References

- [National Register of Historic Places](https://www.nps.gov/subjects/nationalregister/index.htm)
- [Section 106 of the National Historic Preservation Act](https://www.achp.gov/protecting-historic-properties/section-106-process/introduction-section-106)
- [Source repository](https://github.com/GSA-TTS/nepa-mcp)
- [Upstream project (PNNL)](https://github.com/pnnl/nepa-mcp)
- [Model Context Protocol](https://modelcontextprotocol.io/)
