# 2. Use alpha versioning during initial development

Date: 2023-11-07

## Status

Accepted

## Context

Semantic versioning is a (sometimes) helpful communication tool to help users know when to expect they'll need to respond to, or at least be aware of, changes that break an API. Semantic versioning communicates a different set of concepts altogether than calendar versioning, and although it leaves room for subjectivity and human error is currently the prevailing approach.

During initial development of a project, many changes may be breaking changes. If semantic versioning is followed well during this phase, the outcome is a fast-increasing version number. By the time the project stabilizes, there may already have been tends or even hundreds of breaking changes.

Choosing the right semantic version also carries a mild cognitive burden and can create points of drawn out discussion. Left to these devices, initial development can be slowed by too much back-and-forth.

## Decision

Use alpha versioning during initial development such that all versions are monotonically increasing versions of the form `0.0.XYZ`.

## Consequences

- Consumers won't know when a change is breaking, and should assume _every_ change is breaking
- This decision will need to be amended once the project matures into a stable release pattern
- There is sometimes confusion about versions like `0.0.996` and people try to install `0.99.6` or similar instead
- Every released change during initial development will simply increase the last portion of the version string by one
