import unittest
from unittest.mock import AsyncMock, patch

from app.services.deep_dive import DeepDiveService


def _ok_result(title: str, links: list[str]) -> dict:
    return {
        "status": "success",
        "title": title,
        "markdown": f"# {title}\ncontent",
        "metadata": {},
        "links": {"internal": [{"href": link} for link in links]},
    }


class DeepDiveFilterTests(unittest.IsolatedAsyncioTestCase):
    def test_infer_scope_prefix_prefers_repo_scope_when_dense(self) -> None:
        service = DeepDiveService()
        seed = "https://github.com/f/prompts.chat?tab=readme-ov-file"
        links = [
            "https://github.com/f/prompts.chat/blob/main/README.md",
            "https://github.com/f/prompts.chat/tree/main/src",
            "https://github.com/f/prompts.chat/issues",
            "https://github.com/features/copilot",
            "https://github.com/login?return_to=/f/prompts.chat",
        ]

        prefix = service._infer_scope_prefix(seed, links)
        self.assertEqual(prefix, "/f/prompts.chat")

    def test_infer_scope_prefix_falls_back_to_first_segment(self) -> None:
        service = DeepDiveService()
        seed = "https://example.com/docs/start"
        links = [
            "https://example.com/docs/intro",
            "https://example.com/docs/api",
            "https://example.com/docs/install",
            "https://example.com/pricing",
        ]

        prefix = service._infer_scope_prefix(seed, links)
        self.assertEqual(prefix, "/docs")

    async def test_dive_filters_noise_and_out_of_scope_links(self) -> None:
        service = DeepDiveService()
        seed = "https://github.com/f/prompts.chat?tab=readme-ov-file"
        repo_readme = "https://github.com/f/prompts.chat/blob/main/README.md"
        repo_src = "https://github.com/f/prompts.chat/tree/main/src"
        repo_issues = "https://github.com/f/prompts.chat/issues"

        responses = {
            "https://github.com/f/prompts.chat?tab=readme-ov-file": _ok_result(
                "seed",
                [
                    "/f/prompts.chat/blob/main/README.md",
                    "/f/prompts.chat/tree/main/src",
                    "/f/prompts.chat/issues",
                    "/login?return_to=/f/prompts.chat",
                    "/",
                    "/features/copilot",
                ],
            ),
            repo_readme: _ok_result("readme", []),
            repo_src: _ok_result("src", []),
            repo_issues: _ok_result("issues", []),
        }

        async def _fake_inspect(url: str, js_mode: bool = True):  # noqa: ARG001
            if url in responses:
                return responses[url]
            return {"status": "failed", "error": f"unexpected url: {url}"}

        with patch(
            "app.services.deep_dive.crawler_service.inspect_url",
            AsyncMock(side_effect=_fake_inspect),
        ):
            result = await service.dive(seed, max_depth=1, max_pages=10)

        artifact_urls = [item["url"] for item in result["artifacts"]]
        self.assertIn("https://github.com/f/prompts.chat?tab=readme-ov-file", artifact_urls)
        self.assertIn(repo_readme, artifact_urls)
        self.assertIn(repo_src, artifact_urls)
        self.assertIn(repo_issues, artifact_urls)

        self.assertNotIn("https://github.com/", artifact_urls)
        self.assertTrue(all("/login" not in url for url in artifact_urls))

