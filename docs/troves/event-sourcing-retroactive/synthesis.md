# Event Sourcing Retroactive Patterns -- Synthesis

Trove: `event-sourcing-retroactive` | SPIKE-014, EPIC-037

---

## Snapshot Strategies

Event-sourced systems use snapshots to avoid replaying full event history on every read. Four trigger strategies appear in practice (`kurrent-event-sourcing-snapshots`):

- **Threshold-based (every N events)** -- the most common. Balances read optimization against write overhead. Requires storing the snapshotted stream revision in metadata so the reader knows where to resume.
- **Event-triggered** -- snapshots fire on specific business events (e.g., "shift ended", "books closed"). Aligns well with domain boundaries and supports the "closing the books" pattern, where a summary event caps a business cycle and new periods start from that summary.
- **Time-based (scheduled)** -- daily or hourly. Risks processing spikes between intervals and stale reads during gaps.
- **After every event** -- eliminates replay cost entirely but shifts all cost to the write path. Essentially an inline projection.

Storage options range from a separate snapshot stream (best for schema evolution) to external caches (Redis) or in-memory stores. The key insight: snapshots are a tactical optimization, not architecture. Better stream design -- shorter, lifecycle-aligned streams -- often removes the need (`kurrent-event-sourcing-snapshots`).

## Retroactive Event Patterns

When events arrive late, are rejected, or contain errors, the system must correct downstream state (`fowler-retroactive-events`). Two core strategies:

- **Rebuild** -- revert to the last snapshot before the branch point, insert or remove the retroactive event, replay forward. Straightforward but expensive for long histories.
- **Rewind** -- reverse events backward from current state to the branch point, apply the correction, then replay forward. Requires every event type to have a defined reverse operation.

Three retroactive event types: out-of-order (late arrival), rejected (false event), and incorrect (wrong data). Each demands different handling. External system integration is the hardest part -- side effects already dispatched to other systems need detection and correction.

Fowler recommends limiting retroactive scope to bounded areas with minimal external dependencies, or within fixed business cycles before period close.

## Projection Lifecycles

Marten's projection model (`marten-projections`) maps cleanly to three execution modes:

- **Live (on-demand)** -- computed in-memory per request. No storage cost, always current, but expensive for complex aggregates.
- **Inline (synchronous)** -- updated during event capture in the same transaction. Strong consistency but couples read and write performance.
- **Async (eventual)** -- a background daemon processes events. Best throughput, but reads may lag behind writes.

Projection types range from single-stream aggregations to multi-stream views that combine events across arbitrary groupings. The `Apply()` pattern -- a pure function from (event, current-state) to new-state -- is the universal building block.

Projection rebuilding is a first-class operation: when projection code changes, the system replays all events through the new logic to regenerate views.

## Aggregate Stream Snapshots and Schema Evolution

Long-lived streams face schema drift as event shapes change over time. Snapshots encode a point-in-time schema, so older snapshots may not match current event versions (`kurrent-event-sourcing-snapshots`). Storing snapshots in a separate stream from events isolates this concern. The "closing the books" pattern sidesteps the problem entirely -- old streams terminate and new ones start fresh with current schemas.

## Gaps Relevant to Our Use Case

The prior art assumes **linear event streams** -- one ordered sequence per aggregate. Our fold event model uses a **DAG-structured event log** where events can have multiple parents and the topology is not strictly linear. This affects:

- **Snapshot placement** -- in a linear stream, a snapshot covers "everything up to revision N." In a DAG, a snapshot must reference a set of event nodes (a cut across the graph), not a single position.
- **Retroactive insertion** -- Fowler's branch-point model assumes a single timeline. In a DAG, inserting a retroactive event may affect multiple downstream paths, requiring multi-path replay.
- **Shared state across projections** -- standard projections are independent views. Our personas share underlying evidence pools and can cross-reference each other's fold state. No source addresses projection interdependence or shared mutable context between projection instances.
- **Projection identity** -- Marten ties projections to aggregate IDs or stream groupings. Our "projections" (persona briefs) are identified by persona + evidence pool + fold generation, a composite key with no direct analog in the literature.

These gaps confirm that SPIKE-014 needs to design novel checkpoint and replay semantics rather than directly adopting any single pattern from the sources.
