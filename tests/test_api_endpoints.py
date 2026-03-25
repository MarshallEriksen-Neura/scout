import unittest
from unittest.mock import AsyncMock, patch

from app.api.endpoints import ScoutRequest, inspect_target


class ScoutInspectEndpointTests(unittest.IsolatedAsyncioTestCase):
    async def test_inspect_target_returns_title_and_normalization_metadata(self) -> None:
        mock_result = {
            "status": "success",
            "title": "Volcengine Docs",
            "markdown": "abcdef",
            "metadata": {
                "title": "Volcengine Docs",
                "normalization": {
                    "removed_zero_width_chars": 1,
                    "removed_bom": False,
                    "normalized_newlines": True,
                },
            },
            "media": [],
            "links": {"internal": ["https://example.com/a", "https://example.com/b"]},
        }

        with patch(
            "app.api.endpoints.crawler_service.inspect_url",
            AsyncMock(return_value=mock_result),
        ):
            response = await inspect_target(
                ScoutRequest(url="https://example.com/docs", js_mode=True)
            )

        self.assertEqual("success", response.status)
        self.assertEqual("Volcengine Docs", response.title)
        self.assertEqual("abcdef", response.markdown)
        self.assertEqual(
            {
                "removed_zero_width_chars": 1,
                "removed_bom": False,
                "normalized_newlines": True,
            },
            response.metadata["normalization"],
        )
        self.assertEqual(2, response.metadata["link_count"])

