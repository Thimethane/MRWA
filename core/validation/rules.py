# ============================================================================
# FILE: core/validation/rules.py
# ============================================================================
VALIDATION_RULES = '''"""
core/validation/rules.py
Pre-defined Validation Rules
"""

from typing import Dict, Any, Tuple, List


def check_citations(output: Dict[str, Any]) -> Tuple[bool, List[str]]:
    """Validate citations are present"""
    citations = output.get('citations', [])
    if not citations:
        return False, ["No citations found"]
    return True, []


def check_completeness(output: Dict[str, Any]) -> Tuple[bool, List[str]]:
    """Check output completeness"""
    required = ['result', 'data']
    missing = [f for f in required if f not in output]
    if missing:
        return False, [f"Missing: {f}" for f in missing]
    return True, []


def check_format(output: Dict[str, Any]) -> Tuple[bool, List[str]]:
    """Validate output format"""
    if not isinstance(output, dict):
        return False, ["Invalid format"]
    return True, []
'''
