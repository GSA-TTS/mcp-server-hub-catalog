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
│   └── nih_clinicaltrials*.yaml   # ClinicalTrials.gov component and vMCP
├── docs/
│   ├── SCHEMA.md                  # generic Obot catalog field reference
│   └── servers/                   # service documentation and migration history
└── icons/                         # shared product icons
```

## Contributing

See [`CONTRIBUTING.md`](CONTRIBUTING.md). A cloud.gov addition is not complete
until its app, C2C policy, component entry, vMCP, gateway tool calls, and a real
external client connection are all verified.
