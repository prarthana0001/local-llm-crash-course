import argparse
import json

from code_intelligence.utils import find_py_files
from code_intelligence.static_analyzer import analyze_file
from code_intelligence.complexity_metrics import (
    get_cyclomatic_complexity,
    get_maintainability_index,
    count_nesting_levels,
)

def analyze_project(path: str) -> dict:
    """
    Analyze all Python files in the given directory.
    Returns a dictionary mapping each file to its structural and complexity info.
    """
    results = {}

    for file_path in find_py_files(path):
        analysis = analyze_file(file_path)

        # If parse failed, skip complexity checks
        if "error" in analysis:
            results[file_path] = analysis
            continue

        # Read raw source for complexity + nesting
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                source = f.read()
        except Exception as e:
            results[file_path] = {"file": file_path, "error": f"Read error: {e}"}
            continue

        complexity = get_cyclomatic_complexity(source)
        maintainability = get_maintainability_index(source)
        nesting = count_nesting_levels(source)

        # Bundle everything together
        results[file_path] = {
            "structure": analysis,
            "metrics": {
                "cyclomatic_complexity": complexity,
                "maintainability_index": maintainability,
                "nesting_depth": nesting
            }
        }

    return results


def main():
    parser = argparse.ArgumentParser(description="Code Intelligence Engine — Static Analyzer CLI")
    parser.add_argument("--path", type=str, required=True, help="Path to Python codebase")
    parser.add_argument("--out", type=str, default=None, help="Optional: path to save output JSON")
    args = parser.parse_args()

    print(f"🔍 Analyzing codebase at: {args.path}")
    analysis_results = analyze_project(args.path)

    if args.out:
        with open(args.out, "w", encoding="utf-8") as outfile:
            json.dump(analysis_results, outfile, indent=2)
        print(f"✅ Results saved to: {args.out}")
    else:
        print(json.dumps(analysis_results, indent=2))


if __name__ == "__main__":
    main()
