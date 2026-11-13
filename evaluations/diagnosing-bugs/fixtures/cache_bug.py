"""Synthetic fixture for diagnosing-bugs evaluation."""

ROLE_DEFAULTS = {
    "viewer": ["read"],
    "editor": ["read", "write"],
}

_PERM_CACHE: dict[tuple[str, str], list[str]] = {}


def get_user_permissions(user_id: str, tier: str) -> list[str]:
    key = (user_id, tier)
    if key not in _PERM_CACHE:
        _PERM_CACHE[key] = list(ROLE_DEFAULTS.get(tier, []))
    return _PERM_CACHE[key]
