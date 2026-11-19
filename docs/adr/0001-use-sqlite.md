# Title

Use SQLite for the Team Directory service

## Status

Accepted

## Context

The Team Directory is a single-instance service with a small, low-write dataset. Writes occur only when a team roster changes. We want no additional infrastructure to operate.

## Decision

We chose SQLite over PostgreSQL for the Team Directory service.

## Consequences

SQLite does not handle concurrent writes from multiple processes well. Revisit this decision if the service is scaled to multiple replicas.