from __future__ import annotations

from typing import Any


ZERO_WIDTH_TRANSLATION = {
    ord("\u200b"): None,
    ord("\u200c"): None,
    ord("\u200d"): None,
    ord("\ufeff"): None,
}


def normalize_crawled_markdown(markdown: str | None) -> tuple[str, dict[str, Any]]:
    text = str(markdown or "")
    had_bom = text.startswith("\ufeff")
    normalized = text.replace("\r\n", "\n").replace("\r", "\n")
    before = len(normalized)
    normalized = normalized.translate(ZERO_WIDTH_TRANSLATION)
    removed_zero_width_chars = before - len(normalized)
    return normalized, {
        "removed_zero_width_chars": removed_zero_width_chars,
        "removed_bom": had_bom,
        "normalized_newlines": True,
    }
