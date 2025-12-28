# MRWA Test Suite

Comprehensive testing for MRWA components.

## Structure

## Running Tests
```bash
# All tests
pytest tests/ -v

# Unit tests only
pytest tests/unit/ -v

# Integration tests
pytest tests/integration/ -v

# E2E tests
pytest tests/e2e/ -v

# With coverage
pytest tests/ --cov=core --cov=ingestion --cov-report=html
```

## Writing Tests

### Unit Test Example
```python
import pytest
from core.orchestrator import WorkflowEngine

class TestWorkflowEngine:
    @pytest.fixture
    def engine(self):
        return WorkflowEngine()
    
    @pytest.mark.asyncio
    async def test_execute_workflow(self, engine):
        config = {'name': 'Test', 'inputs': []}
        result = await engine.execute_workflow(config)
        assert result.stage.value == 'completed'
```

### Integration Test Example
```python
import pytest
from core.orchestrator import WorkflowEngine
from ingestion import DocumentParser

@pytest.mark.asyncio
async def test_full_pipeline():
    parser = DocumentParser()
    docs = parser.parse_directory('samples/research_papers/')
    
    engine = WorkflowEngine()
    result = await engine.execute_workflow({
        'name': 'Test',
        'inputs': docs
    })
    
    assert len(result.artifacts) > 0
```

## Configuration

See `pytest.ini` for test configuration.

## Dependencies
```bash
pip install pytest pytest-asyncio pytest-cov
```

## Coverage Report

After running with `--cov`, open `htmlcov/index.html` to view coverage.

## CI/CD Integration
```yaml
# .github/workflows/test.yml
name: Tests
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Set up Python
        uses: actions/setup-python@v2
      - name: Install dependencies
        run: pip install -r requirements.txt
      - name: Run tests
        run: pytest tests/ --cov=core --cov=ingestion
```