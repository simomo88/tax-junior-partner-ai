#!/usr/bin/env python
"""Tax Junior Partner AI - Main entry point."""

import asyncio
import logging
from pathlib import Path

import click

from config.settings import settings
from src.utils.logger import setup_logging
from src.core.tax_agent import TaxAgent
from src.services.scrapers.agenzia_entrate import AgenziaScraper

# Setup logging
setup_logging(
    settings.get_log_path(),
    settings.app_log_level,
    settings.log_format,
)

logger = logging.getLogger(__name__)


@click.group()
def cli():
    """Tax Junior Partner AI - Your personal tax assistant."""
    logger.info("Tax Junior Partner AI CLI started")
    pass


@cli.command()
@click.option("--query", required=True, help="Search query")
@click.option("--limit", default=5, help="Number of results")
def search(query: str, limit: int):
    """Search the knowledge base.
    
    Examples:
        python main.py search --query "novità PEX 2024"
        python main.py search --query "holding che rifattura costi" --limit 10
    """
    click.echo(f"Searching for: {query}")
    click.echo(f"Limit: {limit}")
    click.echo("\n[MVP] Search functionality to be implemented\n")
    # TODO: Implement search command
    pass


@cli.command()
@click.option("--issue", required=True, help="Tax issue to analyze")
def analyze(issue: str):
    """Analyze a tax issue and generate risk assessment.
    
    Examples:
        python main.py analyze --issue "holding che rifattura costi: è deducibile?"
    """
    click.echo(f"Analyzing: {issue}")
    click.echo("\n[MVP] Analysis functionality to be implemented\n")
    # TODO: Implement analyze command
    pass


@cli.command()
def briefing():
    """Generate daily tax news briefing.
    
    Examples:
        python main.py briefing
    """
    click.echo("Generating daily briefing...\n")
    click.echo("[MVP] Briefing functionality to be implemented\n")
    # TODO: Implement briefing command
    pass


@cli.command()
def status():
    """Check system status and configuration."""
    click.echo("\nTax Junior Partner AI - Status\n")
    click.echo(f"Environment: {settings.app_env}")
    click.echo(f"Debug: {settings.app_debug}")
    click.echo(f"Log Level: {settings.app_log_level}")
    click.echo(f"\nLLM Provider: OpenAI (configured: {bool(settings.openai_api_key)})")
    click.echo(f"Vector DB: {settings.vector_db_type}")
    click.echo(f"Vector DB Path: {settings.vector_db_path}")
    click.echo(f"\nFeatures:")
    click.echo(f"  - News Scraper: {settings.feature_news_scraper}")
    click.echo(f"  - Semantic Search: {settings.feature_semantic_search}")
    click.echo(f"  - Risk Analyzer: {settings.feature_risk_analyzer}")
    click.echo(f"  - Daily Briefing: {settings.feature_daily_briefing}")
    click.echo()


@cli.command()
def init():
    """Initialize the application.
    
    Sets up directories and prepares the system.
    """
    click.echo("Initializing Tax Junior Partner AI...\n")
    
    # Create necessary directories
    settings.get_vector_db_path()
    settings.get_kb_data_path()
    settings.get_log_path()
    
    click.echo("✓ Directories created")
    click.echo("✓ Logging configured")
    click.echo("✓ Configuration loaded")
    click.echo("\nSetup complete! Run 'python main.py status' to verify.\n")


@cli.command()
@click.option(
    "--output-dir",
    default="data/raw/agenzia_entrate",
    help="Output directory for scraped documents",
)
@click.option(
    "--rate-limit",
    default=1.0,
    type=float,
    help="Requests per second rate limit",
)
def scrape(output_dir: str, rate_limit: float):
    """Download the latest documents from Agenzia Entrate.
    
    Downloads interpelli, circolari, and risoluzioni and saves them as JSON files.
    
    Examples:
        python main.py scrape
        python main.py scrape --output-dir ./data --rate-limit 0.5
    """
    click.echo("\n🔄 Starting Agenzia Entrate scraper...\n")
    
    try:
        scraper = AgenziaScraper(
            output_dir=Path(output_dir),
            requests_per_second=rate_limit,
        )
        
        # Run async scraper
        results = asyncio.run(scraper.scrape())
        
        # Display results
        click.echo("\n✅ Scraping completed!\n")
        click.echo("Downloaded:")
        click.echo(f"  • {results['interpelli']} interpelli")
        click.echo(f"  • {results['circolari']} circolari")
        click.echo(f"  • {results['risoluzioni']} risoluzioni")
        
        if results["errors"] > 0:
            click.echo(f"\n⚠️  Errors encountered: {results['errors']}")
        
        click.echo(f"\n📁 Documents saved to: {output_dir}\n")
        
        if results['interpelli'] + results['circolari'] + results['risoluzioni'] == 0:
            click.echo("⚠️  No documents were downloaded. Check logs for details.\n")
            return
        
        click.echo("✨ Done!\n")
    
    except Exception as e:
        logger.error(f"Scraping failed: {e}", exc_info=True)
        click.echo(f"\n❌ Error: {e}\n")
        raise


if __name__ == "__main__":
    try:
        cli()
    except KeyboardInterrupt:
        logger.info("Application interrupted by user")
        click.echo("\nGoodbye!")
    except Exception as e:
        logger.error(f"Fatal error: {e}", exc_info=True)
        click.echo(f"\nError: {e}\n")
        raise
