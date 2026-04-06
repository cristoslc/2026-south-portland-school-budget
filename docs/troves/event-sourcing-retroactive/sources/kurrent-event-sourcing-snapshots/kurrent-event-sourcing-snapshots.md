---
source-id: "kurrent-event-sourcing-snapshots"
title: "Snapshots in Event Sourcing"
type: web
url: "https://www.kurrent.io/blog/snapshots-in-event-sourcing"
fetched: 2026-04-05T00:00:00Z
hash: "2f3ba0a6f31f80d91a5d0d8caa8b6b64eacd82dbe96a6d68b72afd7b5d3df531"
---

# Snapshots in Event Sourcing

## Overview

This comprehensive guide by Oskar Dudycz explores snapshots as a performance optimization technique in Event Sourcing systems. Snapshots store an aggregate's current state at a specific point in time, allowing systems to skip replaying previous events.

## What Are Snapshots?

Snapshots reduce the number of events needed to restore an aggregate's state. Rather than replaying thousands of events (like a bank account's 18,615+ transactions over 17 years), a snapshot stores the computed state, requiring only events after the snapshot for complete reconstruction.

## When to Create Snapshots

The article identifies four primary strategies:

1. **After each event** -- Eliminates event replaying but impacts write performance
2. **Every N events** -- Balances optimization with overhead
3. **On specific event types** -- Aligned with business operations (e.g., "shift ended")
4. **Scheduled intervals** -- Daily or hourly snapshots risk processing spikes between intervals

## Disadvantages

- **Schema versioning complexity** -- Long-lived streams require supporting multiple event schemas during migration
- **Design smell indicator** -- Snapshots may signal inadequate domain modeling rather than genuine performance needs
- **Read-write coupling risks** -- Using snapshots as read models introduces architectural coupling
- **Additional system complexity** -- Extra storage and potential staleness issues

## Alternatives to Snapshots

### Shorter Streams

Breaking streams into smaller, business-aligned lifecycles (cashier shifts, billing days) naturally reduces event counts. This aligns technical models with actual workflows and simplifies schema versioning -- old schema support ends when streams complete, enabling smoother deployments.

### "Closing the Books" Pattern

This mirrors real-world practices: create summary events when business cycles end, then archive old data. New periods begin with the summarized state rather than replaying history.

## Implementation Strategies

### Storage Locations

- Separate event stream (optimal for schema evolution)
- Same stream as regular events
- External databases or caches (Redis)
- In-memory storage (actor systems)

### Reading Approaches

**With snapshots:** Load the snapshot, then apply only subsequent events for complete current state.

**Snapshot metadata:** Store the snapshotted stream revision in metadata to know where to resume reading events.

### Asynchronous Snapshots

Subscriptions can monitor for snapshot-triggering events, avoiding write-path performance degradation. This trades real-time consistency for better throughput.

## Key Recommendation

Oskar emphasizes: "Treat snapshots as a tactical hotfix or optimisation" rather than foundational architecture. Evaluate domain modeling first -- better stream design often eliminates the need entirely.
