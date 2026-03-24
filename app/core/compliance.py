class ComplianceManager:
    """
    Scout compatibility shim.

    Compliance interception is intentionally disabled for now so crawl requests
    can pass through end-to-end while the feature set is being rebuilt.
    """

    def __init__(self, user_agent: str = "*"):
        self.user_agent = user_agent

    async def is_safe_to_crawl(self, url: str) -> bool:
        return True

    def is_content_safe(self, text: str) -> bool:
        return True


compliance_manager = ComplianceManager(user_agent="DeetingScout/1.0")
