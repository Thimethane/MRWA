# ============================================================================
# FILE: ingestion/__init__.py
# ============================================================================
INGESTION_INIT = '''"""Data Ingestion Module"""
from .document_parser.parser import DocumentParser
from .code_analyzer.analyzer import CodeAnalyzer
from .web_scraper.scraper import WebScraper
from .media_processor.processor import MediaProcessor

__all__ = ['DocumentParser', 'CodeAnalyzer', 'WebScraper', 'MediaProcessor']
'''
