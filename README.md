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
| **BLM** | Screen a location against BLM land use plans, wilderness areas, and National Monuments/NCAs for NEPA analysis | [BLM National ArcGIS REST services](https://services1.arcgis.com/KbxwQRRfWyEYLgp4/arcgis/rest/services) | [`blm.yaml`](blm.yaml) | [docs](docs/servers/blm.md) |
| **USACE IWR River Mile Markers** | Locate river mile markers on navigable U.S. rivers — nearest marker, search by area, or filter by river and mile range | [USACE IWR River Mile Markers service](https://services7.arcgis.com/n1YM8pTrFmm7L4hs/arcgis/rest/services/usace_river_mile_markers/FeatureServer/0) | [`usace_iwr.yaml`](usace_iwr.yaml) | [docs](docs/servers/usace_iwr.md) |
| **CFR** | Resolve, browse, and diff Code of Federal Regulations text and trace the Federal Register rulemaking behind it | [eCFR](https://www.ecfr.gov/developers/documentation/api/v1) & [Federal Register](https://www.federalregister.gov/developers/documentation/api/v1) APIs | [`cfr.yaml`](cfr.yaml) | [docs](docs/servers/cfr.md) |
| **Census** | Establish socioeconomic baseline conditions for NEPA analysis from U.S. Census Bureau ACS data by region of interest (per-user API key) | [Census ACS 5-Year Estimates](https://www.census.gov/programs-surveys/acs) | [`census.yaml`](census.yaml) | [docs](docs/servers/census.md) |
| **NEPA EFH** | Screen a location against NOAA Essential Fish Habitat (EFH), HAPC, and salmon/HMS/CPS/groundfish designations for NEPA analysis | [NOAA Fisheries West Coast EFH services](https://www.fisheries.noaa.gov/national/habitat-conservation/essential-fish-habitat) | [`efh.yaml`](efh.yaml) | [docs](docs/servers/efh.md) |
| **NEPA EPA AQS** | Assess air quality baseline conditions for NEPA analysis from EPA AQS criteria-pollutant monitoring data and NAAQS screening (per-user API key) | [EPA Air Quality System API](https://aqs.epa.gov/aqsweb/documents/data_api.html) | [`epa_aqs.yaml`](epa_aqs.yaml) | [docs](docs/servers/epa_aqs.md) |
| **NEPA ESA Ranges** | Screen a location against NOAA ESA-listed species ranges (HUC-12 watershed detail) for Section 7 consultation in NEPA analysis | [NOAA Fisheries Ranges_dice service](https://www.fisheries.noaa.gov/topic/endangered-species-conservation) | [`esa_ranges.yaml`](esa_ranges.yaml) | [docs](docs/servers/esa_ranges.md) |
| **NEPA FEMA NFHL** | Screen a location against FEMA National Flood Hazard Layer (NFHL) flood zones, levees, and water areas for NEPA analysis | [FEMA NFHL ArcGIS service](https://hazards.fema.gov/arcgis/rest/services/public/NFHL/MapServer) | [`nepa_fema_nfhl.yaml`](nepa_fema_nfhl.yaml) | [docs](docs/servers/nepa_fema_nfhl.md) |
| **NEPA GBIF** | Retrieve georeferenced GBIF species occurrences and county-level species presence for NEPA biodiversity screening | [GBIF API](https://www.gbif.org/developer/summary) | [`gbif.yaml`](gbif.yaml) | [docs](docs/servers/gbif.md) |
| **NEPA IPaC** | Screen a location against USFWS IPaC ESA species, migratory birds, wetlands, critical habitat, and refuges for NEPA analysis | [USFWS IPaC](https://ipac.ecosphere.fws.gov/) | [`ipac.yaml`](ipac.yaml) | [docs](docs/servers/ipac.md) |
| **NEPA NOAA Critical Habitat** | Screen a location against NOAA West Coast Region ESA-designated critical habitat for Section 7 consultation in NEPA analysis | [NOAA Fisheries West Coast critical-habitat service](https://www.fisheries.noaa.gov/national/endangered-species-conservation/critical-habitat) | [`noaa.yaml`](noaa.yaml) | [docs](docs/servers/noaa.md) |
| **NEPA NRHP** | Screen a location against National Register of Historic Places (NRHP) listed properties for Section 106 review in NEPA analysis | [NPS Cultural Resources service](https://www.nps.gov/subjects/nationalregister/index.htm) | [`nrhp.yaml`](nrhp.yaml) | [docs](docs/servers/nrhp.md) |
| **NEPA USGS PAD-US** | Screen a location against the USGS PAD-US protected-areas database (ownership and management) for NEPA analysis | [USGS PAD-US](https://www.usgs.gov/programs/gap-analysis-project/science/pad-us-data-overview) | [`padus.yaml`](padus.yaml) | [docs](docs/servers/padus.md) |
| **NEPA NOAA PCSRF** | Screen a location against NOAA species ranges, critical habitat, EFH, and Pacific Coastal Salmon Recovery Fund projects for NEPA analysis | [NOAA Fisheries ArcGIS services](https://www.fisheries.noaa.gov/grant/pacific-coastal-salmon-recovery-fund) | [`pcsrf.yaml`](pcsrf.yaml) | [docs](docs/servers/pcsrf.md) |
| **NEPA USACE** | Identify the USACE regulatory district and wetland delineation regions/subregions for a location for Section 404 NEPA analysis | [USACE regulatory ArcGIS services](https://www.usace.army.mil/Missions/Civil-Works/Regulatory-Program-and-Permits/) | [`usace.yaml`](usace.yaml) | [docs](docs/servers/usace.md) |
| **NEPA Tribal Lands** | Identify tribal lands (Census TIGERweb AIANNHA) intersecting a location for geographic context in NEPA analysis | [Census TIGERweb AIANNHA](https://tigerweb.geo.census.gov/tigerwebmain/TIGERweb_main.html) | [`tribal.yaml`](tribal.yaml) | [docs](docs/servers/tribal.md) |
| **NEPA Counties (TIGERweb)** | Identify the counties intersecting a location (Census TIGERweb) for jurisdictional coordination in NEPA analysis | [Census TIGERweb](https://tigerweb.geo.census.gov/tigerwebmain/TIGERweb_main.html) | [`tigerweb_counties.yaml`](tigerweb_counties.yaml) | [docs](docs/servers/tigerweb_counties.md) |

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
│       ├── blm_mlrs.md
│       ├── blm.md
│       ├── usace_iwr.md
│       ├── cfr.md
│       ├── census.md
│       ├── efh.md
│       ├── epa_aqs.md
│       ├── esa_ranges.md
│       ├── nepa_fema_nfhl.md
│       ├── gbif.md
│       ├── ipac.md
│       ├── noaa.md
│       ├── nrhp.md
│       ├── padus.md
│       ├── pcsrf.md
│       ├── usace.md
│       ├── tribal.md
│       └── tigerweb_counties.md
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
├── blm_mlrs.yaml
├── blm.yaml
├── usace_iwr.yaml
├── cfr.yaml
├── census.yaml
├── efh.yaml
├── epa_aqs.yaml
├── esa_ranges.yaml
├── nepa_fema_nfhl.yaml
├── gbif.yaml
├── ipac.yaml
├── noaa.yaml
├── nrhp.yaml
├── padus.yaml
├── pcsrf.yaml
├── usace.yaml
├── tribal.yaml
└── tigerweb_counties.yaml
```

## Adding a server

See [`CONTRIBUTING.md`](CONTRIBUTING.md) for the full workflow and
[`docs/SCHEMA.md`](docs/SCHEMA.md) for the catalog entry schema.

## Contact

For questions about the catalog or the gateway, contact the GSA-TTS team
maintaining this repository.
