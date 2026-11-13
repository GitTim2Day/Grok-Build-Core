2026-11-13T07:08-05:00 America/New_York

LAN/WAN links map for Shepherd brain (NTP + selective xAI).

WAN NTP (time lock for SVCT):
- pool.ntp.org (0/1/2/3.pool.ntp.org)
- us.pool.ntp.org
- north-america.pool.ntp.org
- Status: https://www.ntppool.org/zone/

WAN xAI/Grok API (direct, no browser):
- Base: https://api.x.ai
- US regional: https://us.api.x.ai/v1
- POST /v1/chat/completions
- POST /v1/responses
- GET /v1/models
- Docs: https://docs.x.ai/docs/api-reference

LAN:
- Prefer local NTP once stood up on the network.
- Local services (redaction, Cubie AN, etc.) stay inside shell/firewall.

Pi 5 functional checks:
timedatectl status
chronyc tracking
ping -c 3 pool.ntp.org
curl -s -o /dev/null -w "%{http_code}\n" https://api.x.ai/v1/models

All listed WAN endpoints operational at mapping time. Pi needs NTP pool for continuous time; xAI base + key only when selective call is earned.

Pattern-match-map-audit-remap complete. Email hop: 1a1d4cf7f96a2a5a. Notion: 417c9bfe-3aff-817c-bb13-d4a3b013b036.
