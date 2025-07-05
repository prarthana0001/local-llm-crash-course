import ast
from typing import Dict, Any


class CodeAnalyzer(ast.NodeVisitor):
    def __init__(self):
        self.classes = []
        self.functions = []
        self.imports = []

    def visit_Import(self, node):
        for alias in node.names:
            self.imports.append({
                "module": alias.name,
                "alias": alias.asname
            })
        self.generic_visit(node)

    def visit_ImportFrom(self, node):
        for alias in node.names:
            self.imports.append({
                "module": node.module,
                "name": alias.name,
                "alias": alias.asname
            })
        self.generic_visit(node)

    def visit_FunctionDef(self, node):
        self.functions.append({
            "name": node.name,
            "args": [arg.arg for arg in node.args.args],
            "docstring": ast.get_docstring(node)
        })
        self.generic_visit(node)

    def visit_ClassDef(self, node):
        class_info = {
            "name": node.name,
            "docstring": ast.get_docstring(node),
            "methods": []
        }

        for item in node.body:
            if isinstance(item, ast.FunctionDef):
                class_info["methods"].append({
                    "name": item.name,
                    "args": [arg.arg for arg in item.args.args],
                    "docstring": ast.get_docstring(item)
                })

        self.classes.append(class_info)
        self.generic_visit(node)


def analyze_file(file_path: str) -> Dict[str, Any]:
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            source_code = file.read()
        tree = ast.parse(source_code)
        analyzer = CodeAnalyzer()
        analyzer.visit(tree)
        return {
            "file": file_path,
            "functions": analyzer.functions,
            "classes": analyzer.classes,
            "imports": analyzer.imports
        }
    except (SyntaxError, UnicodeDecodeError) as e:
        return {
            "file": file_path,
            "error": str(e)
        }
