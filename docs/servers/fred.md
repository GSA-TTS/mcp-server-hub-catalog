---
title: "FRED MCP Connector"
description: "Official externally operated FRED connector listing and hub acceptance gate"
status: draft
tier: 2
last_updated: "2026-11-23"
related_files:
  - catalog/cloudgov/fred.yaml
  - catalog/cloudgov/fred_vmcp.yaml
  - catalog/cloudgov/README.md
  - docs/decisions/0002-fred-external-remote.md
---

# FRED MCP Connector

> **Status:** Hub integration pilot; not authorized for production use.
> **Live tested (human-reported, 2026-11-23):** The maintainer reported that all
> live acceptance checks passed. The AI agent did not execute these tests or
> receive raw test outputs; see the verification record below.

## Provider and boundary

The official FRED MCP Connector is operated by the FRED team in the Research
Division of the Federal Reserve Bank of St. Louis. It provides access to FRED
economic time series, including data from federal statistical agencies and
other providers. It is not one of the independent community FRED MCP servers.
The Claude directory's “Community” label describes Anthropic's review category,
not the identity of the operator or GSA approval.

**Endpoint:** `https://mcp.stlouisfed.org` (no added `/mcp` path).

This public HTTPS service is **outside the GSA hub boundary**. Obot forwards
tool requests and arguments to the provider; an Obot proxy does not bring the
upstream service inside that boundary. GSA does not host or operate it, and
cloud.gov internal routing/C2C protections do not apply to the upstream hop.
Use public research inputs only. Do not send PII, CUI, credentials, or nonpublic
government information without appropriate authorization. Catalog inclusion
does not establish an ATO, FedRAMP status, or approval for sensitive data.

## Connect

1. Launch **FRED** in Obot, not **FRED External Component**.
2. Use the gateway-issued `https://<obot-host>/mcp-connect/<vmcp-id>` URL,
   without `/mcp`. Do not assume the runtime ID equals the catalog key `fred`.
3. Authenticate to Obot using OAuth or a scoped API key for this vMCP.
4. Complete the provider's separate authorization flow when prompted. First-time
   users choose **Sign up** in the provider's Okta view, create a free **FRED MCP
   Connector account**, and accept the provider's Terms of Service and Privacy
   Policy. An existing FRED user account does not sign in to the connector.
5. Returning users sign in with their connector account. The same account can
   be used across assistants, with separate authorization for each assistant.

The connector is free and requires **no FRED API key**. The component uses
`serverUserType: singleUser` because upstream authorization is per user; no
credential fields or shared account are configured. This declaration alone
does not prove OAuth compatibility or credential isolation in the gateway.
Do not manually copy tokens or account credentials into YAML or headers.

For direct connections outside Obot, the provider advertises the exact endpoint
above and a [Claude directory entry](https://claude.ai/directory/fred).
Direct use does not exercise hub access controls or validate the hub integration.

## Tools and examples

| Tool | Purpose |
|---|---|
| `fred-search-series` | Search economic time series by keywords or concepts |
| `fred-get-series-metadata` | Inspect units, frequency, seasonal adjustment, sources, and notes |
| `fred-get-series-observations` | Retrieve data with date ranges, transformations, or lower-frequency aggregation |
| `fred-download-series-observations-link` | Generate CSV or JSON download links |
| `fred-graph-series` | Create interactive graphs with up to five series |

The `everyone` profile permits authenticated Obot users, not anonymous access.
Only these five tools are allowlisted; future tools require reviewed policy
updates. Catalog previews are based on the supplied provider descriptions, not
live discovery. Parameter names are intentionally omitted until verified.
Use the exact names returned by gateway `tools/list`, which may be qualified.

Example prompts:

- “What is the latest unemployment rate?”
- “How has inflation changed over the past five years?”
- “Compare CPI and PCE inflation.”
- “Graph the federal funds rate since 1990.”
- “Download monthly unemployment since 1980 as CSV.”

## Data limitations

- Verify the series ID, units, frequency, seasonal adjustment, and source.
  An unemployment percentage is already a rate; a price index is not inflation.
- `.` means missing data, not zero. Observation dates identify the measured
  period, not publication or retrieval dates.
- Statistics can be revised; `realtime_start` and `realtime_end` record as-of
  dates. The provider points to ALFRED for earlier vintages; this listing does
  not claim that these five tools support ALFRED vintage retrieval.
- AI-generated analysis can contain mistakes. Verify important research
  against source data. FRED does not provide financial, investment, legal, or
  policy advice.

## Live acceptance gate and verification record

This is the durable, repository-local record for FRED acceptance. On 2026-11-23,
the requesting maintainer reported live testing through the catalog, working
tools, and that **all checks passed**. The table records that human report,
not an AI-executed verification transcript. Raw test outputs, client identity,
and detailed test inputs were not supplied to the AI agent.

| Acceptance check | Result reported on 2026-11-23 |
|---|---|
| Catalog synchronization and FRED launch | PASS (human-reported) |
| Permitted HTTPS egress, MCP initialization, authentication discovery, and upstream OAuth through Obot | PASS (human-reported) |
| Live `tools/list` matches the five-tool allowlist; no additional tools exposed | PASS (human-reported) |
| Real calls covering search, metadata, observations, download link, and graph | PASS (human-reported) |
| Real external-client connection using the gateway-issued URL | PASS (human-reported) |
| Unauthenticated rejection, two-user authorization isolation, and upstream revocation/reauthorization | PASS (human-reported) |

All previously blocked acceptance steps are recorded as passed on this basis.
This does not grant production or sensitive-data authorization, accept the
proposed ADR, or establish that every client or future upstream release works.

### Repeatable acceptance procedure

For future validation, repository maintainers need approved gateway test access,
a FRED MCP Connector test account, and permitted upstream egress. Capture actual
results without credentials or sensitive response metadata:

1. Synchronize the catalog and launch FRED successfully.
2. Verify permitted HTTPS egress, MCP initialization, authentication discovery,
   and successful provider OAuth through Obot. No upstream `/health` endpoint
   is documented; do not invent one or apply the internal-app migration gate.
3. Compare live `tools/list` with the five-tool allowlist; confirm no additional
   upstream tool is exposed.
4. Execute real `tools/call` requests with public inputs (for example `UNRATE`),
   covering search, metadata, observations, a download link, and a graph.
5. Connect from a real external MCP client using the gateway-issued URL.
6. Verify unauthenticated rejection, isolation between two users' upstream
   authorizations, and upstream revocation/reauthorization behavior. Do not
   assume a scoped Obot API key bypasses FRED authorization.

### Earlier agent-side attempts (2026-11-13)

On 2026-11-13, `git fetch origin main` succeeded. Fetching the assumed provider
documentation URL `https://fred.stlouisfed.org/mcp` failed with a transport error;
its path remains unconfirmed. A TLS-verified request to
`https://mcp.stlouisfed.org/.well-known/oauth-protected-resource` failed to connect
(curl exit 7). No discovery response, tool inventory, or OAuth result was
observed. Descriptions and tool names come from the user-supplied website and
directory text. These earlier environment failures are preserved as history;
they are not the current status of the maintainer-tested hub integration.
Static validation alone does not prove live behavior.

## Rollback and review

Withdraw both FRED manifests and synchronize the catalog. Check whether
launched instances need explicit removal or access revocation in Obot, and
revoke provider authorizations where appropriate. Leave other products intact.

AI-assisted catalog content requires human review before merge. Review external
data flows, provider terms/privacy, egress approval, and per-user OAuth evidence.
See the [proposed decision record](../decisions/0002-fred-external-remote.md).
