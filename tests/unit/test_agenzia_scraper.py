"""Unit tests for Agenzia Entrate scraper."""

import json
import pytest
from pathlib import Path
from unittest.mock import AsyncMock, patch, MagicMock
from datetime import datetime

from src.services.scrapers.agenzia_entrate import (
    AgenziaScraper,
    TaxDocument,
    RateLimiter,
)


class TestTaxDocument:
    """Test TaxDocument dataclass."""
    
    def test_tax_document_creation(self):
        """Test creating a TaxDocument."""
        doc = TaxDocument(
            title="Test Title",
            number="2024/1",
            publication_date="2024-01-01",
            url="https://example.com",
            doc_type="interpello",
            summary="Test summary",
        )
        
        assert doc.title == "Test Title"
        assert doc.number == "2024/1"
        assert doc.publication_date == "2024-01-01"
        assert doc.url == "https://example.com"
        assert doc.doc_type == "interpello"
        assert doc.summary == "Test summary"
        assert doc.fetched_at  # Should have auto-generated timestamp
    
    def test_tax_document_auto_timestamp(self):
        """Test that fetched_at is auto-generated."""
        doc = TaxDocument(
            title="Test",
            number="1",
            publication_date="2024-01-01",
            url="https://example.com",
            doc_type="interpello",
        )
        
        assert doc.fetched_at
        # Check it's a valid ISO format datetime
        datetime.fromisoformat(doc.fetched_at)


class TestRateLimiter:
    """Test RateLimiter class."""
    
    @pytest.mark.asyncio
    async def test_rate_limiter_no_wait_on_first_call(self):
        """Test that first call doesn't wait."""
        limiter = RateLimiter(requests_per_second=1.0)
        
        import time
        start = time.time()
        await limiter.wait()
        elapsed = time.time() - start
        
        # Should be nearly instant
        assert elapsed < 0.1
    
    @pytest.mark.asyncio
    async def test_rate_limiter_enforces_limit(self):
        """Test that rate limiter enforces request limit."""
        limiter = RateLimiter(requests_per_second=1.0)
        
        import time
        start = time.time()
        
        await limiter.wait()
        await limiter.wait()
        
        elapsed = time.time() - start
        
        # Should have waited approximately 1 second
        assert 0.9 < elapsed < 1.2


class TestAgenziaScraper:
    """Test AgenziaScraper class."""
    
    def test_scraper_initialization(self, tmp_path):
        """Test scraper initialization."""
        scraper = AgenziaScraper(output_dir=tmp_path)
        
        assert scraper.output_dir == tmp_path
        assert scraper.max_retries == 3
        assert scraper.timeout == 30.0
        assert tmp_path.exists()
    
    def test_scraper_creates_output_directory(self, tmp_path):
        """Test that scraper creates output directory."""
        output_dir = tmp_path / "test_output"
        assert not output_dir.exists()
        
        scraper = AgenziaScraper(output_dir=output_dir)
        
        assert output_dir.exists()
    
    def test_save_document(self, tmp_path):
        """Test saving a document as JSON."""
        scraper = AgenziaScraper(output_dir=tmp_path)
        
        doc = TaxDocument(
            title="Test",
            number="2024/1",
            publication_date="2024-01-01",
            url="https://example.com",
            doc_type="interpello",
        )
        
        result = scraper._save_document(doc)
        
        assert result is True
        
        # Check file was created
        expected_file = tmp_path / "interpello" / "2024_1.json"
        assert expected_file.exists()
        
        # Check file content
        with open(expected_file) as f:
            saved_data = json.load(f)
        
        assert saved_data["title"] == "Test"
        assert saved_data["number"] == "2024/1"
        assert saved_data["doc_type"] == "interpello"
    
    def test_save_document_creates_subdirectories(self, tmp_path):
        """Test that save_document creates subdirectories by type."""
        scraper = AgenziaScraper(output_dir=tmp_path)
        
        doc_interpello = TaxDocument(
            title="Test 1",
            number="2024/1",
            publication_date="2024-01-01",
            url="https://example.com/1",
            doc_type="interpello",
        )
        
        doc_circolare = TaxDocument(
            title="Test 2",
            number="2024/2",
            publication_date="2024-01-01",
            url="https://example.com/2",
            doc_type="circolare",
        )
        
        scraper._save_document(doc_interpello)
        scraper._save_document(doc_circolare)
        
        assert (tmp_path / "interpello").exists()
        assert (tmp_path / "circolare").exists()
    
    @pytest.mark.asyncio
    async def test_fetch_with_retry_success(self):
        """Test successful fetch with retry."""
        scraper = AgenziaScraper()
        
        mock_response = "<html>Test</html>"
        
        with patch("httpx.AsyncClient") as mock_client_class:
            mock_client = AsyncMock()
            mock_response_obj = AsyncMock()
            mock_response_obj.text = mock_response
            mock_client.__aenter__.return_value = mock_client
            mock_client.get.return_value = mock_response_obj
            mock_client_class.return_value = mock_client
            
            result = await scraper._fetch_with_retry("https://example.com")
            
            assert result == mock_response
    
    @pytest.mark.asyncio
    async def test_fetch_with_retry_failure(self):
        """Test fetch with retry after failures."""
        scraper = AgenziaScraper(max_retries=2)
        
        with patch("httpx.AsyncClient") as mock_client_class:
            mock_client = AsyncMock()
            mock_client.__aenter__.return_value = mock_client
            mock_client.get.side_effect = Exception("Connection error")
            mock_client_class.return_value = mock_client
            
            result = await scraper._fetch_with_retry("https://example.com")
            
            assert result is None
            # Should have retried
            assert mock_client.get.call_count == 2
    
    @pytest.mark.asyncio
    async def test_parse_interpelli(self):
        """Test parsing interpelli from HTML."""
        scraper = AgenziaScraper()
        
        html = """
        <html>
            <div class="interpello-item">
                <h3 class="title">Interpello 1</h3>
                <span class="number">2024/1</span>
                <span class="date">2024-01-01</span>
                <a href="/page1">Link</a>
                <p class="summary">Summary 1</p>
            </div>
            <div class="interpello-item">
                <h3 class="title">Interpello 2</h3>
                <span class="number">2024/2</span>
                <span class="date">2024-01-02</span>
                <a href="/page2">Link</a>
            </div>
        </html>
        """
        
        docs = await scraper._parse_interpelli(html)
        
        assert len(docs) == 2
        assert docs[0].title == "Interpello 1"
        assert docs[0].number == "2024/1"
        assert docs[0].doc_type == "interpello"
        assert docs[0].summary == "Summary 1"
        assert docs[1].title == "Interpello 2"
        assert docs[1].number == "2024/2"
    
    @pytest.mark.asyncio
    async def test_parse_circolari(self):
        """Test parsing circolari from HTML."""
        scraper = AgenziaScraper()
        
        html = """
        <html>
            <div class="circolare-item">
                <h3 class="title">Circolare 1</h3>
                <span class="number">2024/C1</span>
                <span class="date">2024-01-01</span>
                <a href="/circ1">Link</a>
            </div>
        </html>
        """
        
        docs = await scraper._parse_circolari(html)
        
        assert len(docs) == 1
        assert docs[0].title == "Circolare 1"
        assert docs[0].number == "2024/C1"
        assert docs[0].doc_type == "circolare"
    
    @pytest.mark.asyncio
    async def test_parse_risoluzioni(self):
        """Test parsing risoluzioni from HTML."""
        scraper = AgenziaScraper()
        
        html = """
        <html>
            <div class="risoluzione-item">
                <h3 class="title">Risoluzione 1</h3>
                <span class="number">2024/R1</span>
                <span class="date">2024-01-01</span>
                <a href="/ris1">Link</a>
            </div>
        </html>
        """
        
        docs = await scraper._parse_risoluzioni(html)
        
        assert len(docs) == 1
        assert docs[0].title == "Risoluzione 1"
        assert docs[0].number == "2024/R1"
        assert docs[0].doc_type == "risoluzione"
    
    @pytest.mark.asyncio
    async def test_scrape_integration(self, tmp_path):
        """Test full scrape integration with mocked responses."""
        scraper = AgenziaScraper(output_dir=tmp_path)
        
        interpelli_html = """
        <html>
            <div class="interpello-item">
                <h3 class="title">Interpello 1</h3>
                <span class="number">2024/1</span>
                <a href="/page1">Link</a>
            </div>
        </html>
        """
        
        circolari_html = """
        <html>
            <div class="circolare-item">
                <h3 class="title">Circolare 1</h3>
                <span class="number">2024/C1</span>
                <a href="/circ1">Link</a>
            </div>
        </html>
        """
        
        risoluzioni_html = """
        <html>
            <div class="risoluzione-item">
                <h3 class="title">Risoluzione 1</h3>
                <span class="number">2024/R1</span>
                <a href="/ris1">Link</a>
            </div>
        </html>
        """
        
        with patch.object(
            scraper, "_fetch_with_retry", new_callable=AsyncMock
        ) as mock_fetch:
            mock_fetch.side_effect = [interpelli_html, circolari_html, risoluzioni_html]
            
            results = await scraper.scrape()
        
        assert results["interpelli"] == 1
        assert results["circolari"] == 1
        assert results["risoluzioni"] == 1
        assert results["errors"] == 0
        
        # Check files were created
        assert (tmp_path / "interpello").exists()
        assert (tmp_path / "circolare").exists()
        assert (tmp_path / "risoluzione").exists()
