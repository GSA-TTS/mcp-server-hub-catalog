# MCP Server Hub Catalog

This repository is the catalog for the GSA-managed Obot MCP gateway. `main`
supports the primary cloud.gov deployment. The `aws` branch preserves the
legacy containerized pilot until cloud.gov reaches feature parity.

> These services are pilots and proofs of concept. They are not authorized for
> production use.

## Active Catalog

Obot loads this repository from `main`. The root `.obotcatalogs` file selects
only `catalog/cloudgov/*.yaml`.

| Product | Runtime | Component | Product definition | Status |
|---|---|---|---|---|
| CDC PLACES | Internal cloud.gov app | [`cdc_places.yaml`](catalog/cloudgov/cdc_places.yaml) | [`cdc_places_vmcp.yaml`](catalog/cloudgov/cdc_places_vmcp.yaml) | Live tested |
| NIH RePORTER | Internal cloud.gov app | [`nih_reporter.yaml`](catalog/cloudgov/nih_reporter.yaml) | [`nih_reporter_vmcp.yaml`](catalog/cloudgov/nih_reporter_vmcp.yaml) | Live verification pending |
| ClinicalTrials.gov | Internal cloud.gov app | [`nih_clinicaltrials.yaml`](catalog/cloudgov/nih_clinicaltrials.yaml) | [`nih_clinicaltrials_vmcp.yaml`](catalog/cloudgov/nih_clinicaltrials_vmcp.yaml) | Live verification pending |
| NCBI E-Utils | Internal cloud.gov app | [`ncbi_eutils.yaml`](catalog/cloudgov/ncbi_eutils.yaml) | [`ncbi_eutils_vmcp.yaml`](catalog/cloudgov/ncbi_eutils_vmcp.yaml) | Live verification pending |
| NEPA BLM | Internal cloud.gov app | [`nepa_blm.yaml`](catalog/cloudgov/nepa_blm.yaml) | [`nepa_blm_vmcp.yaml`](catalog/cloudgov/nepa_blm_vmcp.yaml) | Live tested |
| NEPA CFR | Internal cloud.gov app | [`nepa_cfr.yaml`](catalog/cloudgov/nepa_cfr.yaml) | [`nepa_cfr_vmcp.yaml`](catalog/cloudgov/nepa_cfr_vmcp.yaml) | Live tested |
| NEPA EFH | Internal cloud.gov app | [`nepa_efh.yaml`](catalog/cloudgov/nepa_efh.yaml) | [`nepa_efh_vmcp.yaml`](catalog/cloudgov/nepa_efh_vmcp.yaml) | Live tested |
| NEPA EPA ACRES | Internal cloud.gov app | [`nepa_epa_acres.yaml`](catalog/cloudgov/nepa_epa_acres.yaml) | [`nepa_epa_acres_vmcp.yaml`](catalog/cloudgov/nepa_epa_acres_vmcp.yaml) | Live tested |
| NEPA ESA Ranges | Internal cloud.gov app | [`nepa_esa_ranges.yaml`](catalog/cloudgov/nepa_esa_ranges.yaml) | [`nepa_esa_ranges_vmcp.yaml`](catalog/cloudgov/nepa_esa_ranges_vmcp.yaml) | Live tested |
| NEPA FEMA NFHL | Internal cloud.gov app | [`nepa_fema_nfhl.yaml`](catalog/cloudgov/nepa_fema_nfhl.yaml) | [`nepa_fema_nfhl_vmcp.yaml`](catalog/cloudgov/nepa_fema_nfhl_vmcp.yaml) | Live tested |
| NEPA GBIF | Internal cloud.gov app | [`nepa_gbif.yaml`](catalog/cloudgov/nepa_gbif.yaml) | [`nepa_gbif_vmcp.yaml`](catalog/cloudgov/nepa_gbif_vmcp.yaml) | Live tested |
| NEPA IPaC | Internal cloud.gov app | [`nepa_ipac.yaml`](catalog/cloudgov/nepa_ipac.yaml) | [`nepa_ipac_vmcp.yaml`](catalog/cloudgov/nepa_ipac_vmcp.yaml) | Live tested |
| NEPA NOAA Critical Habitat | Internal cloud.gov app | [`nepa_noaa.yaml`](catalog/cloudgov/nepa_noaa.yaml) | [`nepa_noaa_vmcp.yaml`](catalog/cloudgov/nepa_noaa_vmcp.yaml) | Live tested |
| NEPA NRHP | Internal cloud.gov app | [`nepa_nrhp.yaml`](catalog/cloudgov/nepa_nrhp.yaml) | [`nepa_nrhp_vmcp.yaml`](catalog/cloudgov/nepa_nrhp_vmcp.yaml) | Live tested |

Each service is represented by:

- a `runtime: remote` component entry pointing to an `apps.internal` endpoint;
- a user-facing `type: vmcp` product with profiles and tool permissions; and
- an internal cloud.gov app protected by a C2C network policy.

Users connect to the authenticated vMCP endpoint:

```text
https://<obot-host>/mcp-connect/<vmcp-id>
```

Do not append `/mcp` to the Obot connection URL.

See [`catalog/cloudgov/README.md`](catalog/cloudgov/README.md) for architecture,
visibility, migration gates, and repository-privacy guidance.

## Legacy AWS Catalog

The `aws` branch retains the full containerized catalog and remains supported
for break/fix maintenance. There are no production users on the AWS pilot.

```bash
git switch aws
```

New servers and product work target `main`. AWS-specific fixes target `aws` and
should not be merged back unless they also apply to cloud.gov.

## Repository Structure

```text
.
├── .obotcatalogs                  # selects the active cloud.gov manifests
├── catalog/cloudgov/
│   ├── README.md                  # cloud.gov architecture and migration gate
│   ├── cdc_places.yaml            # internal remote component
│   ├── cdc_places_vmcp.yaml       # user-facing vMCP product
│   ├── nih_reporter*.yaml         # NIH RePORTER component and vMCP
│   ├── nih_clinicaltrials*.yaml   # ClinicalTrials.gov component and vMCP
│   ├── ncbi_eutils*.yaml          # NCBI E-Utils component and vMCP
│   ├── nepa_blm*.yaml             # NEPA BLM component and vMCP
│   ├── nepa_cfr*.yaml             # NEPA CFR component and vMCP
│   ├── nepa_efh*.yaml             # NEPA EFH component and vMCP
│   ├── nepa_epa_acres*.yaml       # NEPA EPA ACRES component and vMCP
│   ├── nepa_esa_ranges*.yaml      # NEPA ESA Ranges component and vMCP
│   ├── nepa_fema_nfhl*.yaml       # NEPA FEMA NFHL component and vMCP
│   ├── nepa_gbif*.yaml            # NEPA GBIF component and vMCP
│   ├── nepa_ipac*.yaml            # NEPA IPaC component and vMCP
│   ├── nepa_noaa*.yaml            # NEPA NOAA component and vMCP
│   └── nepa_nrhp*.yaml            # NEPA NRHP component and vMCP
├── docs/
│   ├── SCHEMA.md                  # generic Obot catalog field reference
│   └── servers/                   # service documentation and migration history
└── icons/                         # shared product icons
```

## Contributing

See [`CONTRIBUTING.md`](CONTRIBUTING.md). A cloud.gov addition is not complete
until its app, C2C policy, component entry, vMCP, gateway tool calls, and a real
external client connection are all verified.
