# Good and Bad Tests

## Behavior-focused tests

Test observable outcomes through stable interfaces rather than mocking internal collaborators:

```typescript
// GOOD: Verifies caller-visible behavior
test("user can checkout with valid cart", async () => {
  const cart = createCart();
  cart.add(product);
  const result = await checkout(cart, paymentMethod);
  expect(result.status).toBe("confirmed");
});
```

What makes this durable:
- Exercises behavior callers rely on
- Uses a stable public seam that survives internal refactoring
- Names the expected outcome rather than internal method calls
- Asserts one coherent contract per test

## Fragile test patterns

### 1. Implementation-detail coupling

```typescript
// BAD: Locks in internal call structure without proving checkout succeeds
test("checkout calls paymentService.process", async () => {
  const mockPayment = jest.mock(paymentService);
  await checkout(cart, mockPayment);
  expect(mockPayment.process).toHaveBeenCalledWith(cart.total);
});
```

Warning signs to check (justified only when persistence, audit logging, or call ordering is itself the contract):
- Mocking internal modules inside the same package
- Calling private methods or exporting helpers just for tests
- Asserting exact internal call counts or intermediate variable shapes
- Test breaks during a pure behavior-preserving refactor

Prefer testing round-trip behavior over raw table inspection when retrievability is the requirement:

```typescript
// Misses bugs in the read/deserialization path
test("createUser writes row", async () => {
  await createUser({ name: "Alice" });
  const row = await db.query("SELECT * FROM users WHERE name = ?", ["Alice"]);
  expect(row).toBeDefined();
});

// Exercises the full create-and-read contract
test("created user can be retrieved by id", async () => {
  const user = await createUser({ name: "Alice" });
  const retrieved = await getUser(user.id);
  expect(retrieved.name).toBe("Alice");
});
```

### 2. Tautological expected values

```typescript
// BAD: Mirrors the implementation formula, so a shared bug passes
test("calculateTotal sums line items", () => {
  const items = [{ price: 10 }, { price: 5 }];
  const expected = items.reduce((sum, i) => sum + i.price, 0);
  expect(calculateTotal(items)).toBe(expected);
});

// GOOD: Independent known literal
test("calculateTotal sums line items", () => {
  expect(calculateTotal([{ price: 10 }, { price: 5 }])).toBe(15);
});
```
