---
title: "Use existing NEPA components for a NEPA Applications vMCP"
description: "Compose all 15 NEPA services for project screening and regulatory research"
status: proposed
tier: 2
date: "2026-11-12"
last_updated: "2026-11-12"
decision_makers: ["Repository maintainers (human review pending)"]
category: "Agent Authorization"
nist_controls: ["AC-3", "AC-6", "CM-3", "SA-11"]
impact_level: moderate
ato_relevance: yes-internal
risk_treatment: mitigate
related_files:
  - catalog/cloudgov/nepa_applications_vmcp.yaml
  - docs/servers/nepa_applications.md
  - catalog/cloudgov/README.md
---

# Use existing NEPA components for a NEPA Applications vMCP

## Context and Problem Statement

NEPA project screening and regulatory research span 15 existing catalog
services. Users need a single connection for this coherent workflow without
replacing the individual products or deploying another application.

## Decision Drivers

- Reuse stable component IDs and existing private network protections.
- Scope the composition to NEPA rather than grant access to the entire catalog.
- Expose all tools as requested while making the authorization consequences
  explicit (AC-3, AC-6).
- Require change review and live integration evidence (CM-3, SA-11).

## Considered Options

1. **Separate NEPA connections only:** retain the current products but require
   clients to configure and authenticate multiple connections.
2. **Compose existing components:** add one vMCP with explicit NEPA membership
   and all tools from each included component.
3. **Build a new aggregation application:** introduce another runtime and
   network configuration for functionality already available in the gateway.

## Decision Outcome

Chosen option: **Compose existing components**, using `nepa-applications` and
the display name **NEPA Applications**. Reuse the 15 existing NEPA component
references and IDs; do not reference the individual vMCPs as components.

The `everyone` profile uses `selector: "*"` for authenticated Obot users and
`allowedTools: null` for each component, matching the existing NEPA products.
New servers require explicit reviewed membership and permission updates.

### Positive Consequences

- One user-facing connection supports cross-resource research.
- Existing individual products remain available for narrower workflows.
- No new server, dependency, public application route, or C2C policy is needed.

### Negative Consequences

- The larger tool inventory may complicate client tool selection.
- Component availability and upstream errors can affect the combined workflow.
- All-tool permissions also expose future tools from included components;
  tool additions need review for this audience, not just individual products.

### Compliance Consequences

- Authentication is still required; this profile does not allow anonymous use.
- Reviewers must assess the combined authorization scope and future-tool
  behavior. Existing per-service access does not prove least privilege for
  every future NEPA workflow.
- Live tool discovery, calls, external-client access, and authentication
  rejection must be verified before marking the aggregate live tested.
- The Moderate impact-level metadata follows the agent contract's planning
  baseline, not a system FIPS 199 determination. Maintainers must confirm it
  and ATO relevance; this pilot remains unauthorized for production use.
- This AI-assisted record is proposed and requires human acceptance.

## Links

- [Product documentation](../servers/nepa_applications.md)
- [Catalog definition](../../catalog/cloudgov/nepa_applications_vmcp.yaml)
- [Architecture and visibility](../../catalog/cloudgov/README.md)
- [Contribution and verification requirements](../../CONTRIBUTING.md)
