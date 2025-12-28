# ============================================================================
# FILE: core/__init__.py
# ============================================================================
CORE_INIT = '''"""MRWA Core Module"""
from .orchestrator.engine import WorkflowEngine, WorkflowStage, TaskStatus

__version__ = "1.0.0"
__all__ = ['WorkflowEngine', 'WorkflowStage', 'TaskStatus']
'''