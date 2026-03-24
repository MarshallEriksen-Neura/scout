import unittest
from unittest.mock import AsyncMock, patch

from app.core.compliance import ComplianceManager
from app.services.crawler import CrawlerService


class ComplianceRobotsTests(unittest.IsolatedAsyncioTestCase):
    async def test_is_safe_to_crawl_allows_blacklisted_url(self) -> None:
        manager = ComplianceManager(user_agent="DeetingScout/1.0")
        allowed = await manager.is_safe_to_crawl("https://people.com.cn/internal/login")

        self.assertTrue(allowed)

    async def test_is_safe_to_crawl_ignores_robots_disallow(self) -> None:
        manager = ComplianceManager(user_agent="DeetingScout/1.0")
        allowed = await manager.is_safe_to_crawl("https://example.com/ghost/abc")

        self.assertTrue(allowed)

    def test_is_content_safe_allows_sensitive_keywords(self) -> None:
        manager = ComplianceManager(user_agent="DeetingScout/1.0")
        text = "该页面包含色情内容、赌博推广和内部资料。"

        self.assertTrue(manager.is_content_safe(text))

    async def test_inspect_url_does_not_call_compliance_checks(self) -> None:
        service = CrawlerService()
        crawl_result = {"status": "success", "url": "https://example.com"}

        with patch.object(CrawlerService, "_crawl", AsyncMock(return_value=crawl_result)) as crawl_mock:
            result = await service.inspect_url("https://example.com")

        self.assertEqual(result, crawl_result)
        crawl_mock.assert_awaited_once()
