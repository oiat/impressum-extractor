from typing import Optional

import requests
from bs4 import BeautifulSoup

from utils.logging import logger


class WebsiteCrawler:
    """Zuständig für das Laden und Vorverarbeiten von Webinhalten."""

    def __init__(self, timeout: int = 10):
        self.timeout = timeout
        self.session = requests.Session()
        self.session.headers.update({"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/120.0.0.0"})

    def fetch_html(self, url: str) -> Optional[str]:
        try:
            response = self.session.get(url, timeout=self.timeout)
            response.raise_for_status()
            return response.text
        except Exception as e:
            logger.error(f"Fehler bei {url}: {e}")
            return None

    def clean_html_to_text(self, html: str) -> str:
        soup = BeautifulSoup(html, "html.parser")
        for tag in soup(["script", "style", "noscript"]):
            tag.decompose()
        return soup.get_text(separator="\n", strip=True)