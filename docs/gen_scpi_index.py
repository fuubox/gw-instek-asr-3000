"""Generate the SCPI-to-Python index from command method docstrings."""

import ast
from pathlib import Path

import mkdocs_gen_files


root = Path(__file__).parents[1] / "src" / "gw_instek_asr" / "commands"
rows: list[tuple[str, str, str]] = []
for path in sorted(root.glob("*.py")):
    if path.name == "__init__.py":
        continue
    tree = ast.parse(path.read_text(encoding="utf-8"))
    for node in ast.walk(tree):
        if not isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)) or node.name.startswith("_"):
            continue
        doc = ast.get_docstring(node)
        if not doc:
            continue
        first = doc.splitlines()[0].strip()
        if first.startswith(":"):
            rows.append((first, node.name, path.stem))

rows.sort(key=lambda row: (row[0].lower(), row[1]))
with mkdocs_gen_files.open("scpi-index.md", "w") as destination:
    destination.write("# SCPI-to-Python index\n\n")
    destination.write("Generated from public command method docstrings at build time.\n\n")
    destination.write("| SCPI path | Python method | Subsystem |\n| --- | --- | --- |\n")
    for scpi, method, module in rows:
        destination.write(f"| `{scpi}` | `{method}` | {module} |\n")
