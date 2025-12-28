"""
core/orchestrator/engine.py
Main Workflow Execution Engine

This module orchestrates the complete autonomous workflow execution,
including planning, task execution, validation, and self-correction.
"""

import asyncio
import logging
from typing import List, Dict, Any, Optional
from datetime import datetime
from enum import Enum
from dataclasses import dataclass, field, asdict

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class WorkflowStage(Enum):
    """Workflow execution stages"""
    IDLE = "idle"
    INGESTING = "ingesting"
    PLANNING = "planning"
    EXECUTING = "executing"
    VALIDATING = "validating"
    CORRECTING = "correcting"
    COMPLETED = "completed"
    FAILED = "failed"


class TaskStatus(Enum):
    """Individual task status"""
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    CORRECTED = "corrected"


@dataclass
class LogEntry:
    """Execution log entry"""
    timestamp: str
    level: str  # info, success, warning, error
    message: str
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class Task:
    """Individual workflow task"""
    id: str
    step_number: int
    description: str
    status: TaskStatus
    started_at: Optional[str] = None
    completed_at: Optional[str] = None
    error: Optional[str] = None
    correction_applied: bool = False
    
    def to_dict(self) -> Dict[str, Any]:
        d = asdict(self)
        d['status'] = self.status.value
        return d


@dataclass
class ValidationResult:
    """Validation result for task output"""
    passed: bool
    issues: List[str]
    severity: str  # none, low, medium, high, critical
    task_id: str
    
    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class CorrectionStrategy:
    """Self-correction strategy"""
    action: str
    strategy: str
    confidence: float
    task_id: str
    
    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class Artifact:
    """Generated output artifact"""
    name: str
    type: str  # document, data, log, code
    size: str
    verified: bool
    path: Optional[str] = None
    content_preview: Optional[str] = None
    
    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class WorkflowResult:
    """Complete workflow execution result"""
    workflow_id: str
    name: str
    stage: WorkflowStage
    progress: float
    tasks: List[Task]
    logs: List[LogEntry]
    artifacts: List[Artifact]
    validation_failure: Optional[ValidationResult] = None
    correction: Optional[CorrectionStrategy] = None
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())
    completed_at: Optional[str] = None
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            'workflow_id': self.workflow_id,
            'name': self.name,
            'stage': self.stage.value,
            'progress': self.progress,
            'tasks': [t.to_dict() for t in self.tasks],
            'logs': [l.to_dict() for l in self.logs],
            'artifacts': [a.to_dict() for a in self.artifacts],
            'validation_failure': self.validation_failure.to_dict() if self.validation_failure else None,
            'correction': self.correction.to_dict() if self.correction else None,
            'created_at': self.created_at,
            'completed_at': self.completed_at
        }


class WorkflowEngine:
    """
    Main Workflow Execution Engine
    
    Orchestrates autonomous multi-step workflows with:
    - Dynamic planning with Gemini 3
    - Parallel task execution
    - Automatic validation
    - Intelligent self-correction
    - Artifact generation
    """
    
    def __init__(self, gemini_api_key: Optional[str] = None, config: Optional[Dict] = None):
        """
        Initialize workflow engine
        
        Args:
            gemini_api_key: API key for Gemini 3 (optional for demo)
            config: Configuration dictionary
        """
        self.gemini_api_key = gemini_api_key
        self.config = config or {}
        self.current_workflow: Optional[WorkflowResult] = None
        
        # Import other core modules
        try:
            from ..validation.validator import Validator
            from ..correction.corrector import Corrector
            from ..gemini_integration.client import GeminiClient
            
            self.validator = Validator()
            self.corrector = Corrector()
            self.gemini_client = GeminiClient(gemini_api_key) if gemini_api_key else None
        except ImportError:
            logger.warning("Some core modules not available, using fallbacks")
            self.validator = None
            self.corrector = None
            self.gemini_client = None
        
        logger.info("WorkflowEngine initialized")
    
    def add_log(self, level: str, message: str, metadata: Optional[Dict] = None):
        """Add log entry to current workflow"""
        if self.current_workflow:
            entry = LogEntry(
                timestamp=datetime.now().strftime("%H:%M:%S.%f")[:-3],
                level=level,
                message=message,
                metadata=metadata or {}
            )
            self.current_workflow.logs.append(entry)
            
            # Also log to standard logger
            log_func = getattr(logger, level if level in ['info', 'warning', 'error'] else 'info')
            log_func(f"[{self.current_workflow.workflow_id}] {message}")
    
    async def generate_plan(self, config: Dict[str, Any]) -> List[Task]:
        """
        Generate workflow plan using Gemini 3
        
        Args:
            config: Workflow configuration with inputs and requirements
            
        Returns:
            List of tasks to execute
        """
        self.add_log("info", "Gemini 3 analyzing task requirements...")
        await asyncio.sleep(1.5)  # Simulate API call
        
        # In production, this calls Gemini API:
        # if self.gemini_client:
        #     plan = await self.gemini_client.generate_plan(config)
        
        # For demo, generate intelligent plan based on inputs
        inputs = config.get('inputs', [])
        task_type = config.get('name', 'workflow')
        
        # Different plans for different task types
        if 'research' in task_type.lower() or 'synthesis' in task_type.lower():
            plan_steps = [
                "Parse and extract content from all input sources",
                "Identify key themes and patterns using NLP analysis",
                "Cross-reference findings across all sources",
                "Generate comprehensive synthesis report with citations",
                "Validate output completeness and citation accuracy"
            ]
        elif 'code' in task_type.lower() or 'analysis' in task_type.lower():
            plan_steps = [
                "Analyze code structure and dependencies",
                "Detect code smells and anti-patterns",
                "Evaluate security vulnerabilities",
                "Generate improvement recommendations",
                "Validate analysis completeness"
            ]
        else:
            plan_steps = [
                "Process and normalize input data",
                "Apply analysis algorithms",
                "Generate insights and findings",
                "Create output artifacts",
                "Validate results quality"
            ]
        
        tasks = []
        for i, description in enumerate(plan_steps, 1):
            task = Task(
                id=f"task_{i}",
                step_number=i,
                description=description,
                status=TaskStatus.PENDING
            )
            tasks.append(task)
        
        self.add_log("success", f"Generated {len(tasks)}-step workflow plan", {
            'task_count': len(tasks),
            'input_count': len(inputs)
        })
        
        return tasks
    
    async def execute_task(self, task: Task, inputs: List[Any]) -> Dict[str, Any]:
        """
        Execute a single task
        
        Args:
            task: Task to execute
            inputs: Input data for the task
            
        Returns:
            Task execution result
        """
        task.status = TaskStatus.RUNNING
        task.started_at = datetime.now().isoformat()
        
        self.add_log("info", f"Executing step {task.step_number}: {task.description}")
        
        # Simulate task execution with processing time
        await asyncio.sleep(1.5)
        
        # Simulate success/failure based on step number
        # Step 3 intentionally fails for demo purposes
        if task.step_number == 3:
            task.status = TaskStatus.FAILED
            task.error = "Edge case not handled"
            return {'success': False, 'error': task.error}
        
        task.status = TaskStatus.COMPLETED
        task.completed_at = datetime.now().isoformat()
        
        # Generate mock output
        output = {
            'task_id': task.id,
            'result': f"Completed: {task.description}",
            'data': {'processed': True}
        }
        
        return output
    
    async def validate_output(self, task: Task, output: Dict[str, Any]) -> ValidationResult:
        """
        Validate task output
        
        Args:
            task: Task that was executed
            output: Output from task execution
            
        Returns:
            Validation result
        """
        self.add_log("info", f"Validating step {task.step_number} output...")
        await asyncio.sleep(0.8)
        
        # Use validator if available
        if self.validator:
            result = await self.validator.validate(task, output)
            return result
        
        # Fallback validation logic
        # Step 3 fails validation for demo
        if task.step_number == 3:
            result = ValidationResult(
                passed=False,
                issues=["Missing error handling for edge case: empty citation list"],
                severity="medium",
                task_id=task.id
            )
            self.add_log("error", f"Validation FAILED: {result.issues[0]}")
            return result
        
        result = ValidationResult(
            passed=True,
            issues=[],
            severity="none",
            task_id=task.id
        )
        self.add_log("success", f"Step {task.step_number} validation passed")
        return result
    
    async def apply_correction(self, task: Task, validation: ValidationResult) -> CorrectionStrategy:
        """
        Apply autonomous self-correction
        
        Args:
            task: Failed task
            validation: Validation result with issues
            
        Returns:
            Applied correction strategy
        """
        self.add_log("warning", "Initiating autonomous self-correction...")
        await asyncio.sleep(1.2)
        
        # Use corrector if available
        if self.corrector:
            correction = await self.corrector.correct(task, validation)
            return correction
        
        # Fallback correction logic
        correction = CorrectionStrategy(
            action="Add null-check and default handling for citation lists",
            strategy="inject_defensive_code",
            confidence=0.95,
            task_id=task.id
        )
        
        self.add_log("warning", f"Correction strategy: {correction.action}", {
            'strategy': correction.strategy,
            'confidence': correction.confidence
        })
        
        # Re-execute with correction
        self.add_log("info", "Re-executing with correction...")
        await asyncio.sleep(1.5)
        
        task.status = TaskStatus.CORRECTED
        task.correction_applied = True
        task.completed_at = datetime.now().isoformat()
        
        self.add_log("success", "Validation PASSED after correction")
        
        return correction
    
    def generate_artifacts(self) -> List[Artifact]:
        """
        Generate final verified artifacts
        
        Returns:
            List of generated artifacts
        """
        self.add_log("info", "Generating verified artifacts...")
        
        artifacts = [
            Artifact(
                name="research_synthesis_report.pdf",
                type="document",
                size="2.4 MB",
                verified=True,
                content_preview="# Research Synthesis Report\n\nComplete analysis with citations..."
            ),
            Artifact(
                name="key_findings.json",
                type="data",
                size="156 KB",
                verified=True,
                content_preview='{"themes": ["AI", "ML"], "insights": [...]}'
            ),
            Artifact(
                name="execution_log.txt",
                type="log",
                size="45 KB",
                verified=True,
                content_preview="[00:00:00] Workflow started\n[00:00:01] Planning phase..."
            )
        ]
        
        for artifact in artifacts:
            self.add_log("success", f"Generated artifact: {artifact.name}", {
                'type': artifact.type,
                'size': artifact.size
            })
        
        return artifacts
    
    async def execute_workflow(self, config: Dict[str, Any]) -> WorkflowResult:
        """
        Execute complete autonomous workflow
        
        This is the main entry point for workflow execution.
        
        Args:
            config: Workflow configuration with name, inputs, etc.
            
        Returns:
            Complete workflow result with logs and artifacts
        """
        workflow_id = f"wf_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        # Initialize workflow result
        self.current_workflow = WorkflowResult(
            workflow_id=workflow_id,
            name=config.get('name', 'Unnamed Workflow'),
            stage=WorkflowStage.IDLE,
            progress=0.0,
            tasks=[],
            logs=[],
            artifacts=[]
        )
        
        try:
            # Stage 1: Data Ingestion
            self.current_workflow.stage = WorkflowStage.INGESTING
            self.add_log("info", f"Starting workflow: {config['name']}")
            
            inputs = config.get('inputs', [])
            self.add_log("info", f"Ingesting {len(inputs)} input sources...")
            await asyncio.sleep(1.2)
            
            for inp in inputs:
                input_type = inp.get('type', 'unknown')
                input_name = inp.get('name', 'unknown')
                self.add_log("success", f"Ingested {input_type}: {input_name}")
            
            self.current_workflow.progress = 0.2
            
            # Stage 2: Planning with Gemini 3
            self.current_workflow.stage = WorkflowStage.PLANNING
            tasks = await self.generate_plan(config)
            self.current_workflow.tasks = tasks
            self.current_workflow.progress = 0.3
            
            # Stage 3: Task Execution
            self.current_workflow.stage = WorkflowStage.EXECUTING
            
            for i, task in enumerate(tasks):
                # Execute task
                output = await self.execute_task(task, inputs)
                
                # Stage 4: Validation
                self.current_workflow.stage = WorkflowStage.VALIDATING
                validation = await self.validate_output(task, output)
                
                if not validation.passed:
                    # Stage 5: Self-Correction
                    self.current_workflow.stage = WorkflowStage.CORRECTING
                    self.current_workflow.validation_failure = validation
                    
                    correction = await self.apply_correction(task, validation)
                    self.current_workflow.correction = correction
                    self.current_workflow.validation_failure = None
                
                # Update progress
                self.current_workflow.stage = WorkflowStage.EXECUTING
                self.current_workflow.progress = 0.3 + (0.6 * (i + 1) / len(tasks))
            
            # Stage 6: Generate Artifacts
            self.current_workflow.stage = WorkflowStage.COMPLETED
            self.current_workflow.progress = 0.9
            
            await asyncio.sleep(0.8)
            artifacts = self.generate_artifacts()
            self.current_workflow.artifacts = artifacts
            self.current_workflow.progress = 1.0
            self.current_workflow.completed_at = datetime.now().isoformat()
            
            self.add_log("success", "Workflow completed successfully", {
                'total_tasks': len(tasks),
                'artifacts': len(artifacts)
            })
            
        except Exception as e:
            self.current_workflow.stage = WorkflowStage.FAILED
            self.add_log("error", f"Workflow failed: {str(e)}")
            logger.exception("Workflow execution failed")
            raise
        
        return self.current_workflow


# Standalone test function
async def test_engine():
    """Test the workflow engine"""
    print("\n" + "="*60)
    print("MRWA Workflow Engine Test")
    print("="*60 + "\n")
    
    engine = WorkflowEngine()
    
    config = {
        'name': 'Research Paper Synthesis',
        'inputs': [
            {'type': 'pdf', 'name': 'attention_is_all_you_need.pdf'},
            {'type': 'pdf', 'name': 'gpt4_technical_report.pdf'},
            {'type': 'url', 'name': 'https://arxiv.org/abs/2303.08774'}
        ]
    }
    
    result = await engine.execute_workflow(config)
    
    print("\n" + "="*60)
    print("Workflow Execution Complete")
    print("="*60)
    print(f"Status: {result.stage.value}")
    print(f"Progress: {result.progress * 100}%")
    print(f"Tasks: {len(result.tasks)} (all completed)")
    print(f"Logs: {len(result.logs)} entries")
    print(f"Artifacts: {len(result.artifacts)} verified outputs")
    print(f"Self-Correction: {'Applied' if result.correction else 'Not needed'}")
    print("="*60 + "\n")
    
    return result


if __name__ == "__main__":
    asyncio.run(test_engine())