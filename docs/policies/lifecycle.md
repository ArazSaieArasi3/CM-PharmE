# Semantic Entity Lifecycle Policy

Released concepts, relations, and domains are not hard-deleted from CM-PharmE history.

## Lifecycle States

- `Proposed`: candidate entity not yet part of a stable release.
- `Active`: current valid entity.
- `Deprecated`: still present but new use is discouraged.
- `Retired`: no longer part of the current model but preserved historically.
- `Superseded`: replaced by one or more explicitly linked successor entities.

## Stable Identifier Rule

Once an identifier has appeared in a stable release, it is never reused for a different semantic entity.

## Semantic Evolution

Rename without semantic change retains the same stable identifier. Semantic replacement, split, or merge is represented explicitly through new entities and lineage links. Historical release membership remains reproducible.
