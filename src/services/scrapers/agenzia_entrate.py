"""Agenzia Entrate scraper for Italian tax documents.

Improvements:
- Uses a persistent async HTTP session with realistic browser headers.
- Retries with exponential backoff + jitter and special handling for 403 responses.
- Robust parsing: finds PDF/document links and extracts nearby metadata.
- Downloads PDF files and saves JSON metadata.
- Supports a verify mode that only fetches pages and counts detected documents (no downloads).
"""

import asyncio
import json
import logging
import random
import re
from datetime import datetime
from pathlib import Path
from typing import Optional, Dict, List, Any, Tuple
from dataclasses import dataclass, asdict
from urllib.parse import urljoin, urlparse

import httpx
from bs4 import BeautifulSoup

logger = logging.getLogger(__name__)


@dataclass
class TaxDocument:
    """Represents a tax document from Agenzia Entrate."""

    title: str
    number: str
    publication_date: str
    url: str
    doc_type: str  # 'interpello', 'circolare', 'risoluzione'
    summary: Optional[str] = None
    fetched_at: str = ""

    def __post_init__(self):
        if not self.fetched_at:
            self.fetched_at = datetime.utcnow().isoformat()


class RateLimiter:
    """Simple async rate limiter to avoid overwhelming the server."""

    def __init__(self, requests_per_second: float = 1.0):
        self.min_interval = 1.0 / requests_per_second
        self.last_request_time = 0.0

    async def wait(self) -> None:
        current_time = datetime.utcnow().timestamp()
        time_since_last = current_time - self.last_request_time
        if time_since_last < self.min_interval:
            wait_time = self.min_interval - time_since_last
            logger.debug(f"Rate limiting: waiting {wait_time:.2f}s")
            await asyncio.sleep(wait_time)
        self.last_request_time = datetime.utcnow().timestamp()


class AgenziaScraper:
    """Scraper for Agenzia Entrate tax documents."""

    BASE_URL = "https://www.agenziaentrate.gov.it/portale/"
    INTERPELLI_URL = "https://www.agenziaentrate.gov.it/portale/normativa-e-prassi/risposte-agli-interpelli/interpelli"
    CIRCOLARI_URL = "https://www.agenziaentrate.gov.it/portale/normativa-e-prassi/circolari"
    RISOLUZIONI_URL = "https://www.agenziaentrate.gov.it/portale/normativa-e-prassi/risoluzioni"

    DEFAULT_HEADERS = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/120.0.0.0 Safari/537.36"
        ),
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
        "Accept-Language": "it-IT,it;q=0.9,en-US;q=0.8,en;q=0.7",
        "Referer": "https://www.google.com/",
    }

    def __init__(
        self,
        output_dir: Path = Path("data/raw/agenzia_entrate"),
        max_retries: int = 4,
        timeout: float = 30.0,
        requests_per_second: float = 1.0,
    ):
        self.output_dir = Path(output_dir)
        self.max_retries = max_retries
        self.timeout = timeout
        self.rate_limiter = RateLimiter(requests_per_second)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        logger.info(f"Output directory set to: {self.output_dir}")

    async def _fetch_with_retry(
        self, client: httpx.AsyncClient, url: str, as_bytes: bool = False
    ) -> Optional[Any]:
        """Fetch URL using provided client with retry/backoff. Returns text or bytes."""
        await self.rate_limiter.wait()
        backoff_base = 1.0

        for attempt in range(self.max_retries):
            try:
                response = await client.get(url, timeout=self.timeout, follow_redirects=True)
                status = response.status_code

                # If blocked with 403, log details and backoff more aggressively
                if status == 403:
                    logger.warning(f"403 Forbidden for {url} (attempt {attempt + 1}/{self.max_retries})")
                    # give an extra long wait before retry
                    extra = backoff_base * (2 ** attempt) + random.uniform(1.0, 3.0)
                    logger.info(f"403 encountered. Waiting {extra:.1f}s before retry.")
                    await asyncio.sleep(extra)
                    continue

                response.raise_for_status()
                logger.debug(f"Fetched {url} (status {status})")
                return response.content if as_bytes else response.text

            except httpx.TimeoutException:
                logger.warning(f"Timeout fetching {url} (attempt {attempt + 1}/{self.max_retries})")
            except httpx.HTTPStatusError as e:
                logger.warning(f"HTTP error fetching {url} (attempt {attempt + 1}/{self.max_retries}): {e}")
            except httpx.HTTPError as e:
                logger.warning(f"HTTP error fetching {url} (attempt {attempt + 1}/{self.max_retries}): {e}")
            except Exception as e:
                logger.error(f"Unexpected error fetching {url} (attempt {attempt + 1}/{self.max_retries}): {e}")

            # Exponential backoff with jitter
            if attempt < self.max_retries - 1:
                sleep_for = backoff_base * (2 ** attempt) + random.uniform(0, 1.0)
                logger.info(f"Retrying {url} in {sleep_for:.1f}s (attempt {attempt + 2}/{self.max_retries})")
                await asyncio.sleep(sleep_for)

        logger.error(f"Failed to fetch {url} after {self.max_retries} attempts")
        return None

    async def _download_and_save(self, client: httpx.AsyncClient, doc: TaxDocument) -> bool:
        """Download the document (PDF) if possible and save metadata JSON."""
        try:
            type_dir = self.output_dir / doc.doc_type
            type_dir.mkdir(parents=True, exist_ok=True)

            # Make a safe filename from URL or number
            parsed = urlparse(doc.url)
            basename = Path(parsed.path).name
            if not basename:
                basename = f"{doc.number or 'doc'}_{int(datetime.utcnow().timestamp())}.pdf"
            # Ensure extension
            if not basename.lower().endswith(".pdf"):
                basename = f"{basename}.pdf"

            pdf_path = type_dir / basename
            json_path = type_dir / f"{Path(basename).stem}.json"

            # Download if URL points to a PDF or content-type indicates PDF
            content_bytes = None
            # First, attempt to fetch as bytes
            content_bytes = await self._fetch_with_retry(client, doc.url, as_bytes=True)
            if content_bytes:
                # Save PDF file
                with open(pdf_path, "wb") as f:
                    f.write(content_bytes)
                logger.debug(f"Saved PDF: {pdf_path}")
            else:
                logger.warning(f"Could not download file for {doc.url}")

            # Save metadata JSON (include local file path if downloaded)
            meta = asdict(doc)
            if content_bytes:
                meta["_local_file"] = str(pdf_path)

            with open(json_path, "w", encoding="utf-8") as jf:
                json.dump(meta, jf, ensure_ascii=False, indent=2)

            logger.debug(f"Saved metadata JSON: {json_path}")
            return True

        except Exception as e:
            logger.error(f"Error saving document {doc.url}: {e}")
            return False

    def _extract_date_and_number_from_text(self, text: str) -> Tuple[str, str]:
        """Try to find a date or number in a piece of text using regex heuristics."""
        if not text:
            return "", ""
        # Look for common Italian date formats or year
        date_match = re.search(r"\d{1,2}/\d{1,2}/\d{4}|\d{1,2}\s+[A-Za-zàèéìòù]+\.?\s+\d{4}|\d{4}", text)
        num_match = re.search(r"[Rr]isoluzione\s+n\.?\s*\d+|[Cc]ircolare\s+n\.?\s*\d+|n\.?\s*\d+/\d{4}", text)
        date = date_match.group(0).strip() if date_match else ""
        number = num_match.group(0).strip() if num_match else ""
        return date, number

    async def _parse_documents_generic(self, html: str, doc_type: str) -> List[TaxDocument]:
        """Generic parser that finds PDF/document links and extracts nearby metadata."""
        documents: List[TaxDocument] = []
        try:
            soup = BeautifulSoup(html, "html.parser")

            # Strategy:
            # - Find links (<a href=...>) that point to PDFs or to pages that likely contain documents.
            # - For each link, extract title from the link text or nearby header tags.
            # - Attempt to find a date/number in the surrounding text.

            candidates = []
            for a in soup.find_all("a", href=True):
                href = a["href"]
                href_l = href.lower()
                # Heuristics: direct PDF or path that usually contains documents
                if href_l.endswith(".pdf") or "/documenti/" in href_l or "/download/" in href_l or "pdf" in href_l:
                    candidates.append(a)

            # De-duplicate by resolved absolute URL
            seen = set()
            for a in candidates:
                raw_href = a["href"]
                url = raw_href
                if not url.startswith("http"):
                    url = urljoin(self.BASE_URL, url)

                if url in seen:
                    continue
                seen.add(url)

                title = a.get_text(strip=True) or a.get("title") or ""
                # If link text is empty, try nearby headers
                if not title:
                    # Look for parent header tags up to a few levels
                    p = a.parent
                    title_found = ""
                    for ancestor in (p, p.parent if p else None, (p.parent.parent if p and p.parent else None)):
                        if ancestor:
                            header = ancestor.find(re.compile("^h[1-6]$"))
                            if header:
                                title_found = header.get_text(strip=True)
                                break
                    title = title_found or title

                # gather surrounding text
                surrounding = ""
                try:
                    surrounding = " ".join(a.parent.get_text(" ", strip=True).split()) if a.parent else ""
                except Exception:
                    surrounding = ""

                # try to find date/number in surrounding or in higher ancestor
                date = ""
                number = ""
                combined_text = " ".join(filter(None, [a.get_text(" ", strip=True), surrounding]))
                if not combined_text:
                    combined_text = soup.get_text(" ", strip=True)
                date, number = self._extract_date_and_number_from_text(combined_text)

                summary = None
                # look for a short paragraph sibling
                try:
                    sib_p = a.find_next("p")
                    if sib_p:
                        summary = sib_p.get_text(strip=True)
                except Exception:
                    summary = None

                doc = TaxDocument(
                    title=title or Path(urlparse(url).path).name,
                    number=number or "",
                    publication_date=date or "",
                    url=url,
                    doc_type=doc_type,
                    summary=summary,
                )
                documents.append(doc)
                logger.debug(f"Found candidate doc: {doc.title} ({doc.url})")

        except Exception as e:
            logger.error(f"Error parsing {doc_type} HTML: {e}", exc_info=True)

        return documents

    async def scrape(self, verify: bool = False) -> Dict[str, int]:
        """Scrape all document types from Agenzia Entrate.

        If verify=True, only fetch pages and return verification info (url, status_code, title, detected_docs).
        Otherwise download documents and save them.
        """
        results = {"interpelli": 0, "circolari": 0, "risoluzioni": 0, "errors": 0}
        verifications = []
        logger.info("Starting Agenzia Entrate scraper...")

        headers = dict(self.DEFAULT_HEADERS)
        headers["Referer"] = self.BASE_URL

        async with httpx.AsyncClient(headers=headers, timeout=self.timeout, follow_redirects=True) as client:
            try:
                # Helper to fetch and parse for verification
                async def _verify_page(url: str, doc_type: str) -> Tuple[int, str, int]:
                    await self.rate_limiter.wait()
                    try:
                        resp = await client.get(url)
                        status = resp.status_code
                        title = ""
                        detected = 0
                        if resp.status_code == 200:
                            text = resp.text
                            soup = BeautifulSoup(text, "html.parser")
                            title_tag = soup.find("title")
                            title = title_tag.get_text(strip=True) if title_tag else ""
                            docs = await self._parse_documents_generic(text, doc_type)
                            detected = len(docs)
                        return status, title, detected
                    except Exception as e:
                        logger.warning(f"Verification fetch failed for {url}: {e}")
                        return 0, "", 0

                # Interpelli
                logger.info("Fetching interpelli page...")
                if verify:
                    status, title, detected = await _verify_page(self.INTERPELLI_URL, "interpello")
                    verifications.append({"url": self.INTERPELLI_URL, "status_code": status, "title": title, "detected_docs": detected})
                else:
                    interpelli_html = await self._fetch_with_retry(client, self.INTERPELLI_URL)
                    if interpelli_html:
                        interpelli_docs = await self._parse_documents_generic(interpelli_html, "interpello")
                        logger.info(f"Found {len(interpelli_docs)} interpelli candidates")
                        for doc in interpelli_docs:
                            ok = await self._download_and_save(client, doc)
                            if ok:
                                results["interpelli"] += 1
                            else:
                                results["errors"] += 1
                    else:
                        results["errors"] += 1

                # Circolari
                logger.info("Fetching circolari page...")
                if verify:
                    status, title, detected = await _verify_page(self.CIRCOLARI_URL, "circolare")
                    verifications.append({"url": self.CIRCOLARI_URL, "status_code": status, "title": title, "detected_docs": detected})
                else:
                    circolari_html = await self._fetch_with_retry(client, self.CIRCOLARI_URL)
                    if circolari_html:
                        circolari_docs = await self._parse_documents_generic(circolari_html, "circolare")
                        logger.info(f"Found {len(circolari_docs)} circolari candidates")
                        for doc in circolari_docs:
                            ok = await self._download_and_save(client, doc)
                            if ok:
                                results["circolari"] += 1
                            else:
                                results["errors"] += 1
                    else:
                        results["errors"] += 1

                # Risoluzioni
                logger.info("Fetching risoluzioni page...")
                if verify:
                    status, title, detected = await _verify_page(self.RISOLUZIONI_URL, "risoluzione")
                    verifications.append({"url": self.RISOLUZIONI_URL, "status_code": status, "title": title, "detected_docs": detected})
                else:
                    risoluzioni_html = await self._fetch_with_retry(client, self.RISOLUZIONI_URL)
                    if risoluzioni_html:
                        risoluzioni_docs = await self._parse_documents_generic(risoluzioni_html, "risoluzione")
                        logger.info(f"Found {len(risoluzioni_docs)} risoluzioni candidates")
                        for doc in risoluzioni_docs:
                            ok = await self._download_and_save(client, doc)
                            if ok:
                                results["risoluzioni"] += 1
                            else:
                                results["errors"] += 1
                    else:
                        results["errors"] += 1

                if verify:
                    results["verifications"] = verifications
                logger.info(f"Scraping completed. Results: {results}")
                return results

            except Exception as e:
                logger.error(f"Fatal error during scraping: {e}", exc_info=True)
                results["errors"] += 1
                return results
