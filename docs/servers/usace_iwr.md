# USACE IWR River Mile Markers MCP Server

> **Status:** Pilot / proof of concept. Not intended for production use.

## Overview

The USACE IWR River Mile Markers MCP server exposes the U.S. Army Corps of
Engineers (USACE) Institute for Water Resources (IWR)
[River Mile Markers](https://www.arcgis.com/home/item.html?id=604cdc08fe7d43cb90a0584a0b198875)
dataset as a set of MCP tools. River mile markers are reference points along
navigable U.S. rivers, and the dataset is published as an
[Esri ArcGIS REST Feature Service](https://services7.arcgis.com/n1YM8pTrFmm7L4hs/arcgis/rest/services/usace_river_mile_markers/FeatureServer/0).

The server lets an AI application locate river mile markers for a location — the
nearest marker to a point, all markers in an area, or markers on a named river —
and answer "what river mile am I at?" style questions, all through
natural-language requests routed through the obot MCP gateway.

- **Data source:** [USACE IWR River Mile Markers ArcGIS REST service](https://services7.arcgis.com/n1YM8pTrFmm7L4hs/arcgis/rest/services/usace_river_mile_markers/FeatureServer/0)
- **Source repository:** [GSA-TTS/mcp-server-usace-iwr](https://github.com/GSA-TTS/mcp-server-usace-iwr)
- **Runtime:** `containerized` — hosted by the gateway from the public image
  `ghcr.io/gsa-tts/mcp-server-usace-iwr` (`:8080/mcp`, health at `/health`).
  The container has no public route; it is reachable only through the gateway.
- **Authentication:** None required — queries the public River Mile Markers service.

## Design principles

The server is deliberately built to return **evidence, not data dumps**:

- Only a curated set of marker attributes is returned, keeping the response
  contract stable and minimal.
- The CRS is always explicit — inputs are WGS84 (EPSG:4326) lon/lat; the server
  never silently assumes a coordinate system.
- Results larger than the service's 2000-record cap are paginated.
- Every result carries **provenance** (source agency, dataset, service URL,
  layer, CRS, and UTC retrieval timestamp) for a defensible record.

## Tools

The server registers the following tools. All are read-only.

| Tool | Description |
|------|-------------|
| `usace_rivermile_nearest` | Return the single closest river mile marker to a lat/lon point, with great-circle distance and compass bearing. Answers "what river mile am I at?". |
| `usace_rivermile_find_markers` | Find markers near a point (lat/lon + radius) or within a GeoJSON geometry/bbox. Point queries include a computed distance and are sorted nearest-first. |
| `usace_rivermile_query` | Filter markers by river name (case-insensitive substring) and/or a river-mile value range, ordered by mile ascending, with offset-based pagination. |

## Geometry input

`usace_rivermile_find_markers` accepts either:

- A **`lat` + `lon`** pair (a proximity search, combined with `radius_meters`), or
- A **`geometry`** string containing a GeoJSON geometry object.

Supported GeoJSON geometry types:

- `Point`, `MultiPoint`
- `LineString`, `MultiLineString`
- `Polygon`, `MultiPolygon`
- A `BoundingBox` shorthand:
  `{"type": "BoundingBox", "bbox": [minLon, minLat, maxLon, maxLat]}`

All coordinates must be WGS84 (EPSG:4326) decimal degrees. Supply either
`lat`+`lon` **or** `geometry`, not both.

## Layer fields

The underlying point layer exposes: `name`, `LONGITUDE1`, `LATITUDE1`, `MILE`,
`RIVER_CODE`, `RIVER_NAME`, `RIVER_NUMB`, and `SOURCE`.

## Conventions

- All coordinates are WGS84 decimal degrees. Convert an address or place name to
  coordinates (geocode) before calling the tools.
- The service caps responses at 2000 records; list-style queries paginate and
  report `has_more` / `next_offset`.

## Example prompts

- "What river mile am I at, at latitude 31.45, longitude -92.71?"
- "What river mile markers are within 2 km of this boat ramp?"
- "List the markers on the RED river between mile 100 and 200."
- "Which markers fall inside this bounding box?"

## References

- [USACE IWR River Mile Markers dataset](https://www.arcgis.com/home/item.html?id=604cdc08fe7d43cb90a0584a0b198875)
- [River Mile Markers ArcGIS REST service](https://services7.arcgis.com/n1YM8pTrFmm7L4hs/arcgis/rest/services/usace_river_mile_markers/FeatureServer/0)
- [Source repository](https://github.com/GSA-TTS/mcp-server-usace-iwr)
- [Model Context Protocol](https://modelcontextprotocol.io/)
