from __future__ import annotations

from common.settings import VaultSettings


def test_upload_limit_has_safe_default():
    settings = VaultSettings()
    assert settings.max_upload_bytes == 100 * 1024 * 1024


def test_upload_limit_is_explicitly_configurable():
    settings = VaultSettings(max_upload_bytes=8 * 1024 * 1024)
    assert settings.max_upload_bytes == 8 * 1024 * 1024
