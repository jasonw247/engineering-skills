"""Synthetic fixture for codebase-design evaluation."""


class TenantAuthorizer:
    """Enforces tenant isolation before any order mutation."""

    def assert_member(self, actor_tenant_id: str, resource_tenant_id: str) -> None:
        if actor_tenant_id != resource_tenant_id:
            raise PermissionError("cross-tenant access denied")


class OrderRepository:
    def __init__(self, db):
        self._db = db

    def save_order(self, tenant_id: str, items: list[dict]) -> str:
        return self._db.insert("orders", {"tenant_id": tenant_id, "items": items})


class OrderProcessor:
    def __init__(self, repo: OrderRepository):
        self._repo = repo

    def process(self, tenant_id: str, items: list[dict]) -> str:
        return self._repo.save_order(tenant_id, items)


class OrderManager:
    def __init__(self, processor: OrderProcessor):
        self._processor = processor

    def create(self, tenant_id: str, items: list[dict]) -> str:
        return self._processor.process(tenant_id, items)


class OrderController:
    def __init__(self, authorizer: TenantAuthorizer, manager: OrderManager):
        self._authorizer = authorizer
        self._manager = manager

    def post_order(self, actor_tenant_id: str, payload: dict) -> str:
        self._authorizer.assert_member(actor_tenant_id, payload["tenant_id"])
        return self._manager.create(payload["tenant_id"], payload["items"])


def parse_csv_header(header_line: str) -> dict[str, int]:
    cols = [c.strip() for c in header_line.split(",")]
    if "sku" not in cols or "qty" not in cols:
        raise ValueError("missing required columns")
    return {name: idx for idx, name in enumerate(cols)}


def parse_csv_rows(lines: list[str], col_map: dict[str, int]) -> list[dict]:
    # Assumes caller passed output of parse_csv_header with exact keys 'sku' and 'qty'
    return [
        {
            "sku": parts[col_map["sku"]].strip(),
            "qty": int(parts[col_map["qty"]].strip()),
        }
        for line in lines
        if line.strip()
        for parts in [line.split(",")]
    ]
