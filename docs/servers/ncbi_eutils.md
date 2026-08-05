# NCBI E-Utils MCP Server

> **Status:** Pilot / proof of concept. Not intended for production use.

## Overview

The NCBI E-Utils MCP server exposes the
[NCBI Entrez E-utilities](https://www.ncbi.nlm.nih.gov/books/NBK25501/) as MCP
tools. The E-utilities are the public programmatic interface to NCBI's Entrez
system — a set of interconnected biomedical databases including PubMed, PMC,
Gene, Protein, Nucleotide, and many others.

The server maps the nine core E-utilities to MCP tools and adds a small workflow
layer for common agent tasks such as search-then-summary and search-then-fetch.

- **Data source:** [NCBI Entrez E-utilities](https://www.ncbi.nlm.nih.gov/books/NBK25501/)
- **Source repository:** [GSA-TTS/mcp-server-ncbi-eutils](https://github.com/GSA-TTS/mcp-server-ncbi-eutils)
- **Runtime:** `containerized` — hosted by the gateway from the public image
  `ghcr.io/gsa-tts/mcp-server-ncbi-eutils` (`:8080/mcp`, health at `/health`).
  The container has no public route; it is reachable only through the gateway.
- **Authentication:** None required — queries the public NCBI E-utilities API.

## Shared conventions

- Databases and search fields are validated live through `EInfo` rather than a
  hardcoded list.
- Tools accept either direct identifiers (`ids`) or Entrez History inputs
  (`webenv`, `query_key`) when the underlying utility supports both.
- Tools return both concise text and structured, JSON-friendly data.
- Raw upstream payloads are preserved when requested via `include_raw`.
- Errors carry actionable messages for invalid `db`, unsupported format
  combinations, or empty result sets.

## Core tools

These tools map closely to the underlying E-utilities.

| Tool | Backing utility | Purpose |
|------|-----------------|---------|
| `eutils_info` | `EInfo` | Discover databases, fields, links, and database metadata. |
| `eutils_search` | `ESearch` | Search an Entrez database and return UIDs and optional history tokens. |
| `eutils_post` | `EPost` | Upload UIDs to the Entrez History server. |
| `eutils_summary` | `ESummary` | Retrieve document summaries for UIDs or history-backed result sets. |
| `eutils_fetch` | `EFetch` | Retrieve full records in supported `rettype`/`retmode` formats. |
| `eutils_link` | `ELink` | Traverse related records across or within databases. |
| `eutils_global_query` | `EGQuery` | Run a cross-database query and return counts by database. |
| `eutils_spell` | `ESpell` | Retrieve spelling suggestions for a query. |
| `eutils_citation_match` | `ECitMatch` | Resolve citation strings to PubMed identifiers. |

### Key inputs and outputs

- **`eutils_info`** — inputs: `db` (optional; omit to list databases), `version`
  (optional `2.0`). Outputs: `databases`, `db_info`, `fields`, `links`.
- **`eutils_search`** — inputs: `db`, `term`, `retstart`, `retmax`, `sort`,
  `usehistory`, `field`, `datetype`, `mindate`, `maxdate`, `reldate`, `idtype`.
  Outputs: `count`, `ids`, `query_translation`, `translation_stack`, `retstart`,
  `retmax`, `history`.
- **`eutils_post`** — inputs: `db`, `ids`. Outputs: `query_key`, `webenv`,
  `count`.
- **`eutils_summary`** — inputs: `db`, `ids`, `webenv`, `query_key`, `retstart`,
  `retmax`, `version`. Outputs: `db`, `result_count`, `summaries`.
- **`eutils_fetch`** — inputs: `db`, `ids`, `webenv`, `query_key`, `rettype`,
  `retmode`, `retstart`, `retmax`. Outputs: `db`, `record_count`, `format`,
  `records` or `raw_payload`.
- **`eutils_link`** — inputs: `dbfrom`, `db`, `ids`, `webenv`, `query_key`,
  `linkname`, `cmd`. Outputs: `source_db`, `target_db`, `linksets`, `history`.
- **`eutils_global_query`** — inputs: `term`. Outputs: `term`, `results`.
- **`eutils_spell`** — inputs: `db`, `term`. Outputs: `query`,
  `corrected_query`, `replaced`.
- **`eutils_citation_match`** — inputs: `citations`, `raw`. Outputs: `matches`,
  `unmatched`.

## Workflow helpers

Convenience tools built on top of the core layer.

| Tool | Purpose |
|------|---------|
| `eutils_search_and_summary` | Search a database and immediately summarize the matching records. |
| `eutils_search_and_fetch` | Search a database and immediately fetch the matching records. |
| `eutils_find_related` | Search or summarize a source set, then follow links to related records in a target database. |

## Example prompts

- "Search PubMed for recent reviews on CRISPR gene editing and summarize the
  top results."
- "Find the PubMed record for this citation and return its abstract."
- "Given a gene, find related protein records in NCBI."
- "How many results match 'long COVID' across all NCBI databases?"

## References

- [NCBI E-utilities documentation](https://www.ncbi.nlm.nih.gov/books/NBK25501/)
- [Entrez Programming Utilities Help](https://www.ncbi.nlm.nih.gov/books/NBK25497/)
- [Source repository](https://github.com/GSA-TTS/mcp-server-ncbi-eutils)
- [Model Context Protocol](https://modelcontextprotocol.io/)
