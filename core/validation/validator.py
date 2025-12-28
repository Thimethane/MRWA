"""
core/validation/validator.py
Output Validation Engine

Validates task outputs against predefined rules and quality standards.
"""

import asyncio
from typing import Dict, Any, List, Optional
from dataclasses import dataclass


@dataclass
class ValidationRule:
    """Validation rule definition"""
    name: str
    description: str
    severity: str  # low, medium, high, critical
    check_function: Any


class Validator:
    """
    Output Validation Engine
    
    Validates task outputs using:
    - Pre-defined validation rules
    - Custom business logic
    - Quality scoring
    - Completeness checks
    """
    
    def __init__(self):
        """Initialize validator with default rules"""
        self.rules = self._load_default_rules()
    
    def _load_default_rules(self) -> Dict[str, ValidationRule]:
        """Load default validation rules"""
        return {
            'citation_check': ValidationRule(
                name='citation_check',
                description='Verify all citations are present and properly formatted',
                severity='medium',
                check_function=self._check_citations
            ),
            'completeness_check': ValidationRule(
                name='completeness_check',
                description='Ensure all required sections are present',
                severity='high',
                check_function=self._check_completeness
            ),
            'format_check': ValidationRule(
                name='format_check',
                description='Validate output format matches requirements',
                severity='low',
                check_function=self._check_format
            ),
            'quality_score': ValidationRule(
                name='quality_score',
                description='Calculate overall output quality score',
                severity='medium',
                check_function=self._calculate_quality_score
            )
        }
    
    def _check_citations(self, output: Dict[str, Any]) -> tuple[bool, List[str]]:
        """Check if citations are present and valid"""
        # Demo logic - in production would check actual citations
        citations = output.get('citations', [])
        
        if len(citations) == 0:
            return False, ["Missing citations"]
        
        return True, []
    
    def _check_completeness(self, output: Dict[str, Any]) -> tuple[bool, List[str]]:
        """Check if output is complete"""
        required_fields = ['result', 'data']
        missing = [f for f in required_fields if f not in output]
        
        if missing:
            return False, [f"Missing required field: {f}" for f in missing]
        
        return True, []
    
    def _check_format(self, output: Dict[str, Any]) -> tuple[bool, List[str]]:
        """Check output format"""
        if not isinstance(output, dict):
            return False, ["Output must be a dictionary"]
        
        return True, []
    
    def _calculate_quality_score(self, output: Dict[str, Any]) -> tuple[bool, List[str]]:
        """Calculate quality score"""
        # Demo scoring logic
        score = 0.85  # Mock score
        
        if score < 0.7:
            return False, [f"Quality score too low: {score}"]
        
        return True, []
    
    async def validate(self, task: Any, output: Dict[str, Any]) -> Any:
        """
        Validate task output
        
        Args:
            task: Task that was executed
            output: Output from task execution
            
        Returns:
            ValidationResult object
        """
        # Import here to avoid circular dependency
        from ..orchestrator.engine import ValidationResult
        
        # For demo purposes, step 3 always fails validation
        if task.step_number == 3:
            return ValidationResult(
                passed=False,
                issues=["Missing error handling for edge case: empty citation list"],
                severity="medium",
                task_id=task.id
            )
        
        # Run all validation rules
        all_issues = []
        max_severity = "none"
        
        for rule_name, rule in self.rules.items():
            passed, issues = rule.check_function(output)
            if not passed:
                all_issues.extend(issues)
                if rule.severity == "critical":
                    max_severity = "critical"
                elif rule.severity == "high" and max_severity != "critical":
                    max_severity = "high"
                elif rule.severity == "medium" and max_severity not in ["critical", "high"]:
                    max_severity = "medium"
        
        return ValidationResult(
            passed=len(all_issues) == 0,
            issues=all_issues,
            severity=max_severity,
            task_id=task.id
        )
    
    def add_custom_rule(self, rule: ValidationRule):
        """Add a custom validation rule"""
        self.rules[rule.name] = rule


# Example usage
if __name__ == "__main__":
    validator = Validator()
    print("Validator initialized with rules:")
    for name, rule in validator.rules.items():
        print(f"  - {name}: {rule.description}")