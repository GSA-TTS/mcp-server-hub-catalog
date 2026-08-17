# MCP Server Hub Catalog

This repository is the catalog of [Model Context Protocol
(MCP)](https://modelcontextprotocol.io) servers available through the
GSA-managed **obot MCP gateway**. Each entry describes a hosted MCP server that
the gateway can connect to, so that AI applications reaching the gateway can
discover and use these tools.

## What is this catalog?

The obot MCP gateway reads the YAML entries in this repository to populate its
catalog UI and to learn how to connect to each MCP server. Every server is
described by a single YAML file at the repository root, following the
[obot-platform/mcp-catalog](https://github.com/obot-platform/mcp-catalog) entry
format.

The servers cataloged here are pilot/proof-of-concept MCP servers that expose
federal data APIs (NIH, CDC, NCBI, EIA) as MCP tools. Most wrap public, keyless
APIs and are hosted by the gateway as shared (`multiUser`) containers; the EIA
and Regulations.gov servers require a personal API key and are deployed per-user
(`singleUser`).

## Available servers

| Server | Description | Data source | Entry | Docs |
|--------|-------------|-------------|-------|------|
| **NIH RePORTER** | Search and analyze NIH grant funding data | [NIH RePORTER API](https://api.reporter.nih.gov/) | [`nih_reporter.yaml`](nih_reporter.yaml) | [docs](docs/servers/nih_reporter.md) |
| **NIH ClinicalTrials** | Search clinical trial records | [ClinicalTrials.gov API](https://clinicaltrials.gov/data-api/api) | [`nih_clinicaltrials.yaml`](nih_clinicaltrials.yaml) | [docs](docs/servers/nih_clinicaltrials.md) |
| **CDC PLACES** | Local-level health and chronic disease measures | [CDC PLACES API](https://data.cdc.gov/browse?category=500+Cities+%26+Places) | [`cdc_places.yaml`](cdc_places.yaml) | [docs](docs/servers/cdc_places.md) |
| **NCBI E-Utils** | Search NCBI biomedical databases (PubMed, etc.) | [NCBI E-Utilities](https://www.ncbi.nlm.nih.gov/books/NBK25501/) | [`ncbi_eutils.yaml`](ncbi_eutils.yaml) | [docs](docs/servers/ncbi_eutils.md) |
| **NCI EVS** | Search and navigate NCI cancer terminology (NCIt / NCIm) | [NCI EVS API](https://api-evsrest.nci.nih.gov/) | [`nci_evs.yaml`](nci_evs.yaml) | [docs](docs/servers/nci_evs.md) |
| **EIA Open Data** | Query U.S. energy statistics across all 17 EIA datasets (per-user API key) | [EIA Open Data API v2](https://www.eia.gov/opendata/) | [`eia.yaml`](eia.yaml) | [docs](docs/servers/eia.md) |
| **FEMA NFHL** | Screen locations and geometries against FEMA National Flood Hazard Layer flood zones | [FEMA NFHL service](https://hazards.fema.gov/arcgis/rest/services/public/NFHL/MapServer) | [`fema_nfhl.yaml`](fema_nfhl.yaml) | [docs](docs/servers/fema_nfhl.md) |
| **Grants.gov** | Search and retrieve federal grant opportunities across all agencies | [Grants.gov API](https://www.grants.gov/api/) | [`grants_gov.yaml`](grants_gov.yaml) | [docs](docs/servers/grants_gov.md) |
| **Regulations.gov** | Search and retrieve federal regulatory documents, public comments, and dockets (per-user API key) | [Regulations.gov API](https://open.gsa.gov/api/regulationsgov/) | [`regulations_gov.yaml`](regulations_gov.yaml) | [docs](docs/servers/regulations_gov.md) |
| **USGS NHDPlus HR** | Query USGS NHDPlus High Resolution hydrography — streams, lakes, gages, and watersheds — by point or geometry | [USGS NHDPlus HR service](https://hydro.nationalmap.gov/arcgis/rest/services/NHDPlus_HR/MapServer) | [`usgs_nhdplus_hr.yaml`](usgs_nhdplus_hr.yaml) | [docs](docs/servers/usgs_nhdplus_hr.md) |
| **BLM MLRS Geothermal Leases** | Search and retrieve BLM geothermal lease records by case number or by state, status, and date range | [BLM MLRS Geothermal Leases service](https://gis.blm.gov/nlsdb/rest/services/HUB/BLM_Natl_MLRS_Geothermal_Leases/FeatureServer/0) | [`blm_mlrs.yaml`](blm_mlrs.yaml) | [docs](docs/servers/blm_mlrs.md) |

> **Note:** These servers are pilots / proofs of concept and are not intended
> for production use.

## Repository structure

```
.
├── README.md                    # This file
├── CONTRIBUTING.md              # How to add or update a server
├── docs/
│   ├── SCHEMA.md                # Catalog entry field reference
│   └── servers/                 # Detailed per-server documentation
│       ├── nih_reporter.md
│       ├── nih_clinicaltrials.md
│       ├── cdc_places.md
│       ├── ncbi_eutils.md
│       ├── nci_evs.md
│       ├── eia.md
│       ├── grants_gov.md
│       ├── regulations_gov.md
│       ├── fema_nfhl.md
│       ├── usgs_nhdplus_hr.md
│       └── blm_mlrs.md
├── nih_reporter.yaml            # Catalog entries (one per server)
├── nih_clinicaltrials.yaml
├── cdc_places.yaml
├── ncbi_eutils.yaml
├── nci_evs.yaml
├── eia.yaml
├── grants_gov.yaml
├── regulations_gov.yaml
├── fema_nfhl.yaml
├── usgs_nhdplus_hr.yaml
└── blm_mlrs.yaml
```

## Adding a server

See [`CONTRIBUTING.md`](CONTRIBUTING.md) for the full workflow and
[`docs/SCHEMA.md`](docs/SCHEMA.md) for the catalog entry schema.

## Contact

For questions about the catalog or the gateway, contact the GSA-TTS team
maintaining this repository.
