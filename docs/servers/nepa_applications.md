---
title: "NEPA Applications vMCP"
description: "Combined NEPA project-screening and regulatory-research product"
status: draft
tier: 2
last_updated: "2026-11-12"
related_files:
  - catalog/cloudgov/nepa_applications_vmcp.yaml
  - catalog/cloudgov/README.md
  - docs/decisions/0001-nepa-applications-vmcp.md
---

# NEPA Applications vMCP

> **Status:** Pilot / proof of concept. Not authorized for production use.
> Aggregate live verification is pending; existing individual-service results
> do not establish that this combined product works.

## Purpose

NEPA project research often spans biological resources, land use, cultural
resources, water conditions, and regulations. NEPA Applications provides one
authenticated MCP connection to all tools from the 15 existing NEPA components
instead of requiring a separate client connection for each service.

This is a composition of existing internal applications, not a new server or
an automated assessment tool. Clients choose which tools to call. The existing
individual NEPA vMCPs remain available and unchanged.

## Included components

| Service | Component ID | Component entry | Documentation |
|---|---|---|---|
| BLM | `nepa-blm` | `obot-nepa-blm` | [BLM](blm.md) |
| CFR | `nepa-cfr` | `obot-nepa-cfr` | [CFR](cfr.md) |
| EFH | `nepa-efh` | `obot-nepa-efh` | [EFH](efh.md) |
| EPA ACRES | `nepa-epa-acres` | `obot-nepa-epa-acres` | [EPA ACRES](epa_acres.md) |
| ESA Ranges | `nepa-esa-ranges` | `obot-nepa-esa-ranges` | [ESA Ranges](esa_ranges.md) |
| FEMA NFHL | `nepa-fema-nfhl` | `obot-nepa-fema-nfhl` | [FEMA NFHL](nepa_fema_nfhl.md) |
| GBIF | `nepa-gbif` | `obot-nepa-gbif` | [GBIF](gbif.md) |
| IPaC | `nepa-ipac` | `obot-nepa-ipac` | [IPaC](ipac.md) |
| NOAA Critical Habitat | `nepa-noaa` | `obot-nepa-noaa` | [NOAA](noaa.md) |
| NRHP | `nepa-nrhp` | `obot-nepa-nrhp` | [NRHP](nrhp.md) |
| USGS PAD-US | `nepa-padus` | `obot-nepa-usgs-padus` | [PAD-US](padus.md) |
| NOAA PCSRF | `nepa-pcsrf` | `obot-nepa-noaa-pcsrf` | [PCSRF](pcsrf.md) |
| Counties (TIGERweb) | `nepa-tigerweb-counties` | `obot-nepa-tigerweb-counties` | [Counties](tigerweb_counties.md) |
| Tribal Lands | `nepa-tribal` | `obot-nepa-tribal` | [Tribal Lands](tribal.md) |
| USACE | `nepa-usace` | `obot-nepa-usace` | [USACE](usace.md) |

Membership is explicit in the [manifest](../../catalog/cloudgov/nepa_applications_vmcp.yaml).
Adding a NEPA service requires a reviewed update to both `components` and
`allowedComponents`; the product does not discover new servers automatically.

## Access and tools

- The `everyone` profile grants access to all **authenticated Obot users**;
  `selector: "*"` does not grant anonymous access.
- Each component uses `allowedTools: null`, exposing all its tools, including
  future tools added to that component. Review upstream tool changes for
  suitability within this combined access scope.
- Use live `tools/list` as the inventory, not the catalog's `toolPreview`.
  Use the exact tool names returned by the gateway; composition may qualify
  names differently from direct component connections.
- Existing internal-only routes and port-scoped C2C policies remain in place.
  No new application, route, or network policy is required by this manifest.

## Connect

Launch **NEPA Applications** in Obot and use the gateway-issued connection URL:

```text
https://<obot-host>/mcp-connect/<vmcp-id>
```

Authenticate with Obot OAuth or a scoped API key authorized for this vMCP.
Do not append `/mcp`, and do not assume the runtime vMCP ID equals the catalog
key `nepa-applications`.

## Example workflows and limitations

- Screen a public test location for listed species, habitat, flood hazards,
  protected lands, tribal lands, and historic properties; retain source
  references and distinguish missing data from negative findings.
- Identify county and USACE jurisdiction context, then research relevant CFR
  text and Federal Register rulemaking.
- Compare biological-resource evidence from IPaC, ESA Ranges, GBIF, NOAA, and
  EFH where their geographic coverage and input formats are applicable.

Tool results support early research. They do not replace an official species
list, agency determination, consultation, or completed NEPA compliance.
Do not submit sensitive project coordinates, PII, CUI, or nonpublic project
data to this pilot without appropriate authorization. A component outage or
upstream error must be reported as unavailable evidence, not a clean screening.

## Live acceptance gate

With authorized gateway access, record actual outputs for:

1. Catalog synchronization and successful product launch.
2. Internal health reachability and unchanged private routing/C2C protections
   for all 15 applications.
3. Aggregate `tools/list` compared with live inventories of every component,
   including pagination, name qualification, omissions, and collisions.
4. At least one successful real, read-only `tools/call` per component using
   applicable public test inputs.
5. A multi-component screening workflow from a real external MCP client.
6. Rejection of an unauthenticated connection.

Until these pass, report aggregate live verification as **BLOCKED / pending**.
Track this gate with the feature PR; do not mark the product live tested based
only on local YAML checks or individual-service verification.

## Rollback and review

Withdraw the NEPA Applications catalog definition, synchronize the catalog,
and confirm the aggregate is no longer available. Check whether already
launched instances require explicit removal or access revocation in Obot.
Leave the internal components and individual vMCPs intact.

This product and its documentation were prepared with AI assistance and
require human review before merge. See the
[decision record](../decisions/0001-nepa-applications-vmcp.md) for the access
and composition trade-offs.
