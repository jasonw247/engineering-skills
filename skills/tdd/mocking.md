# Boundary Doubles and Mocking

Place test doubles at **external system boundaries**:
- Third-party HTTP APIs (payments, email, identity providers)
- Clocks, timers, and random number generators
- External queues or object stores
- Databases or filesystems only when real local/in-memory instances are impractical or when injecting I/O faults

Avoid mocking internal functions or classes inside the same module boundary to assert call choreography. When injecting a fake to simulate timeouts, permission denials, or disk-full errors, assert the caller-visible recovery or error result and keep at least one integration check against the real adapter.

## Keeping boundaries easy to fake

Use the repository's existing boundary seams first; introduce injection parameters only when an ownership or testability boundary genuinely needs them.

### 1. Pass external clients explicitly

```typescript
// Testable without global monkey-patching
function processPayment(order, paymentClient) {
  return paymentClient.charge(order.total);
}

// Hardwires credentials and network I/O inside business logic
function processPayment(order) {
  const client = new StripeClient(process.env.STRIPE_KEY);
  return client.charge(order.total);
}
```

### 2. Prefer domain-operation clients over raw URL fetchers

When wrapping an external service, operation-level methods make test doubles simple and type-checked (avoid adding thin wrappers around internal functions that have no external boundary):

```typescript
// GOOD: Each external operation stubs one return shape cleanly
const userDirectory = {
  getUser: (id) => fetch(`/users/${id}`),
  getOrders: (userId) => fetch(`/users/${userId}/orders`),
  createOrder: (data) => fetch("/orders", { method: "POST", body: data }),
};

// AWKWARD: Fakes must parse URL strings and HTTP methods in conditionals
const api = {
  fetch: (endpoint, options) => fetch(endpoint, options),
};
```
