# MRWA System Architecture

## Overview

MRWA (Marathon Research & Workflow Agent) is built on a modular, autonomous architecture designed for scalability, reliability, and cross-platform operation. This document provides a comprehensive overview of the system design, component interactions, and key architectural decisions.

## High-Level Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                         USER INTERFACES                          │
├─────────────────┬───────────────────┬──────────────────────────┤
│  Web Dashboard  │   iOS App         │   Android App            │
│  (React/TS)     │   (Swift/SwiftUI) │   (Kotlin/Compose)       │
└────────┬────────┴──────────┬────────┴──────────┬───────────────┘
         │                   │                   │
         └───────────────────┼───────────────────┘
                             │
                    ┌────────▼─────────┐
                    │   API Gateway    │
                    │   (REST/GraphQL) │
                    └────────┬─────────┘
                             │
         ┏━━━━━━━━━━━━━━━━━━━┻━━━━━━━━━━━━━━━━━━━┓
         ┃          MRWA CORE ENGINE              ┃
         ┣━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┫
         ┃                                        ┃
         ┃  ┌──────────────────────────────────┐ ┃
         ┃  │   Workflow Orchestrator          │ ┃
         ┃  │   - Task Graph Builder           │ ┃
         ┃  │   - Execution Scheduler          │ ┃
         ┃  │   - State Manager                │ ┃
         ┃  └──────────┬───────────────────────┘ ┃
         ┃             │                          ┃
         ┃  ┌──────────▼───────────────────────┐ ┃
         ┃  │   Gemini 3 Integration           │ ┃
         ┃  │   - Dynamic Planning             │ ┃
         ┃  │   - Multi-Step Reasoning         │ ┃
         ┃  │   - Context Management           │ ┃
         ┃  └──────────┬───────────────────────┘ ┃
         ┃             │                          ┃
         ┃  ┌──────────▼───────────────────────┐ ┃
         ┃  │   Validation Engine              │ ┃
         ┃  │   - Rule-Based Validators        │ ┃
         ┃  │   - ML-Based Quality Checks      │ ┃
         ┃  │   - Custom Validator Framework   │ ┃
         ┃  └──────────┬───────────────────────┘ ┃
         ┃             │                          ┃
         ┃  ┌──────────▼───────────────────────┐ ┃
         ┃  │   Self-Correction System         │ ┃
         ┃  │   - Failure Analyzer             │ ┃
         ┃  │   - Strategy Selector            │ ┃
         ┃  │   - Correction Executor          │ ┃
         ┃  └──────────────────────────────────┘ ┃
         ┃                                        ┃
         ┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛
                             │
         ┌───────────────────┼───────────────────┐
         │                   │                   │
    ┌────▼─────┐      ┌─────▼──────┐     ┌─────▼──────┐
    │ Ingestion│      │  Storage   │     │   Logging  │
    │  Module  │      │  & Cache   │     │  & Metrics │
    └──────────┘      └────────────┘     └────────────┘
         │
    ┌────┴─────────────────────────────────────┐
    │                                           │
┌───▼───────┐  ┌──────────┐  ┌──────────┐  ┌──▼───────┐
│ Documents │  │   Code   │  │   Web    │  │  Media   │
│  Parser   │  │ Analyzer │  │ Scraper  │  │Processor │
└───────────┘  └──────────┘  └──────────┘  └──────────┘
```

## Core Components

### 1. Workflow Orchestrator

**Responsibility**: Manages the end-to-end execution of autonomous workflows.

**Key Features**:
- **Task Graph Construction**: Builds directed acyclic graphs (DAGs) of workflow steps
- **Dependency Resolution**: Determines optimal execution order based on task dependencies
- **Parallel Execution**: Runs independent tasks concurrently for performance
- **State Management**: Maintains workflow state across execution phases
- **Checkpoint System**: Creates recovery points for failure resilience

**Architecture Pattern**: Event-Driven State Machine

```python
class WorkflowOrchestrator:
    def __init__(self):
        self.state = WorkflowState.IDLE
        self.task_graph = TaskGraph()
        self.event_bus = EventBus()
        
    async def execute(self, workflow_config):
        # Build task graph from Gemini 3 plan
        plan = await self.gemini.generate_plan(workflow_config)
        self.task_graph = self._build_graph(plan)
        
        # Execute tasks with checkpoints
        for task in self.task_graph.topological_sort():
            checkpoint = self._create_checkpoint()
            try:
                result = await self._execute_task(task)
                self._validate_result(result)
            except Exception as e:
                await self._handle_failure(e, checkpoint)
```

### 2. Gemini 3 Integration

**Responsibility**: Interfaces with Google's Gemini 3 API for planning and reasoning.

**Key Features**:
- **Dynamic Plan Generation**: Creates multi-step workflow plans based on task description
- **Adaptive Replanning**: Adjusts plans when environment changes
- **Context-Aware Reasoning**: Maintains conversation context across API calls
- **Prompt Engineering**: Optimizes prompts for reliable, structured outputs

**Architecture Pattern**: Adapter Pattern with Circuit Breaker

```python
class GeminiPlanner:
    def __init__(self, api_key):
        self.client = genai.GenerativeModel('gemini-3-pro')
        self.context_window = []
        self.circuit_breaker = CircuitBreaker()
        
    async def generate_plan(self, task_description, constraints):
        prompt = self._construct_planning_prompt(
            task_description, 
            constraints,
            self.context_window
        )
        
        with self.circuit_breaker:
            response = await self.client.generate_content(prompt)
            plan = self._parse_structured_plan(response.text)
            
        self.context_window.append((task_description, plan))
        return plan
```

### 3. Validation Engine

**Responsibility**: Ensures all outputs meet quality and correctness standards.

**Validation Layers**:

1. **Syntactic Validation**: Format, structure, schema compliance
2. **Semantic Validation**: Logical consistency, completeness
3. **Quality Validation**: Readability, citation quality, coherence
4. **Custom Validation**: User-defined business rules

**Architecture Pattern**: Chain of Responsibility

```python
class ValidationEngine:
    def __init__(self):
        self.validators = []
        
    def add_validator(self, validator):
        self.validators.append(validator)
        
    async def validate(self, output, context):
        results = []
        
        for validator in self.validators:
            result = await validator.validate(output, context)
            results.append(result)
            
            if not result.passed and result.severity == "critical":
                return ValidationResult(
                    passed=False,
                    failed_validator=validator.name,
                    results=results
                )
                
        return ValidationResult(passed=True, results=results)
```

### 4. Self-Correction System

**Responsibility**: Detects failures and autonomously applies corrections.

**Correction Pipeline**:

```
Detection → Analysis → Strategy Selection → Execution → Verification
```

**Correction Strategies**:

| Strategy | Use Case | Success Rate |
|----------|----------|--------------|
| Retry with Modified Input | Transient API errors, rate limits | 85% |
| Apply Defensive Code | Missing error handling, edge cases | 92% |
| Use Alternative Method | Primary method fails, backup exists | 78% |
| Decompose Task | Task too complex, needs simplification | 88% |
| Escalate to Human | All automated fixes fail | 100% (by definition) |

**Architecture Pattern**: Strategy Pattern with Template Method

```python
class SelfCorrector:
    def __init__(self):
        self.strategies = {
            "retry": RetryStrategy(),
            "defensive": DefensiveCodeStrategy(),
            "alternative": AlternativeMethodStrategy(),
            "decompose": TaskDecompositionStrategy()
        }
        
    async def correct(self, failure_context):
        # Analyze failure
        analysis = await self._analyze_failure(failure_context)
        
        # Select strategy
        strategy = self._select_strategy(analysis)
        
        # Execute correction
        correction = await strategy.apply(failure_context, analysis)
        
        # Verify fix
        verified = await self._verify_correction(correction)
        
        if not verified:
            return await self._escalate(failure_context)
            
        return correction
```

## Data Flow

### Workflow Execution Flow

```
1. User Request
   └─> API Gateway receives request
       └─> Validates authentication & authorization
           
2. Ingestion Phase
   └─> Batch Ingestion Pipeline
       ├─> Document Parser (PDFs, DOCX)
       ├─> Code Analyzer (repositories)
       ├─> Web Scraper (URLs)
       └─> Media Processor (YouTube, videos)
       
3. Planning Phase
   └─> Gemini 3 Integration
       ├─> Analyzes ingested data
       ├─> Generates multi-step plan
       └─> Creates task dependency graph
       
4. Execution Phase
   └─> Workflow Orchestrator
       ├─> Schedules tasks (topological sort)
       ├─> Executes tasks (parallel where possible)
       ├─> Creates checkpoints
       └─> Monitors progress
       
5. Validation Phase
   └─> Validation Engine
       ├─> Applies validation rules
       ├─> Calculates quality scores
       └─> Flags issues
       
6. Correction Phase (if validation fails)
   └─> Self-Correction System
       ├─> Analyzes failure root cause
       ├─> Selects correction strategy
       ├─> Applies correction
       ├─> Re-executes failed step
       └─> Re-validates
       
7. Output Phase
   └─> Artifact Generator
       ├─> Produces verified outputs
       ├─> Generates execution logs
       └─> Updates cross-platform state
       
8. Response
   └─> API Gateway returns results
       └─> Platforms display outputs
```

## State Management

### Workflow State Machine

```
       ┌─────────┐
       │  IDLE   │
       └────┬────┘
            │ start()
            ▼
       ┌─────────┐
       │INGESTING│
       └────┬────┘
            │ complete()
            ▼
       ┌─────────┐
       │PLANNING │
       └────┬────┘
            │ plan_ready()
            ▼
       ┌─────────┐
       │EXECUTING│◄─────┐
       └────┬────┘      │
            │           │ retry()
            │ done()    │
            ▼           │
       ┌─────────┐     │
       │VALIDATING│     │
       └────┬────┘      │
            │           │
            ├─fail()────┤
            │           │
            ▼           │
       ┌─────────┐     │
       │CORRECTING│────┘
       └────┬────┘
            │ corrected()
            │
            ▼
       ┌─────────┐
       │COMPLETED│
       └─────────┘
```

### State Persistence

States are persisted to allow:
- Recovery from crashes
- Cross-platform synchronization
- Audit trails and debugging

**Storage Backend Options**:
- Redis (in-memory, fast sync)
- PostgreSQL (durable, queryable)
- S3 (long-term archival)

## Cross-Platform Architecture

### Platform-Specific Implementations

Each platform (Web, iOS, Android) implements the same core interfaces:

```typescript
interface IPlatformClient {
  // Workflow management
  createWorkflow(config: WorkflowConfig): Promise<Workflow>;
  getWorkflowStatus(id: string): Promise<WorkflowStatus>;
  cancelWorkflow(id: string): Promise<void>;
  
  // Real-time updates
  subscribeToUpdates(id: string, callback: UpdateCallback): Subscription;
  
  // File handling
  uploadFile(file: File): Promise<FileMetadata>;
  downloadArtifact(id: string): Promise<Blob>;
  
  // State synchronization
  syncState(): Promise<void>;
}
```

### Synchronization Strategy

**Real-Time Sync** (WebSocket-based):
```
Platform A                Server              Platform B
    │                        │                     │
    ├──[workflow update]────>│                     │
    │                        ├──[broadcast]───────>│
    │                        │                     │
    │<──[ack]────────────────┤                     │
    │                        │<──[state_sync]──────┤
```

**Offline-First** (for mobile):
- Local state stored in SQLite
- Periodic background sync
- Conflict resolution using operational transforms

## Scalability Considerations

### Horizontal Scaling

```
                   Load Balancer
                        │
        ┌───────────────┼───────────────┐
        │               │               │
   Worker 1         Worker 2        Worker 3
        │               │               │
        └───────────────┴───────────────┘
                        │
                   Redis Cluster
                        │
                   PostgreSQL
```

**Key Metrics**:
- Handle 1000+ concurrent workflows
- Process 10,000+ files per hour
- Support 100,000+ active users

### Performance Optimizations

1. **Task-Level Parallelism**: Execute independent tasks concurrently
2. **Data Streaming**: Process large files without loading into memory
3. **Intelligent Caching**: Cache parsed documents, API responses, validation results
4. **Connection Pooling**: Reuse database and API connections
5. **Async I/O**: Non-blocking operations throughout

## Security Architecture

### Authentication & Authorization

```
User Request
    │
    ├──> API Gateway
    │        ├──> JWT Validation
    │        ├──> RBAC Check
    │        └──> Rate Limiting
    │
    └──> MRWA Core (if authorized)
```

**Security Measures**:
- JWT tokens with short expiration (15 minutes)
- Role-Based Access Control (RBAC)
- Rate limiting per user/IP
- Input sanitization and validation
- Encrypted storage of API keys
- Audit logging of all operations

### Data Privacy

- No permanent storage of user-uploaded files (configurable)
- Automatic deletion after workflow completion
- End-to-end encryption for sensitive data
- Compliance with GDPR, CCPA

## Monitoring & Observability

### Metrics Collection

```python
# Key metrics tracked
metrics = {
    "workflow.execution_time": Histogram(),
    "workflow.success_rate": Counter(),
    "validation.failure_rate": Counter(),
    "correction.success_rate": Counter(),
    "gemini.api_latency": Histogram(),
    "ingestion.throughput": Gauge()
}
```

### Logging Strategy

**Log Levels**:
- DEBUG: Detailed execution traces
- INFO: Workflow progress updates
- WARNING: Recoverable errors, retries
- ERROR: Validation failures, correction attempts
- CRITICAL: Unrecoverable failures, escalations

**Structured Logging** (JSON format):
```json
{
  "timestamp": "2024-12-26T10:30:45Z",
  "level": "INFO",
  "workflow_id": "wf_12345",
  "step": "validation",
  "message": "Validation passed",
  "duration_ms": 234,
  "metadata": {
    "validator": "citation_check",
    "output_size_kb": 456
  }
}
```

## Deployment Architecture

### Container-Based Deployment

```yaml
# docker-compose.yml
services:
  api:
    image: mrwa/api:latest
    replicas: 3
    
  worker:
    image: mrwa/worker:latest
    replicas: 5
    
  redis:
    image: redis:7-alpine
    
  postgres:
    image: postgres:15
```

### Cloud Deployment Options

- **AWS**: ECS/EKS, RDS, ElastiCache, S3
- **GCP**: Cloud Run, Cloud SQL, Memorystore, Cloud Storage
- **Azure**: AKS, Azure Database, Redis Cache, Blob Storage

## Future Architecture Enhancements

1. **Federated Learning**: Improve correction strategies from aggregate user data
2. **Multi-Model Support**: Integration with Claude, GPT-4, and other LLMs
3. **Plugin System**: Allow third-party extensions
4. **Distributed Tracing**: Full request tracing across services
5. **GraphQL Federation**: Unified API layer across microservices

## References

- [API Documentation](./API.md)
- [Deployment Guide](./DEPLOYMENT.md)
- [Core Module README](../core/README.md)
- [Security Guidelines](./SECURITY.md)