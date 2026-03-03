import json
import os
from typing import List, Dict, Any
from urllib.parse import urljoin

from bs4 import BeautifulSoup
from google import genai

from services.website_crawler import WebsiteCrawler
from utils.logging import logger
from utils.settings import settings


class ImpressumExtractor:
    """Extrahiert Impressumsdaten und führt Risikoanalysen durch."""

    def __init__(self, api_key: str, prompt_path: str, schema_path: str):
        self.client = genai.Client(api_key=api_key)
        self.crawler = WebsiteCrawler()
        self.keywords = settings.impressum.keywords

        # Lade externe Dateien
        self.prompt_template = self._load_file(prompt_path)
        self.json_schema = json.loads(self._load_file(schema_path))

    def _load_file(self, path: str) -> str:
        """Hilfsmethode zum Laden von Text/JSON Dateien."""
        if not os.path.exists(path):
            raise FileNotFoundError(f"Datei nicht gefunden: {path}")
        with open(path, 'r', encoding='utf-8') as f:
            return f.read()

    def _find_potential_urls(self, base_url: str, html: str) -> List[str]:
        soup = BeautifulSoup(html, 'html.parser')
        links = {urljoin(base_url, a['href']) for a in soup.find_all('a', href=True)
                 if any(k in a.text.lower() or k in a['href'].lower() for k in self.keywords)}
        return list(links)

    def _analyze_with_llm(self, text: str, additional_context: str = "") -> Dict[str, Any]:
        """Nutzt Gemini mit dem geladenen Prompt und Schema."""
        # Platzhalter im Prompt ersetzen
        full_prompt = self.prompt_template.format(
            schema=json.dumps(self.json_schema, indent=2),
            text=text[:15000],
            context=additional_context
        )

        try:
            response = self.client.models.generate_content(
                model=settings.gemini.model,
                contents=full_prompt
            )
            raw_text = response.text.strip().strip('`').replace('json\n', '', 1)
            return json.loads(raw_text)
        except Exception as e:
            logger.error(f"LLM Fehler: {e}")
            return {"found": False, "error": str(e)}

    def run(self, start_url: str) -> Dict[str, Any]:
        logger.info(f"Analysiere: {start_url}")
        html = self.crawler.fetch_html(start_url)

        if not html:
            return {"found": False}

        urls = self._find_potential_urls(start_url, html)

        for url in dict.fromkeys(urls):
            page_html = self.crawler.fetch_html(url)

            if not page_html:
                continue

            text = self.crawler.clean_html_to_text(page_html)
            data = self._analyze_with_llm(text)

            if data.get("found"):
                data["source_url"] = url
                return data

        return {"found": False, "notes": "Nichts gefunden."}
