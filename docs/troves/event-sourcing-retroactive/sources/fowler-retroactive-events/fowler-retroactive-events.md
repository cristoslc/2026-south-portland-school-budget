---
source-id: "fowler-retroactive-events"
title: "Retroactive Event"
type: web
url: "https://martinfowler.com/eaaDev/RetroactiveEvent.html"
fetched: 2026-04-05T00:00:00Z
hash: "d27ed144aa8a18f793425f9e6496a69c4f59575a1d4233392cfef620a69dd7cc"
---

# Retroactive Event

## Core Concept

This architectural pattern addresses a critical enterprise application challenge: automatically correcting consequences of incorrect events already processed in an event sourcing system. As Fowler notes, "the computations they carry out and the actions they initiate can only be as accurate as the information they receive."

## How It Works

The pattern operates using three parallel models:

1. **Incorrect reality** -- current live state without the retroactive event
2. **Correct branch** -- state that should exist if the event had been processed correctly
3. **Corrected reality** -- final desired state

The system identifies a "branch point" where these models diverge, then reconstructs the correct state through either:

- **Rebuild**: Reverting to the last snapshot and replaying events forward
- **Rewind**: Reversing events backward from the latest event to the branch point

## Three Types of Retroactive Events

1. **Out-of-order events** -- received late, requiring insertion and forward processing
2. **Rejected events** -- determined to be false, requiring reversal and marking
3. **Incorrect events** -- containing wrong information, requiring reversal and correction

## Implementation Complexity

The pattern demands significant prerequisites: Event Sourcing foundation, plus either event reversibility or parallel model capabilities. External system integration adds substantial complexity requiring detection and correction logic for mismatched updates.

## When to Use It

Implementation is justified when frequent manual error corrections consume significant human effort. The pattern works best in limited scope applications -- specific system areas with minimal external dependencies, or within fixed business cycles (weekly, monthly) before operations close.
