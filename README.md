

What Is This?

TestSmith is a local, LLM-powered test case generator that analyzes your Python codebase, identifies risky functions, and auto-generates high-quality `pytest` test cases — all without calling a single cloud API.


Project Overview: AI-Powered Test Generator

#Goal
To automatically generate **high-quality pytest test cases** for risky functions in a Python codebase using a **local LLM** (like GPT-2 via CTransformers). The tool analyzes code structure and risk, then prompts the LLM to write tests — saving time and improving coverage.


Key Components

1. **Static Code Analyzer**
- **Input**: Python source files
- **Output**: `analysis.json`
- **What it does**: Extracts structure of each file — functions, classes, arguments, docstrings, and complexity metrics.
- **Example**:
  ```json
  {
    "pycodar/cli.py": {
      "structure": {
        "functions": [
          {
            "name": "extract_code_structure",
            "args": ["file_path"],
            "docstring": "Extracts structure from code."
          }
        ]
      }
    }
  }
  

2. **Risk Mapping Module**
- **Input**: Code metrics and heuristics
- **Output**: `risk_map.json`
- **What it does**: Assigns a **risk score** to each function based on factors like:
  - Cyclomatic complexity
  - Nesting depth
  - Lack of input validation
- **Purpose**: Helps prioritize which functions need tests the most.


3. **Test Generator (Your Current Script)**
- **Input**: `analysis.json` + `risk_map.json`
- **Process**:
  1. Filters out low-risk functions (score < 0.5)
  2. Builds a prompt describing the function and its risks
  3. Sends the prompt to a **local LLM** (GPT-2 via CTransformers)
  4. Receives Python test code from the model
  5. Saves the test as `test_<function>.py` in `tests/generated/`
  **Output**: Auto-generated test files


Technologies Used

| Tool/Library       | Purpose                                      |
|--------------------|----------------------------------------------|
| `langchain`        | Prompt templating and LLM chaining           |
| `ctransformers`    | Lightweight local LLM inference              |
| `pytest`           | Target test framework                        |
| `json`             | Input/output data handling                   |
| `os`               | File system operations                       |



Example Flow

1. You run:
   ```bash
   python test_generator.py
   ```

2. It finds a risky function like:
   ```python
   def extract_code_structure(file_path):
       """Extracts structure from code."""
   ```

3. It builds a prompt:
   ```
   Function name: extract_code_structure
   Arguments: file_path
   Docstring: Extracts structure from code.
   Risk factors: high cyclomatic complexity, deeply nested logic
   ```

4. The LLM replies with:
   ```python
   def test_extract_code_structure_valid_file():
       result = extract_code_structure("example.py")
       assert isinstance(result, dict)
   ```

5. The test is saved to:
   ```
   tests/generated/test_extract_code_structure.py
   ```
orks offline with local models


##  Setup & Run

### 1. Install Ollama
```bash
curl -fsSL https://ollama.com/install.sh | sh
```

### 2. Pull a Model
```bash
ollama pull mistral
```

### 3. Start the Ollama Server
```bash
ollama serve
```

### 4. Run the Test Generator
```bash
python test_generator.py
```


## Sample Prompt

```
Function name: extract_code_structure
Arguments: file_path
Docstring: Extracts structure from code.
Risk factors: high cyclomatic complexity, deeply nested logic

🎯 Task:
Generate high-quality pytest test cases.
Focus on edge cases, invalid input, boundary values, and any risky logic.
```


## 🌱 Why This Project?

Because I’m not just writing tests —  
I’m building intelligent systems that understand code, reason about risk, and generate value.

This project is my playground for:
- Experimenting with **LLM prompting** for structured code generation
- Exploring **risk-aware testing strategies**
- Learning how to **run and fine-tune local models**
- Designing **modular, scalable AI tools** for real-world QA workflows


## About Me

Hi, I’m **Prarthana Kulkarni** —  
A Software Development Engineer in Test who’s passionate about:
- Building AI-powered tools for QA
- Exploring LLMs, NLP, and automation frameworks
- Learning fast, building boldly, and sharing what I discover

Let’s connect and build the future of intelligent testing. 🚀

