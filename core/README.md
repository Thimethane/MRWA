# MRWA Core Module

The Core module is the heart of MRWA, containing the autonomous orchestration engine, validation system, and self-correction mechanisms.

## Components

### Orchestrator (`orchestrator/`)

**Purpose**: Manages end-to-end workflow execution

**Files**:
- `engine.py` - Main workflow execution engine
- `planner.py` - Dynamic workflow planning
- `server.py` - Flask API server

**Usage**:
```python
from core.orchestrator import WorkflowEngine

engine = WorkflowEngine(gemini_api_key="your-key")
result = await engine.execute_workflow({
    'name': 'Research Synthesis',
    'inputs': [...]
})
```

### Validation (`validation/`)

**Purpose**: Validates outputs against quality standards

**Files**:
- `validator.py` - Main validation engine
- `rules.py` - Pre-defined validation rules

**Usage**:
```python
from core.validation import Validator

validator = Validator()
result = await validator.validate(task, output)
```

### Correction (`correction/`)

**Purpose**: Applies autonomous self-correction

**Files**:
- `corrector.py` - Correction engine
- `strategies.py` - Correction strategies

**Usage**:
```python
from core.correction import Corrector

corrector = Corrector()
correction = await corrector.correct(task, validation)
```

### Gemini Integration (`gemini_integration/`)

**Purpose**: Integrates with Gemini 3 API

**Files**:
- `client.py` - Gemini API client

**Usage**:
```python
from core.gemini_integration import GeminiClient

client = GeminiClient(api_key="your-key")
plan = await client.generate_plan(config)
```

## Running the Server
```bash
python -m core.orchestrator.server
```

Server starts on port 8000 by default.

## Testing
```bash
# Test engine directly
python core/orchestrator/engine.py

# Run unit tests
pytest tests/unit/test_orchestrator.py
```

## Dependencies

- flask
- flask-socketio
- python-socketio
- aiohttp

See `requirements.txt` for full list.

## Architecture

The core follows a modular, event-driven architecture:
