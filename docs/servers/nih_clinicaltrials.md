# NIH ClinicalTrials MCP Server

> **Status:** Pilot / proof of concept. Not intended for production use.

## Overview

The NIH ClinicalTrials MCP server exposes the
[ClinicalTrials.gov v2 API](https://clinicaltrials.gov/data-api/api) as MCP
tools. ClinicalTrials.gov is the NIH/NLM registry of clinical studies conducted
around the world — a database of 570,000+ studies covering conditions,
interventions, sponsors, eligibility, locations, and results.

The server lets an AI application search, retrieve, and analyze clinical study
data through natural-language requests routed through the obot MCP gateway.

- **Data source:** [ClinicalTrials.gov v2 API](https://clinicaltrials.gov/data-api/api) (refreshed daily)
- **Source repository:** [GSA-TTS/mcp-server-nih-clinicaltrials](https://github.com/GSA-TTS/mcp-server-nih-clinicaltrials)
- **Gateway endpoint:** hosted by the gateway from the public image
  `ghcr.io/gsa-tts/mcp-server-nih-clinicaltrials` (`:8080/mcp`, health at
  `/health`). Runtime is `containerized`; the container has no public route and
  is reachable only through the gateway.
- **Authentication:** None required — the ClinicalTrials.gov API is public.

## Tools

### `clinicaltrials_get_study`

Retrieve a single study record by NCT ID (all 394 fields available).

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `nct_id` | string | Yes | NCT identifier, e.g. `NCT00000102`. |
| `fields` | `StudyField[]` | No | Specific fields to return; omit for all fields. |
| `format` | `json` \| `csv` | No | Response format (default `json`). |
| `markup_format` | `markdown` \| `legacy` | No | Text markup format (default `markdown`). |

### `clinicaltrials_search_studies`

Search studies by condition, intervention, sponsor, location, and more. Returns
paginated results.

**Query parameters** (at least one required): `query_cond` (condition/disease),
`query_term` (general keyword), `query_intr` (intervention/treatment),
`query_titles` (title only), `query_id` (NCT ID or identifier), `query_spons`
(sponsor/collaborator), `query_locn` (location text or `AREA[...]` syntax),
`query_patient` (plain-language patient search).

**Filters:** `filter_overall_status`, `filter_geo` (e.g.
`distance(39.0,-77.0,50mi)`), `filter_ids`, `post_filter_overall_status`,
`post_filter_geo`, `agg_filter_phase`, `agg_filter_study_type`, `agg_filters`.

**Pagination & output:** `sort` (e.g. `LastUpdatePostDate:desc`), `page_size`
(1–1000, default 20), `page_token`, `count_total`, `fields`, `format`,
`markup_format`.

By default returns **19 essential fields** for compact screening; use
`clinicaltrials_get_study` for full details on a specific study.

### `clinicaltrials_search_datatable`

Same search interface as `clinicaltrials_search_studies`, but renders all
matching results as an interactive, sortable, paginated table (fetches all pages
automatically). Each row shows NCT ID, title, status, phase, conditions,
interventions, sponsor, start date, and enrollment count. Accepts the same
query/filter/sort parameters (excluding pagination and output-format options).

### `clinicaltrials_get_field_values`

Get the distribution of values across all studies for one or more fields (e.g.
study counts per phase, per country, per status).

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `fields` | `StudyField[]` | Yes | Fields to get distributions for. |

Works best with enumerable fields: `Phase`, `OverallStatus`, `StudyType`, `Sex`,
`StdAge`, `LeadSponsorClass`, `InterventionType`, `LocationCountry`,
`DesignAllocation`, `IsFDARegulatedDrug`, `HasResults`, `IPDSharing`.

### `clinicaltrials_analyze_study_locations`

Analyze the geographic distribution of locations across a set of studies. Pages
through all matching results and classifies each study relative to a target
country:

- `only_in_target` — all locations are in the target country
- `mixed` — locations in the target country and at least one other
- `not_in_target` — no locations in the target country
- `no_location_data` — no location country data present

Also returns a frequency table of every country seen, sorted by count. Accepts
the same query/filter parameters as `clinicaltrials_search_studies`, plus:

| Parameter | Default | Description |
|-----------|---------|-------------|
| `target_country` | `United States` | Reference country for classification (case-insensitive). |

## Field selection

- **Default search fields (19):** NCTId, BriefTitle, OfficialTitle, Acronym,
  OverallStatus, StartDate, PrimaryCompletionDate, CompletionDate,
  LastUpdatePostDate, BriefSummary, Condition, Phase, StudyType,
  EnrollmentCount, InterventionName, LeadSponsorName, LeadSponsorClass,
  LocationCountry, LocationFacility.
- **Full details:** use `clinicaltrials_get_study` for all 394 fields on a
  specific study.
- **Custom selection:** all study-returning tools accept a `fields` parameter
  drawn from the `StudyField` enum (394 fields grouped by Identification,
  Status, Sponsor, Design, Arms/Interventions, Outcomes, Eligibility, Locations,
  Results, and MeSH/Browse sections).

## Example prompts

- "Find recruiting Phase 2 and Phase 3 interventional studies for breast
  cancer."
- "Find placebo-controlled drug trials for type 2 diabetes that are currently
  recruiting."
- "Show me double-blind parallel-assignment prevention trials for cardiovascular
  disease."
- "How many recruiting diabetes trials are US-only?"
- "Analyze the country distribution of phase 3 oncology interventional trials."

## References

- [ClinicalTrials.gov](https://clinicaltrials.gov/)
- [ClinicalTrials.gov v2 API](https://clinicaltrials.gov/data-api/api)
- [Source repository](https://github.com/GSA-TTS/mcp-server-nih-clinicaltrials)
- [Model Context Protocol](https://modelcontextprotocol.io/)
