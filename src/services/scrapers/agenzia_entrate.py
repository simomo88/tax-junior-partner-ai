"""Agenzia Entrate scraper for Italian tax documents.

This module provides functionality to download and parse tax documents from
Agenzia Entrate including:
- Interpelli (administrative inquiries)
- Circolari (circulars)
- Risoluzioni (resolutions)
"""

import asyncio
import json
import logging
from datetime import datetime, timedelta
from pathlib import Path
from typing import Optional, Dict, List, Any
from dataclasses import dataclass, asdict
from urllib.parse import urljoin

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
    """Simple rate limiter to avoid overwhelming the server."""
    
    def __init__(self, requests_per_second: float = 1.0):
        """Initialize rate limiter.
        
        Args:
            requests_per_second: Maximum requests per second (default: 1.0)
        """
        self.min_interval = 1.0 / requests_per_second
        self.last_request_time = 0.0
    
    async def wait(self) -> None:
        """Wait if necessary to maintain rate limit."""
        current_time = datetime.utcnow().timestamp()
        time_since_last_request = current_time - self.last_request_time
        
        if time_since_last_request < self.min_interval:
            wait_time = self.min_interval - time_since_last_request
            logger.debug(f"Rate limiting: waiting {wait_time:.2f}s")
            await asyncio.sleep(wait_time)
        
        self.last_request_time = datetime.utcnow().timestamp()


class AgenziaScraper:
    """Scraper for Agenzia Entrate tax documents."""
    
    BASE_URL = "https://www.agenziaentrate.gov.it"
    INTERPELLI_URL = urljoin(BASE_URL, "/cittadini/consumatori/patenti/interpelli")
    CIRCOLARI_URL = urljoin(BASE_URL, "/cittadini/consumatori/normativa-e-prassi/circolari")
    RISOLUZIONI_URL = urljoin(BASE_URL, "/cittadini/consumatori/normativa-e-prassi/risoluzioni")
    
    def __init__(
        self,
        output_dir: Path = Path("data/raw/agenzia_entrate"),
        max_retries: int = 3,
        timeout: float = 30.0,
        requests_per_second: float = 1.0,
    ):
        """Initialize Agenzia Entrate scraper.
        
        Args:
            output_dir: Directory to save JSON files
            max_retries: Maximum number of retry attempts
            timeout: HTTP request timeout in seconds
            requests_per_second: Rate limit for requests
        """
        self.output_dir = Path(output_dir)
        self.max_retries = max_retries
        self.timeout = timeout
        self.rate_limiter = RateLimiter(requests_per_second)
        
        # Create output directory
        self.output_dir.mkdir(parents=True, exist_ok=True)
        logger.info(f"Output directory set to: {self.output_dir}")
    
    async def _fetch_with_retry(self, url: str) -> Optional[str]:
        """Fetch URL with retry logic.
        
        Args:
            url: URL to fetch
            
        Returns:
            HTML content or None if all retries failed
        """
        await self.rate_limiter.wait()
        
        for attempt in range(self.max_retries):
            try:
                async with httpx.AsyncClient() as client:
                    response = await client.get(
                        url,
                        timeout=self.timeout,
                        follow_redirects=True,
                        headers={
                            "User-Agent": (
                                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                                "AppleWebKit/537.36 (KHTML, like Gecko) "
                                "Chrome/91.0.4472.124 Safari/537.36"
                            )
                        },
                    )
                    response.raise_for_status()
                    logger.debug(f"Successfully fetched: {url}")
                    return response.text
            except httpx.TimeoutException:
                logger.warning(
                    f"Timeout fetching {url} (attempt {attempt + 1}/{self.max_retries})"
                )
            except httpx.HTTPError as e:
                logger.warning(
                    f"HTTP error fetching {url} (attempt {attempt + 1}/{self.max_retries}): {e}"
                )
            except Exception as e:
                logger.error(
                    f"Unexpected error fetching {url} (attempt {attempt + 1}/{self.max_retries}): {e}"
                )
            
            if attempt < self.max_retries - 1:
                wait_time = 2 ** attempt  # Exponential backoff: 1s, 2s, 4s
                logger.info(f"Retrying in {wait_time}s...")
                await asyncio.sleep(wait_time)
        
        logger.error(f"Failed to fetch {url} after {self.max_retries} attempts")
        return None
    
    def _save_document(self, doc: TaxDocument) -> bool:
        """Save document as JSON file.
        
        Args:
            doc: TaxDocument to save
            
        Returns:
            True if successful, False otherwise
        """
        try:
            # Create subdirectory by document type
            type_dir = self.output_dir / doc.doc_type
            type_dir.mkdir(parents=True, exist_ok=True)
            
            # Create filename from document number
            filename = f"{doc.number.replace('/', '_')}.json"
            filepath = type_dir / filename
            
            # Save as JSON
            with open(filepath, "w", encoding="utf-8") as f:
                json.dump(asdict(doc), f, ensure_ascii=False, indent=2)
            
            logger.debug(f"Saved document: {filepath}")
            return True
        except Exception as e:
            logger.error(f"Error saving document {doc.number}: {e}")
            return False
    
    async def _parse_interpelli(self, html: str) -> List[TaxDocument]:
        """Parse interpelli from HTML.
        
        Args:
            html: HTML content
            
        Returns:
            List of TaxDocument objects
        """
        documents = []
        try:
            soup = BeautifulSoup(html, "html.parser")
            # This is a mock implementation - adjust selectors based on actual HTML structure
            items = soup.find_all("div", class_="interpello-item")  # Adjust selector
            
            for item in items:
                try:
                    title_elem = item.find("h3", class_="title")
                    number_elem = item.find("span", class_="number")
                    date_elem = item.find("span", class_="date")
                    link_elem = item.find("a")
                    summary_elem = item.find("p", class_="summary")
                    
                    if title_elem and number_elem and link_elem:
                        title = title_elem.get_text(strip=True)
                        number = number_elem.get_text(strip=True)
                        pub_date = date_elem.get_text(strip=True) if date_elem else ""
                        url = link_elem.get("href", "")
                        summary = summary_elem.get_text(strip=True) if summary_elem else None
                        
                        if url and not url.startswith("http"):
                            url = urljoin(self.BASE_URL, url)
                        
                        doc = TaxDocument(
                            title=title,
                            number=number,
                            publication_date=pub_date,
                            url=url,
                            doc_type="interpello",
                            summary=summary,
                        )
                        documents.append(doc)
                        logger.debug(f"Parsed interpello: {number}")
                except Exception as e:
                    logger.warning(f"Error parsing interpello item: {e}")
                    continue
        except Exception as e:
            logger.error(f"Error parsing interpelli HTML: {e}")
        
        return documents
    
    async def _parse_circolari(self, html: str) -> List[TaxDocument]:
        """Parse circolari from HTML.
        
        Args:
            html: HTML content
            
        Returns:
            List of TaxDocument objects
        """
        documents = []
        try:
            soup = BeautifulSoup(html, "html.parser")
            # This is a mock implementation - adjust selectors based on actual HTML structure
            items = soup.find_all("div", class_="circolare-item")  # Adjust selector
            
            for item in items:
                try:
                    title_elem = item.find("h3", class_="title")
                    number_elem = item.find("span", class_="number")
                    date_elem = item.find("span", class_="date")
                    link_elem = item.find("a")
                    summary_elem = item.find("p", class_="summary")
                    
                    if title_elem and number_elem and link_elem:
                        title = title_elem.get_text(strip=True)
                        number = number_elem.get_text(strip=True)
                        pub_date = date_elem.get_text(strip=True) if date_elem else ""
                        url = link_elem.get("href", "")
                        summary = summary_elem.get_text(strip=True) if summary_elem else None
                        
                        if url and not url.startswith("http"):
                            url = urljoin(self.BASE_URL, url)
                        
                        doc = TaxDocument(
                            title=title,
                            number=number,
                            publication_date=pub_date,
                            url=url,
                            doc_type="circolare",
                            summary=summary,
                        )
                        documents.append(doc)
                        logger.debug(f"Parsed circolare: {number}")
                except Exception as e:
                    logger.warning(f"Error parsing circolare item: {e}")
                    continue
        except Exception as e:
            logger.error(f"Error parsing circolari HTML: {e}")
        
        return documents
    
    async def _parse_risoluzioni(self, html: str) -> List[TaxDocument]:
        """Parse risoluzioni from HTML.
        
        Args:
            html: HTML content
            
        Returns:
            List of TaxDocument objects
        """
        documents = []
        try:
            soup = BeautifulSoup(html, "html.parser")
            # This is a mock implementation - adjust selectors based on actual HTML structure
            items = soup.find_all("div", class_="risoluzione-item")  # Adjust selector
            
            for item in items:
                try:
                    title_elem = item.find("h3", class_="title")
                    number_elem = item.find("span", class_="number")
                    date_elem = item.find("span", class_="date")
                    link_elem = item.find("a")
                    summary_elem = item.find("p", class_="summary")
                    
                    if title_elem and number_elem and link_elem:
                        title = title_elem.get_text(strip=True)
                        number = number_elem.get_text(strip=True)
                        pub_date = date_elem.get_text(strip=True) if date_elem else ""
                        url = link_elem.get("href", "")
                        summary = summary_elem.get_text(strip=True) if summary_elem else None
                        
                        if url and not url.startswith("http"):
                            url = urljoin(self.BASE_URL, url)
                        
                        doc = TaxDocument(
                            title=title,
                            number=number,
                            publication_date=pub_date,
                            url=url,
                            doc_type="risoluzione",
                            summary=summary,
                        )
                        documents.append(doc)
                        logger.debug(f"Parsed risoluzione: {number}")
                except Exception as e:
                    logger.warning(f"Error parsing risoluzione item: {e}")
                    continue
        except Exception as e:
            logger.error(f"Error parsing risoluzioni HTML: {e}")
        
        return documents
    
    async def scrape(self) -> Dict[str, int]:
        """Scrape all document types from Agenzia Entrate.
        
        Returns:
            Dictionary with counts of downloaded documents by type
        """
        results = {
            "interpelli": 0,
            "circolari": 0,
            "risoluzioni": 0,
            "errors": 0,
        }
        
        logger.info("Starting Agenzia Entrate scraper...")
        
        try:
            # Scrape interpelli
            logger.info("Fetching interpelli...")
            interpelli_html = await self._fetch_with_retry(self.INTERPELLI_URL)
            if interpelli_html:
                interpelli_docs = await self._parse_interpelli(interpelli_html)
                for doc in interpelli_docs:
                    if self._save_document(doc):
                        results["interpelli"] += 1
                logger.info(f"Downloaded {results['interpelli']} interpelli")
            else:
                results["errors"] += 1
            
            # Scrape circolari
            logger.info("Fetching circolari...")
            circolari_html = await self._fetch_with_retry(self.CIRCOLARI_URL)
            if circolari_html:
                circolari_docs = await self._parse_circolari(circolari_html)
                for doc in circolari_docs:
                    if self._save_document(doc):
                        results["circolari"] += 1
                logger.info(f"Downloaded {results['circolari']} circolari")
            else:
                results["errors"] += 1
            
            # Scrape risoluzioni
            logger.info("Fetching risoluzioni...")
            risoluzioni_html = await self._fetch_with_retry(self.RISOLUZIONI_URL)
            if risoluzioni_html:
                risoluzioni_docs = await self._parse_risoluzioni(risoluzioni_html)
                for doc in risoluzioni_docs:
                    if self._save_document(doc):
                        results["risoluzioni"] += 1
                logger.info(f"Downloaded {results['risoluzioni']} risoluzioni")
            else:
                results["errors"] += 1
            
            logger.info(f"Scraping completed. Results: {results}")
            return results
        
        except Exception as e:
            logger.error(f"Fatal error during scraping: {e}", exc_info=True)
            results["errors"] += 1
            return results
