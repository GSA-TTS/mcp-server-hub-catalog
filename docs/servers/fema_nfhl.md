# FEMA NFHL MCP Server

> **Status:** Pilot / proof of concept. Not intended for production use.

## Overview

The FEMA NFHL MCP server exposes the Federal Emergency Management Agency
[National Flood Hazard Layer (NFHL)](https://www.fema.gov/flood-maps/national-flood-hazard-layer)
as a set of MCP tools. The NFHL is the official, authoritative source of FEMA
flood hazard mapping data, published as an
[Esri ArcGIS REST MapServer](https://hazards.fema.gov/arcgis/rest/services/public/NFHL/MapServer).

The server lets an AI application screen a location — a single point, a parcel
boundary, a corridor, or a bounding box — against mapped flood zones, determine
whether it falls in a Special Flood Hazard Area (SFHA), and retrieve the
flood-zone designation, subtype, and base flood elevation, all through
natural-language requests routed through the obot MCP gateway.

- **Data source:** [FEMA NFHL ArcGIS REST service](https://hazards.fema.gov/arcgis/rest/services/public/NFHL/MapServer)
- **Source repository:** [GSA-TTS/mcp-server-fema-nfhl](https://github.com/GSA-TTS/mcp-server-fema-nfhl)
- **Runtime:** `containerized` — hosted by the gateway from the public image
  `ghcr.io/gsa-tts/mcp-server-fema-nfhl` (`:8080/mcp`, health at `/health`).
  The container has no public route; it is reachable only through the gateway.
- **Authentication:** None required — queries the public NFHL service.

## Design principles

The server is deliberately built to return **evidence, not data dumps**:

- Queries request `returnGeometry=false` so responses stay small and
  context-window friendly.
- Only named `outFields` are returned (never `*`), keeping the response contract
  stable and minimal.
- The CRS is always explicit — inputs are WGS84 (EPSG:4326) lon/lat; the server
  never silently assumes a coordinate system.
- Results larger than the service's 2000-record cap are paginated automatically.
- Every result carries **provenance** (source agency, service URL, layer, CRS,
  source citation, and UTC retrieval timestamp) for a defensible record.

## Tools

The server registers the following tools.

| Tool | Description |
|------|-------------|
| `nfhl_screen_flood_zone` | Primary screening tool. Screens a point or arbitrary geometry for FEMA flood-zone constraints, returning a plain-language finding (SFHA status, zone(s), subtype(s)), the flood-zone attributes, and full provenance. |
| `nfhl_count_flood_features` | Size guardrail. Returns only the number of flood features intersecting a point or geometry, so you can gauge result volume before fetching full attributes. |
| `nfhl_list_layers` | Discovery. Lists the layers available in the NFHL service (id, name, geometry type) — floodways, FIRM panels, LOMRs, and more. |

## Geometry input

Both `nfhl_screen_flood_zone` and `nfhl_count_flood_features` accept either:

- A **`lat` + `lon`** pair (convenience shorthand for a single point), or
- A **`geometry`** string containing a GeoJSON geometry object.

Supported GeoJSON geometry types:

- `Point`, `MultiPoint`
- `LineString`, `MultiLineString`
- `Polygon`, `MultiPolygon`
- A `BoundingBox` shorthand:
  `{"type": "BoundingBox", "bbox": [minLon, minLat, maxLon, maxLat]}`

All coordinates must be WGS84 (EPSG:4326) decimal degrees. Supply either
`lat`+`lon` **or** `geometry`, not both.

## Conventions

- All coordinates are WGS84 decimal degrees. Convert an address to coordinates
  (geocode) before calling the tools.
- A base flood elevation (BFE) or depth value of `-9999` means "not applicable
  or not mapped" for that flood zone.

## Example prompts

- "Is latitude 29.9511, longitude -90.0715 in a FEMA flood zone?"
- "Does this parcel polygon intersect a Special Flood Hazard Area?"
- "How many flood features overlap this bounding box before I fetch details?"
- "What layers are available in the FEMA NFHL service?"
- "Screen this pipeline corridor for flood hazards and tell me if we'd need
  flood insurance."

## References

- [FEMA National Flood Hazard Layer](https://www.fema.gov/flood-maps/national-flood-hazard-layer)
- [NFHL ArcGIS REST service](https://hazards.fema.gov/arcgis/rest/services/public/NFHL/MapServer)
- [Source repository](https://github.com/GSA-TTS/mcp-server-fema-nfhl)
- [Model Context Protocol](https://modelcontextprotocol.io/)
