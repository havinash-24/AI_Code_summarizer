import json
import ast
import re
from datasets import load_dataset

def is_valid_python_code(code):
    try:
        ast.parse(code)
        return True
    except Exception:
        return False

def extract_first_code_block(text):
    """
    Extracts the first Python code block from markdown-style output.
    Supports both ```python ... ``` and inline code.
    """
    code_block = re.search(r"```(?:python)?(.*?)```", text, re.DOTALL)
    if code_block:
        return code_block.group(1).strip()
    return None

print("Downloading dataset...")
dataset = load_dataset('jtatman/python-code-dataset-500k', split='train')

processed = []
seen = set()

print("Processing entries...")
for item in dataset:
    output = item.get('output')
    doc = item.get('instruction')  # Using instruction as docstring context

    if output and doc:
        code = extract_first_code_block(output)
        if code and is_valid_python_code(code):
            code_clean = code.strip()
            doc_clean = doc.strip()

            key = (code_clean, doc_clean)
            if key not in seen:
                seen.add(key)
                processed.append({'code': code_clean, 'docstring': doc_clean})

    if len(processed) >= 1000:
        break

with open("processed_code_doc_pairs.json", "w", encoding="utf-8") as f:
    json.dump(processed, f, indent=2)

print(f"✅ Done! Saved {len(processed)} cleaned examples to processed_code_doc_pairs.json")
