# GLOSSARY.md format

Preserve the repository's existing glossary path and formatting if one exists. Use this format when adding entries to a standard `GLOSSARY.md` or creating an approved new glossary.

## Single-context layout

```markdown
# {Domain / Context Name}

{1-2 sentences stating the problem domain this context owns.}

## Terms

**Order**:
A customer's confirmed commitment to purchase specific line items at quoted prices.
_Avoid_: Cart, purchase, transaction

**Invoice**:
A payment demand issued after fulfillment dispatches one or more shipments for an Order.
_Avoid_: Bill, receipt
```

## Entry rules

- **Pick one canonical term per concept.** List competing words found in discussions, tickets, or legacy code under `_Avoid_` so new code converges on one name.
- **Keep definitions to 1–2 plain sentences** stating the domain meaning and boundary conditions (for example, what distinguishes a `DraftOrder` from an `Order`).
- **Exclude implementation details and generic tech terms.** Leave SQL tables, endpoints, framework classes, and general programming terms (`Cache`, `Timeout`, `Webhook`, `Adapter`) out of the glossary.
- **Add subheadings only when distinct clusters emerge**; keep small glossaries flat.

## Multi-context repositories

When the same word intentionally means different things in separate subsystems (for example, an `Account` in Auth vs an `Account` in Ledger), keep a root `GLOSSARY-MAP.md` pointing to each bounded context's glossary and summarizing how those contexts translate between each other:

```markdown
# Glossary map

## Contexts

- [Ordering](./src/ordering/GLOSSARY.md): order capture, pricing lock, and cancellation rules
- [Billing](./src/billing/GLOSSARY.md): invoicing, payment capture, and refunds
- [Fulfillment](./src/fulfillment/GLOSSARY.md): inventory reservation, picking, and shipment dispatch

## Context translations

- **Ordering → Fulfillment:** `OrderConfirmed` carries `OrderId` and line SKUs; Fulfillment creates `Shipment` records.
- **Fulfillment → Billing:** `ShipmentDispatched` triggers `Invoice` generation.
```
