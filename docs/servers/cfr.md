# CFR MCP Server

> **Status:** Pilot / proof of concept. Not intended for production use.

## Overview

The CFR MCP server exposes the Code of Federal Regulations (CFR) and the
Federal Register as a set of MCP tools built for NEPA/EIS regulatory citation
and compliance work. It resolves CFR citations to verbatim text, browses the
CFR table of contents, tracks amendment history, diffs a section between two
dates, and traces the Federal Register rulemaking behind a regulation — all
through natural-language requests routed through the obot MCP gateway.

- **Data sources:**
  - [eCFR API](https://www.ecfr.gov/developers/documentation/api/v1) — current
    and historical CFR text, structure, versions, and ancestry.
  - [Federal Register API](https://www.federalregister.gov/developers/documentation/api/v1)
    — rules, proposed rules, notices, and Presidential Documents (executive
    orders).
- **Source repository:** [GSA-TTS/nepa-mcp](https://github.com/GSA-TTS/nepa-mcp)
  (a fork of [pnnl/nepa-mcp](https://github.com/pnnl/nepa-mcp); the CFR server
  is containerized additively under `docker/cfr/`).
- **Runtime:** `containerized` — hosted by the gateway from the public image
  `ghcr.io/gsa-tts/mcp-server-nepa-cfr` (`:8080/mcp`, health at `/health`).
  The container has no public route; it is reachable only through the gateway.
- **Authentication:** None required — queries the public eCFR and Federal
  Register APIs.

## Design principles

- **Never raise for navigation.** `cfr_resolve_citation` falls back to the
  deepest matching ancestor with a `resolution_warning` when a paragraph path
  no longer resolves at the requested date.
- **Token-efficient output.** Structure browsing prunes to a caller-chosen
  depth; version diffs omit unchanged paragraphs from the body.
- **Structured JSON** with a `source` and UTC `retrieved` timestamp on every
  response for a defensible record.

## Tools

The server registers the following tools.

| Tool | Description |
|------|-------------|
| `cfr_resolve_citation` | Resolve a CFR citation (any depth) to its verbatim text, heading, ancestry, and in-text FR citations. |
| `cfr_browse_structure` | Browse the CFR TOC: list all 50 titles, or drill into a title or part pruned to a chosen depth. |
| `cfr_history` | All eCFR amendment events for a citation (section, part, or title) in a date window, with a substantive-only filter. |
| `cfr_compare_versions` | Per-paragraph diff of a single section between two dates, optionally scoped to a subtree. |
| `cfr_rulemaking` | Federal Register documents that touched a CFR title/part, optionally correlated to eCFR amendment events. |
| `cfr_resolve_fr_citation` | Resolve a Federal Register citation (e.g. `90 FR 29498`) to its source document and summary. |
| `cfr_resolve_executive_order` | Resolve an Executive Order number to its Federal Register Presidential Document record. |

## Example prompts

- "What does 40 CFR 1502.14 say today?"
- "Show the structure of 40 CFR Part 1500 down to the section level."
- "What amendments hit 33 CFR 328.3 in the last 5 years?"
- "Diff 40 CFR 230.10 between 2015-01-01 and 2024-01-01."
- "What Federal Register rules touched 43 CFR Part 46 last year?"
- "Resolve the citation 90 FR 29498."
- "Look up Executive Order 14008."

## References

- [eCFR API documentation](https://www.ecfr.gov/developers/documentation/api/v1)
- [Federal Register API documentation](https://www.federalregister.gov/developers/documentation/api/v1)
- [Source repository](https://github.com/GSA-TTS/nepa-mcp)
- [Upstream project (PNNL)](https://github.com/pnnl/nepa-mcp)
- [Model Context Protocol](https://modelcontextprotocol.io/)
