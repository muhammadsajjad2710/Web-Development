"""Utility helpers."""

import re
import secrets
import string
from datetime import datetime, timezone
from typing import Optional
from uuid import uuid4


def slugify(value: str) -> str:
    value = value.lower().strip()
    value = re.sub(r"[^\w\s-]", "", value)
    value = re.sub(r"[\s_-]+", "-", value)
    return value.strip("-")[:200] or f"item-{uuid4().hex[:8]}"


def unique_slug(base: str, exists_fn) -> str:
    slug = slugify(base)
    candidate = slug
    counter = 1
    while exists_fn(candidate):
        candidate = f"{slug}-{counter}"
        counter += 1
    return candidate


def generate_order_number(prefix: str = "OR") -> str:
    stamp = datetime.now(timezone.utc).strftime("%y%m%d")
    suffix = "".join(secrets.choice(string.digits) for _ in range(5))
    return f"{prefix}-{stamp}-{suffix}"


def generate_reset_token() -> str:
    return secrets.token_urlsafe(32)


def paginate(total: int, page: int, page_size: int) -> dict:
    pages = max(1, (total + page_size - 1) // page_size) if total else 1
    return {
        "total": total,
        "page": page,
        "page_size": page_size,
        "pages": pages,
    }


def mask_phone(phone: Optional[str]) -> Optional[str]:
    if not phone or len(phone) < 4:
        return phone
    return "*" * (len(phone) - 4) + phone[-4:]
