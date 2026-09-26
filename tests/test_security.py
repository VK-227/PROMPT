from __future__ import annotations

import pytest

from common.rate_limit import SlidingWindowRateLimiter


def test_rate_limiter_allows_within_limit_and_rejects_burst():
    limiter = SlidingWindowRateLimiter(limit=2, window_seconds=60, max_clients=4)

    assert limiter.allow("client-a", now=100.0) == (True, 0)
    assert limiter.allow("client-a", now=101.0) == (True, 0)
    allowed, retry_after = limiter.allow("client-a", now=102.0)

    assert allowed is False
    assert retry_after >= 1


def test_rate_limiter_expires_old_events():
    limiter = SlidingWindowRateLimiter(limit=1, window_seconds=10, max_clients=4)

    assert limiter.allow("client-a", now=100.0) == (True, 0)
    assert limiter.allow("client-a", now=109.0)[0] is False
    assert limiter.allow("client-a", now=110.1) == (True, 0)


@pytest.mark.parametrize(
    "value",
    ["", None],
)
def test_rate_limiter_requires_client_key(value):
    limiter = SlidingWindowRateLimiter(limit=1)
    with pytest.raises(ValueError):
        limiter.allow(value)  # type: ignore[arg-type]


def test_rate_limiter_can_be_disabled():
    limiter = SlidingWindowRateLimiter(limit=0)
    assert limiter.allow("client-a") == (True, 0)


def test_rate_limiter_bounds_client_state():
    limiter = SlidingWindowRateLimiter(limit=1, window_seconds=60, max_clients=2)
    assert limiter.allow("client-a", now=1.0)[0] is True
    assert limiter.allow("client-b", now=1.0)[0] is True
    assert limiter.allow("client-c", now=1.0)[0] is True
    # A new client cannot cause unbounded retention of client identities.
    assert len(limiter._events) <= 2  # noqa: SLF001


def test_security_contract_documents_modern_browser_isolation():
    from pathlib import Path

    source = Path("gateway/app.py").read_text(encoding="utf-8")
    for header in (
        "Cross-Origin-Opener-Policy",
        "Cross-Origin-Resource-Policy",
        "Origin-Agent-Cluster",
        "Strict-Transport-Security",
    ):
        assert header in source
