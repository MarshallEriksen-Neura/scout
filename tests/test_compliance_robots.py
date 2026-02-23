import unittest
from unittest.mock import AsyncMock, patch

from app.core.compliance import ComplianceManager


class ComplianceRobotsTests(unittest.IsolatedAsyncioTestCase):
    async def test_cloudflare_like_robots_does_not_false_block_allowed_path(self) -> None:
        manager = ComplianceManager(user_agent="DeetingScout/1.0")
        robots_txt = """User-agent: *
Allow: /
Disallow: /ghost/
Content-Signal: ai-train=yes, search=yes, ai-input=yes
"""
        with patch.object(manager, "_fetch_robots_txt", AsyncMock(return_value=robots_txt)):
            allowed = await manager.is_safe_to_crawl("https://blog.cloudflare.com/code-mode-mcp/")

        self.assertTrue(allowed)

    async def test_respects_disallow_rule(self) -> None:
        manager = ComplianceManager(user_agent="DeetingScout/1.0")
        robots_txt = """User-agent: *
Disallow: /ghost/
"""
        with patch.object(manager, "_fetch_robots_txt", AsyncMock(return_value=robots_txt)):
            allowed = await manager.is_safe_to_crawl("https://example.com/ghost/abc")

        self.assertFalse(allowed)

    async def test_fetch_failure_falls_back_to_allow_and_uses_cache(self) -> None:
        manager = ComplianceManager(user_agent="DeetingScout/1.0")
        fetch_mock = AsyncMock(return_value=None)

        with patch.object(manager, "_fetch_robots_txt", fetch_mock):
            first = await manager.is_safe_to_crawl("https://example.com/a")
            second = await manager.is_safe_to_crawl("https://example.com/b")

        self.assertTrue(first)
        self.assertTrue(second)
        self.assertEqual(fetch_mock.await_count, 1)
