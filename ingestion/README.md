# MRWA Ingestion Module

The Ingestion module handles multi-modal data intake, including documents, code repositories, web content, and video media.

## Components

### Document Parser (`document_parser/`)

**Purpose**: Parse PDFs, Word docs, and text files

**Supported Formats**:
- PDF (.pdf)
- Text (.txt, .md)
- Word (.docx)

**Usage**:
```python
from ingestion.document_parser import DocumentParser

parser = DocumentParser()

# Parse single file
doc = parser.parse_file('samples/research_papers/paper.pdf')

# Parse directory
docs = parser.parse_directory('samples/research_papers/')
```

**Output**:
```python
{
    'filename': 'paper.pdf',
    'type': 'pdf',
    'content': 'Extracted text...',
    'metadata': {
        'size': '2.1 MB',
        'pages': 15
    }
}
```

### Code Analyzer (`code_analyzer/`)

**Purpose**: Analyze code repositories and extract insights

**Supported Languages**:
- Python
- JavaScript/TypeScript
- Java
- C/C++
- And more...

**Usage**:
```python
from ingestion.code_analyzer import CodeAnalyzer

analyzer = CodeAnalyzer()

# Analyze directory
analysis = analyzer.analyze_directory('samples/code_repositories/ml_pipeline/')

# Analyze Git repository
analysis = analyzer.analyze_repository('https://github.com/user/repo')
```

**Output**:
```python
{
    'path': 'ml_pipeline/',
    'languages': {'Python': 75.0, 'JavaScript': 25.0},
    'metrics': {
        'lines_of_code': 1500,
        'complexity': 12.5
    }
}
```

### Web Scraper (`web_scraper/`)

**Purpose**: Extract content from web pages

**Features**:
- HTML parsing
- Content extraction
- Metadata extraction
- Link following

**Usage**:
```python
from ingestion.web_scraper import WebScraper

scraper = WebScraper()

# Scrape single URL
content = scraper.scrape_url('https://example.com/article')

# Scrape from file
contents = scraper.scrape_urls_from_file('samples/links.txt')
```

**Output**:
```python
{
    'url': 'https://example.com/article',
    'title': 'Article Title',
    'content': 'Extracted content...',
    'metadata': {
        'author': 'John Doe',
        'date': '2024-01-01'
    }
}
```

### Media Processor (`media_processor/`)

**Purpose**: Process YouTube videos and extract transcripts

**Features**:
- YouTube video processing
- Transcript extraction
- Metadata extraction

**Usage**:
```python
from ingestion.media_processor import MediaProcessor

processor = MediaProcessor()

# Process YouTube video
video = processor.process_youtube('https://youtube.com/watch?v=...')
```

**Output**:
```python
{
    'url': 'https://youtube.com/watch?v=...',
    'title': 'Video Title',
    'duration': '15:43',
    'transcript': 'Extracted transcript...',
    'metadata': {
        'channel': 'Channel Name',
        'views': 125000
    }
}
```

## Batch Processing

Process multiple sources efficiently:
```python
from ingestion import DocumentParser, WebScraper

parser = DocumentParser()
scraper = WebScraper()

# Ingest all sources
docs = parser.parse_directory('samples/research_papers/')
web = scraper.scrape_urls_from_file('samples/links.txt')

all_inputs = docs + web
```

## Configuration

No configuration needed for basic usage. Advanced options:
```python
parser = DocumentParser(enable_ocr=True)
scraper = WebScraper(respect_robots_txt=True, rate_limit=1.0)
```

## Dependencies

- PyPDF2
- beautifulsoup4
- requests

See `requirements.txt` for versions.

## Testing
```bash
pytest tests/unit/test_ingestion.py
```

## Adding Custom Parsers

Create a new parser in the appropriate subdirectory:
```python
# ingestion/custom_parser/parser.py
class CustomParser:
    def parse(self, source):
        # Your parsing logic
        return parsed_data
```

Then import in `ingestion/__init__.py`.
