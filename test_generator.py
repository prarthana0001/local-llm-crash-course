import os
import json
import requests
from typing import Dict

LLM_URL = "http://localhost:11434/api/generate"  # Local Ollama-compatible endpoint
MODEL_NAME = "orca-mini-3b.q4_0.gguf"  # Replace with your actual model name from local LLM backend


def load_json(path: str) -> Dict:
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def prompt_llm(prompt_text: str) -> str:
    response = requests.post(LLM_URL, json={
        "model": MODEL_NAME,
        "prompt": prompt_text,
        "stream": False
    })
    return response.json().get("response", "")


def format_prompt(func_name: str, args, docstring: str, risk_reasons) -> str:
    joined_args = ", ".join(args) if args else "None"
    reasons = ", ".join(risk_reasons) if risk_reasons else "None"
    doc = docstring or "No docstring provided."

    return f"""
You are a Python test case generator.

Function name: {func_name}
Arguments: {joined_args}
Docstring: {doc}

Risk factors: {reasons}

🎯 Task:
Generate high-quality pytest test cases.
Focus on edge cases, invalid input, boundary values, and any risky logic.
Keep test names descriptive and readable.
Return only valid Python code.
"""


def save_test_file(func_name: str, test_code: str, output_dir: str = "tests/generated"):
    os.makedirs(output_dir, exist_ok=True)
    filename = f"test_{func_name}.py"
    path = os.path.join(output_dir, filename)

    with open(path, "w", encoding="utf-8") as f:
        f.write("# Auto-generated test file\n\n")
        f.write(test_code)

    print(f"✅ Test saved: {path}")


def generate_tests(analysis_path: str, risk_path: str):
    analysis = load_json(analysis_path)
    risk_map = load_json(risk_path)

    for file_path, funcs in risk_map.items():
        file_data = analysis.get(file_path, {})
        structure = file_data.get("structure", {})

        all_functions = {f["name"]: f for f in structure.get("functions", [])}
        for cls in structure.get("classes", []):
            for method in cls.get("methods", []):
                all_functions[method["name"]] = method

        for func_name, risk_data in funcs.items():
            score = risk_data.get("risk_score", 0)
            if score < 0.5:
                continue  # Skip low-risk functions

            func_data = all_functions.get(func_name, {})
            args = func_data.get("args", [])
            docstring = func_data.get("docstring", "")
            reasons = risk_data.get("reasons", [])

            prompt_text = format_prompt(func_name, args, docstring, reasons)
            print(f"🎯 Generating tests for: {func_name} (risk: {score})")
            test_code = prompt_llm(prompt_text)

            if test_code.strip():
                save_test_file(func_name, test_code)
            else:
                print(f"⚠️ No test code returned for: {func_name}")


if __name__ == "__main__":
    # Example usage:
    generate_tests("analysis.json", "risk_map.json")
