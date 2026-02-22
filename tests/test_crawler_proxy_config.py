import unittest
from unittest.mock import patch

from app.core.config import settings
from app.services.crawler import CrawlerService


class FakeAsyncWebCrawler:
    instances = []

    def __init__(self, *args, **kwargs) -> None:
        self.args = args
        self.kwargs = kwargs
        self.ready = False
        FakeAsyncWebCrawler.instances.append(self)

    async def start(self) -> None:
        self.ready = True

    async def close(self) -> None:
        self.ready = False


class CrawlerProxyConfigTests(unittest.IsolatedAsyncioTestCase):
    def setUp(self) -> None:
        self._origin_proxy = settings.SCOUT_BROWSER_PROXY
        FakeAsyncWebCrawler.instances.clear()

    def tearDown(self) -> None:
        settings.SCOUT_BROWSER_PROXY = self._origin_proxy
        FakeAsyncWebCrawler.instances.clear()

    async def test_builds_browser_with_proxy_config(self) -> None:
        settings.SCOUT_BROWSER_PROXY = "http://127.0.0.1:7890"
        service = CrawlerService()

        with patch("app.services.crawler.AsyncWebCrawler", FakeAsyncWebCrawler):
            await service._get_crawler()

        self.assertEqual(len(FakeAsyncWebCrawler.instances), 1)
        browser_config = FakeAsyncWebCrawler.instances[0].kwargs["config"]
        self.assertIsNotNone(browser_config.proxy_config)
        self.assertEqual(browser_config.proxy_config.server, "http://127.0.0.1:7890")
        self.assertEqual(browser_config.user_agent, settings.DEFAULT_USER_AGENT)

    async def test_omits_proxy_config_when_empty(self) -> None:
        settings.SCOUT_BROWSER_PROXY = ""
        service = CrawlerService()

        with patch("app.services.crawler.AsyncWebCrawler", FakeAsyncWebCrawler):
            await service._get_crawler()

        self.assertEqual(len(FakeAsyncWebCrawler.instances), 1)
        browser_config = FakeAsyncWebCrawler.instances[0].kwargs["config"]
        self.assertIsNone(browser_config.proxy_config)
