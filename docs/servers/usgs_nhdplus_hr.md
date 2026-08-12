# USGS NHDPlus HR MCP Server

> **Status:** Pilot / proof of concept. Not intended for production use.

## Overview

The USGS NHDPlus HR MCP server exposes the U.S. Geological Survey
[NHDPlus High Resolution (NHDPlus HR)](https://www.usgs.gov/national-hydrography/nhdplus-high-resolution)
dataset as a set of MCP tools. NHDPlus HR is a nationally seamless, routed
surface-water network built from the high-resolution National Hydrography
Dataset (NHD), the Watershed Boundary Dataset (WBD), and 3DEP elevation, and is
published as an
[Esri ArcGIS REST MapServer](https://hydro.nationalmap.gov/arcgis/rest/services/NHDPlus_HR/MapServer).

The server lets an AI application query hydrography for a location — a single
point, a parcel boundary, a corridor, or a bounding box — and retrieve the
streams, rivers, lakes, gages, water features, and watershed boundaries that
intersect it, all through natural-language requests routed through the obot MCP
gateway.

- **Data source:** [USGS NHDPlus HR ArcGIS REST service](https://hydro.nationalmap.gov/arcgis/rest/services/NHDPlus_HR/MapServer)
- **Source repository:** [GSA-TTS/mcp-server-usgs-nationalmap](https://github.com/GSA-TTS/mcp-server-usgs-nationalmap)
- **Runtime:** `containerized` — hosted by the gateway from the public image
  `ghcr.io/gsa-tts/mcp-server-usgs-nationalmap` (`:8080/mcp`, health at `/health`).
  The container has no public route; it is reachable only through the gateway.
- **Authentication:** None required — queries the public NHDPlus HR service.

## Design principles

The server is deliberately built to return **evidence, not data dumps**:

- Queries request `returnGeometry=false` so responses stay small and
  context-window friendly.
- Only named `outFields` are returned by default (a curated core set), keeping
  the response contract stable and minimal; a `verbose` flag is available for the
  full flowline attribute set.
- The CRS is always explicit — inputs are WGS84 (EPSG:4326) lon/lat; the server
  never silently assumes a coordinate system.
- Results larger than the service's 2000-record cap are paginated automatically.
- Integer FType/FCode feature codes are translated to human-readable labels.
- Every result carries **provenance** (source agency, dataset, service URL,
  layer, CRS, and UTC retrieval timestamp) for a defensible record.

## Tools

The server registers the following tools.

| Tool | Description |
|------|-------------|
| `hydro_find_waterways` | Find NHD flowlines (streams, rivers, canals, artificial paths) intersecting a point or geometry, with Strahler stream order, total drainage area, slope, elevation, and modeled mean-annual flow (EROM) and velocity. Optional flags add non-network flowlines or the full attribute set. |
| `hydro_find_waterbodies` | Find NHD waterbodies (lakes, ponds, reservoirs, swamps) and areal water features (wide rivers, bays, rapids, dams) intersecting a point or geometry. |
| `hydro_find_gages` | Find NHDPlus stream gages intersecting a geometry, with NWIS linkage and monitored drainage area (in square miles). |
| `hydro_find_water_features` | Find NHD point and line water features (springs, waterfalls, dams/weirs, gates, levees, wells) intersecting a geometry. |
| `hydro_identify_watershed` | Identify the HUC12 subwatershed(s) containing or intersecting a location, with name, 12-digit HUC code, downstream HUC (`tohuc`), type, area, and states. |
| `hydro_count_features` | Size guardrail. Returns only the number of features of a chosen layer intersecting a point or geometry, so you can gauge result volume before fetching full attributes. |
| `hydro_list_layers` | Discovery. Lists the layers available in the NHDPlus HR service (id, name, geometry type) — catchments, sinks, boundary units, and more. |

## Geometry input

The geometry tools accept either:

- A **`lat` + `lon`** pair (convenience shorthand for a single point), or
- A **`geometry`** string containing a GeoJSON geometry object.

Supported GeoJSON geometry types:

- `Point`, `MultiPoint`
- `LineString`, `MultiLineString`
- `Polygon`, `MultiPolygon`
- A `BoundingBox` shorthand:
  `{"type": "BoundingBox", "bbox": [minLon, minLat, maxLon, maxLat]}`

All coordinates must be WGS84 (EPSG:4326) decimal degrees. Supply either
`lat`+`lon` **or** `geometry`, not both. For the point/line layers (gages, water
features), pass a Polygon or BoundingBox to capture nearby features — a bare
point rarely coincides exactly with one.

## Conventions

- All coordinates are WGS84 decimal degrees. Convert an address or place name to
  coordinates (geocode) before calling the tools.
- Integer `ftype`/`fcode` feature codes come back with `ftype_label` /
  `fcode_label` giving readable names (e.g. `46006` → "Stream/River: Perennial").
- Drainage-area units differ: stream gages report drainage area in **square
  miles** (`dasqmi`); flowlines and watersheds use **square kilometers**
  (`AreaSqKm` / `TotalDrainageAreaSqKm`).
- Each service layer caps responses at 2000 records; the server paginates
  automatically and sets `truncated: true` when a cap is reached.

## Example prompts

- "What river runs through latitude 30.45, longitude -91.19?"
- "Which HUC12 watershed contains this point, and where does it drain?"
- "What is the highest stream order among the flowlines crossing this bounding box?"
- "Are there any stream gages within this polygon, and what drainage area do they monitor?"
- "Name the lake at this coordinate."
- "Are there waterfalls or dams along this river reach?"

## Possible future add-ons

NHDPlus HR is a fully routed network, which enables higher-value tools not yet
implemented, e.g. upstream/downstream network tracing (via `hydroseq` /
`levelpathi`), watershed routing traversal (via `tohuc`), catchment lookup
(NHDPlusCatchment), reach-code / NHDPlusID lookups, and NWIS gage cross-walk to
live streamflow. See the source repository README for details.

## References

- [USGS NHDPlus High Resolution](https://www.usgs.gov/national-hydrography/nhdplus-high-resolution)
- [NHDPlus HR ArcGIS REST service](https://hydro.nationalmap.gov/arcgis/rest/services/NHDPlus_HR/MapServer)
- [Source repository](https://github.com/GSA-TTS/mcp-server-usgs-nationalmap)
- [Model Context Protocol](https://modelcontextprotocol.io/)
