# ============================================================================
# FILE: core/orchestrator/__init__.py
# ============================================================================
ORCHESTRATOR_INIT = '''"""Workflow Orchestration Module"""
from .engine import WorkflowEngine, WorkflowStage, TaskStatus, Task, WorkflowResult

__all__ = ['WorkflowEngine', 'WorkflowStage', 'TaskStatus', 'Task', 'WorkflowResult']
'''