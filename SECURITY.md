# Security Policy

The U.S. General Services Administration (GSA) takes seriously its
responsibility to protect public information and systems. This repository is
subject to the [GSA Vulnerability Disclosure Policy](https://www.gsa.gov/website-information/vulnerability-disclosure-policy).

## Reporting A Vulnerability

Do not open a public GitHub issue or pull request for a suspected vulnerability.
Report it privately through this repository's
[GitHub security advisory form](https://github.com/GSA-TTS/mcp-server-hub-catalog/security/advisories/new).

Include, when available:

- the affected branch, catalog entry, or vMCP;
- a description of the vulnerability and its potential impact;
- reproducible steps or a minimal proof of concept; and
- any suggested remediation.

Do not include credentials, tokens, personal information, or government data in
the report. GSA will coordinate validation and disclosure under its
Vulnerability Disclosure Policy.

## Supported Branches

| Branch | Security support |
|---|---|
| `main` | Supported primary cloud.gov catalog |
| `aws` | Supported legacy pilot during the cloud.gov parity period |
| Other branches | Not supported |

## Research Guidelines

Security researchers must:

- avoid privacy violations, service degradation, disruption, and data
  destruction or manipulation;
- use exploits only as necessary to confirm a vulnerability;
- never exfiltrate data, establish persistence, or pivot to other systems;
- stop testing and report immediately after confirming a vulnerability or
  encountering sensitive data; and
- keep vulnerability details confidential during coordinated disclosure.

Authorization and safe-harbor terms are governed by the GSA Vulnerability
Disclosure Policy linked above.
