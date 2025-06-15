import datasets
import ast

def is_valid_python_code(code):
    try:
        ast.parse(code)
        return True
    except Exception:
        return False

def preprocess_python_code_dataset():
    # Download the dataset
    dataset = datasets.load_dataset('jtatman/python-code-dataset-500k', split='train')
    processed = []

    for item in dataset:
        code = item.get('code')
        doc = item.get('docstring') or item.get('description')
        if code and doc and is_valid_python_code(code):
            processed.append({'code': code, 'docstring': doc})

    # Optionally, save or return the processed data
    # For demonstration, just return the first 1000 pairs
    return processed[:1000]
