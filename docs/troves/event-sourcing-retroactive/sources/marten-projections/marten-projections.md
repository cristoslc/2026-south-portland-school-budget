---
source-id: "marten-projections"
title: "Projections in Marten"
type: web
url: "https://martendb.io/events/projections/"
fetched: 2026-04-05T00:00:00Z
hash: "2535d1abd47d0f9ff4fedcc63e5bbcd672925c9945b064327e9df9b6190b1d09"
---

# Projections in Marten

## Overview

Projections transform event data into queryable views. The documentation explains: "the role of a projection in your system fits into one of the buckets below" -- write models for command handlers, read models for clients, or query models for reporting.

## Three Projection Approaches

Marten supports three execution strategies:

1. **Live Aggregation** -- Events are computed in-memory on-demand without persistence
2. **Inline Projections** -- Projected documents update synchronously during event capture
3. **Asynchronous Projections** -- Background daemon updates projections with eventual consistency

## Aggregate Pattern

The conventional approach uses `public Apply()` methods on aggregate classes. Example:

```csharp
public sealed record QuestParty(Guid Id, List<string> Members)
{
    public static QuestParty Apply(MembersJoined joined, QuestParty party) =>
        party with { Members = party.Members.Union(joined.Members).ToList() };
}
```

Aggregates can be queried live: `var party = await session.Events.AggregateStreamAsync<QuestParty>(questId);`

## Projection Types

- **Single Stream Projections** -- Combine events from one stream into a view
- **Multi Stream Projections** -- Aggregate events across arbitrary stream groupings
- **Event Projections** -- Create/delete documents per single event
- **Custom Aggregations** -- Advanced logic beyond built-in recipes
- **Flat Table Projections** -- Denormalized PostgreSQL tables for reporting

## Key Features

- Integration with PostgreSQL's document database capabilities
- Logging support via `ILogger` when bootstrapped through `AddMarten()`
- Projection rebuilding when code changes require re-applying events
- Default constructor requirement (public, private, or protected)
