# ============================================================================
# FILE: core/orchestrator/planner.py
# ============================================================================
PLANNER_CODE = '''"""
core/orchestrator/planner.py
Dynamic Workflow Planning
"""

from typing import Dict, Any, List


class WorkflowPlanner:
    """Plans multi-step workflows based on task requirements"""
    
    def generate_plan(self, task_type: str, inputs: List[Dict]) -> List[str]:
        """
        Generate workflow plan based on task type
        
        Args:
            task_type: Type of workflow (research, code, video, etc.)
            inputs: List of input sources
            
        Returns:
            List of step descriptions
        """
        if 'research' in task_type.lower() or 'synthesis' in task_type.lower():
            return [
                "Parse and extract content from all input sources",
                "Identify key themes and patterns using NLP analysis",
                "Cross-reference findings across all sources",
                "Generate comprehensive synthesis report with citations",
                "Validate output completeness and citation accuracy"
            ]
        elif 'code' in task_type.lower():
            return [
                "Analyze code structure and dependencies",
                "Detect code smells and anti-patterns",
                "Evaluate security vulnerabilities",
                "Generate improvement recommendations",
                "Validate analysis completeness"
            ]
        elif 'video' in task_type.lower() or 'youtube' in task_type.lower():
            return [
                "Extract video transcript and metadata",
                "Identify key concepts and topics",
                "Generate timeline of important moments",
                "Create summary and study guide",
                "Validate output quality"
            ]
        else:
            return [
                "Process and normalize input data",
                "Apply analysis algorithms",
                "Generate insights and findings",
                "Create output artifacts",
                "Validate results quality"
            ]
'''
