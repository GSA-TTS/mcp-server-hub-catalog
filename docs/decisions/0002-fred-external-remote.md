---
title: "Use the official external FRED connector for a FRED vMCP"
description: "List an externally operated economic-data service without claiming it is inside the hub boundary"
status: proposed
tier: 2
date: "2026-11-13"
last_updated: "2026-11-13"
decision_makers: ["Repository maintainers (human review pending)"]
category: "Deployment and Infrastructure"
nist_controls: ["AC-3", "AC-6", "CM-3", "IA-5", "SA-9", "SA-11", "SC-7", "SC-8"]
impact_level: moderate
ato_relevance: yes-boundary
risk_treatment: mitigate
related_files:
  - catalog/cloudgov/fred.yaml
  - catalog/cloudgov/fred_vmcp.yaml
  - docs/servers/fred.md
  - catalog/cloudgov/README.md
---

# Use the official external FRED connector for a FRED vMCP

## Context and Problem Statement

The Federal Reserve Bank of St. Louis operates the official FRED MCP Connector
at `https://mcp.stlouisfed.org`. Users want this deployed economic-data service
listed in the hub, while acknowledging it remains outside the GSA hub boundary.
Unlike current internal components, it requires per-user provider authorization.

## Decision Drivers

- Use the official provider, not an unrelated community FRED implementation.
- Reuse the existing component/vMCP catalog pattern without deploying a server.
- Make external data flows and provider-controlled operation explicit.
- Avoid shared upstream credentials and restrict access to five advertised tools.
- Require live OAuth and isolation evidence before claiming integration success.

## Considered Options

1. **Documentation-only link:** direct users to the provider, without a hub product.
2. **External remote component and vMCP:** list the provider endpoint and expose
   an explicitly scoped product through Obot.
3. **Host another FRED implementation:** deploy a separate server, introducing
   maintenance and potentially API-key requirements rather than using the
   requested official connector.

## Decision Outcome

Proposed option: **External remote component and vMCP**, with component key
`obot-fred`, product key `fred`, and component ID `fred`. The implementation
name is **FRED External Component**; the user-facing product is **FRED**.

Use the provider's exact HTTPS endpoint without adding `/mcp`. Set
`serverUserType: singleUser` for per-user upstream authorization; omit API-key
configuration, manual headers, and credentials. Obot must handle the provider's
authorization flow; this record does not assert that compatibility is verified.

The `everyone` profile permits authenticated Obot users and explicitly lists
the five advertised tools, not `allowedTools: null`. New tools require review.
Do not add FRED to unrelated aggregate products. No deployment, C2C, egress,
or authentication implementation is changed by these catalog files.

### Positive Consequences

- Official economic data is discoverable through a dedicated hub product.
- No new application, dependency, FRED API key, or shared credential is needed.
- Both listing layers disclose the external boundary and sensitive-input limits.

### Negative Consequences

- Availability, tools, provider terms, and authentication can change upstream.
- Requests leave the hub boundary even when clients connect through Obot.
- Gateway OAuth or per-user isolation may not work; static YAML cannot prove it.

### Compliance Consequences

- Review upstream data handling, terms/privacy, permitted egress, and external
  service usage (SA-9, SC-7, SC-8). Listing is not an authorization decision.
- Verify separate Obot access control and per-user FRED authorization, including
  credential isolation and revocation (AC-3, AC-6, IA-5).
- Internal-app routing, C2C, and `/health` requirements do not apply to this
  external upstream; live MCP, OAuth, tool calls, and client evidence still do.
- Blocked acceptance work is tracked in the service document until authorized
  gateway access and a test account permit actual execution (SA-11).
- Moderate metadata is the agent contract's planning baseline, not a system
  FIPS 199 determination. Maintainers must confirm impact and ATO relevance.
  The hub integration remains a pilot, not authorized for production use.
- This AI-assisted record is proposed and requires human acceptance.

## Links

- [FRED service and acceptance record](../servers/fred.md)
- [Component](../../catalog/cloudgov/fred.yaml)
- [Product](../../catalog/cloudgov/fred_vmcp.yaml)
- [Architecture and external-service exception](../../catalog/cloudgov/README.md)
- [Contribution requirements](../../CONTRIBUTING.md)
