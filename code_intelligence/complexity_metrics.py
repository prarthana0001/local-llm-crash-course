import ast
from radon.complexity import cc_visit, cc_rank
from radon.metrics import mi_visit
from typing import Dict, Any


def get_cyclomatic_complexity(source_code: str) -> Dict[str, Any]:
    """
    Calculate cyclomatic complexity using radon's cc_visit.
    Returns a breakdown per function/method along with average and max scores.
    """
    try:
        blocks = cc_visit(source_code)
        if not blocks:
            return {"average": 0.0, "max": 0.0, "functions": []}

        scores = [b.complexity for b in blocks]
        ranked = [{"name": b.name, "complexity": b.complexity, "rank": cc_rank(b.complexity)} for b in blocks]

        return {
            "average": round(sum(scores) / len(scores), 2),
            "max": max(scores),
            "functions": ranked
        }
    except Exception as e:
        return {"error": str(e)}


def get_maintainability_index(source_code: str) -> float:
    """
    Uses radon's MI scoring to estimate maintainability (higher is better).
    Returns a float between 0–100.
    """
    try:
        return round(mi_visit(source_code, False), 2)
    except Exception:
        return 0.0


def count_nesting_levels(source_code: str) -> int:
    """
    Estimates the maximum depth of nesting in the code.
    """
    try:
        tree = ast.parse(source_code)

        def get_depth(node, depth=0):
            if not hasattr(node, 'body') or not isinstance(node.body, list):
                return depth
            return max(
            (get_depth(child, depth + 1) for child in node.body if isinstance(child, ast.AST)), default=depth
)
        return get_depth(tree)
    except Exception:
        return 0
