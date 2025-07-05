from typing import Dict, Any


def score_function(function_name: str, structure: Dict[str, Any], metrics: Dict[str, Any]) -> Dict[str, Any]:
    """
    Compute a risk score for a given function based on heuristics.
    Returns a dict with score (0–1) and reason tags.
    """
    score = 0.0
    reasons = []

    # Heuristic 1: Cyclomatic Complexity > 10
    for func in metrics.get("cyclomatic_complexity", {}).get("functions", []):
        if func.get("name") == function_name and func.get("complexity", 0) > 10:
            score += 0.4
            reasons.append("high cyclomatic complexity")

    # Heuristic 2: Nesting Depth > 3
    if metrics.get("nesting_depth", 0) > 3:
        score += 0.2
        reasons.append("deeply nested logic")

    # Heuristic 3: FastAPI or inference relevance
    imports = structure.get("imports", [])
    for imp in imports:
        if imp.get("module") in ("fastapi", "pydantic", "uvicorn"):
            score += 0.2
            reasons.append("core inference route or API handler")
            break

    return {
        "risk_score": round(min(score, 1.0), 2),
        "reasons": reasons
    }


def generate_risk_map(analysis_results: Dict[str, Any]) -> Dict[str, Any]:
    """
    Loop through all analyzed files and score each function.
    """
    risk_map = {}

    for file_path, data in analysis_results.items():
        structure = data.get("structure", {})
        metrics = data.get("metrics", {})

        functions = [f["name"] for f in structure.get("functions", [])]
        class_methods = []
        for cls in structure.get("classes", []):
            for method in cls.get("methods", []):
                class_methods.append(method["name"])

        file_risks = {}

        for func_name in functions + class_methods:
            file_risks[func_name] = score_function(func_name, structure, metrics)

        risk_map[file_path] = file_risks

    return risk_map
