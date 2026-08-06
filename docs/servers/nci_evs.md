# NCI EVS MCP Server

> **Status:** Pilot / proof of concept. Not intended for production use.

## Overview

The NCI EVS MCP server exposes the National Cancer Institute
[Enterprise Vocabulary Services (EVS)](https://evs.nci.nih.gov/) API as a set of
MCP tools. EVS provides programmatic access to NCI cancer terminology and
biomedical concepts across two terminologies:

- **NCIt (NCI Thesaurus)** — a standardized, curated vocabulary for cancer
  research and clinical care.
- **NCIm (NCI Metathesaurus)** — an integration of multiple biomedical
  vocabularies including UMLS and SNOMED CT.

The server lets an AI application search concepts, filter by terminology
properties, navigate the concept hierarchy (parents, children, descendants),
and retrieve detailed concept information — all through natural-language
requests routed through the obot MCP gateway.

- **Data source:** [NCI EVS REST API](https://api-evsrest.nci.nih.gov/)
- **Source repository:** [GSA-TTS/mcp-server-nci-evs](https://github.com/GSA-TTS/mcp-server-nci-evs)
- **Runtime:** `containerized` — hosted by the gateway from the public image
  `ghcr.io/gsa-tts/mcp-server-nci-evs` (`:8080/mcp`, health at `/health`).
  The container has no public route; it is reachable only through the gateway.
- **Authentication:** None required — queries the public EVS API.

## Tools

The server registers the following tools.

### Search & discovery

| Tool | Description |
|------|-------------|
| `search_concepts` | Primary search tool. Searches NCIt / NCIm for concepts with flexible match types (`contains`, `startsWith`, `phrase`, `exactMatch`, `fuzzy`), optional property/value filtering, definition and synonym source filters, sorting, and pagination. |
| `get_concepts` | Retrieves detailed metadata for one or more concepts by their codes, with a configurable detail level (`minimal`, `summary`, `full`, or specific aspects such as `properties`, `synonyms`, `definitions`). |

### Hierarchy navigation

| Tool | Description |
|------|-------------|
| `get_parents` | Returns the direct parent concepts (one level up) of a concept in the terminology hierarchy. |
| `get_children` | Returns the direct child concepts (one level down) of a concept in the terminology hierarchy. |
| `get_descendants` | Returns all descendant concepts (the entire subtree) of a concept, with `maxLevel` depth control and `fromRecord`/`pageSize` pagination. Primarily meaningful for NCIt. |

## Property filtering

`search_concepts` supports filtering by terminology-specific property codes via
the `property` and `value` parameters. The server ships two skill resources
documenting the available codes:

- **NCIt properties** (70 documented) — `skill://ncit-property-information/SKILL.md`
- **NCIm properties** (185+ documented) — `skill://ncim-property-information/SKILL.md`

Use the appropriate skill to resolve a plain-English concept (e.g. semantic
type, CAS Registry Number, HGNC ID, SNOMED ID) into the property code required
by the filter.

## NCIt vs NCIm: when to use each

**Use NCIt when** working with NCI Thesaurus concepts, standardized cancer
terminology, or US federal health data standards, or when you need clean,
curated terminology without source conflicts.

**Use NCIm when** you need cross-terminology mapping, are working with UMLS or
SNOMED CT concepts, need multilingual support, or need to trace concept origins
across multiple source vocabularies.

## Example prompts

- "Search NCIt for melanoma concepts."
- "Get full details for NCIt concept C3224."
- "What are the parent concepts of C3224?"
- "List all descendants of C3224 down to 3 levels."
- "Find NCIt concepts with a Semantic_Type of 'Disease or Syndrome'."

## References

- [NCI Enterprise Vocabulary Services](https://evs.nci.nih.gov/)
- [NCI EVS REST API documentation](https://api-evsrest.nci.nih.gov/)
- [NCI Thesaurus Browser](https://ncit.nci.nih.gov/ncitbrowser/)
- [Source repository](https://github.com/GSA-TTS/mcp-server-nci-evs)
- [Model Context Protocol](https://modelcontextprotocol.io/)
