import os
import dotenv
import random
import json
import ast
import torch
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
from autogen import ConversableAgent
from agents.data_preprocessing_agent import get_data_preprocessing_agent, preprocess_python_code_dataset
from agents.code_doc_generation_agent import get_code_doc_generation_agent
from agents.quality_check_agent import get_quality_check_agent

dotenv.load_dotenv()

def parse_code_with_ast(code_snippet):
    """
    Parse Python code using AST to extract function/class names and parameters.
    Returns a structured summary of the code.
    """
    try:
        parsed = ast.parse(code_snippet)
        code_info = {"functions": [], "classes": [], "imports": []}
        
        # Extract imports, functions, and classes
        for node in ast.walk(parsed):
            if isinstance(node, ast.Import):
                for name in node.names:
                    code_info["imports"].append(name.name)
            elif isinstance(node, ast.ImportFrom):
                module = node.module or ""
                for name in node.names:
                    code_info["imports"].append(f"{module}.{name.name}")
            elif isinstance(node, ast.FunctionDef):
                args = [arg.arg for arg in node.args.args]
                code_info["functions"].append({
                    "name": node.name,
                    "args": args,
                    "returns": node.returns.id if node.returns and hasattr(node.returns, 'id') else None
                })
            elif isinstance(node, ast.ClassDef):
                methods = [m.name for m in node.body if isinstance(m, ast.FunctionDef)]
                code_info["classes"].append({
                    "name": node.name,
                    "methods": methods
                })
                
        return code_info
    except SyntaxError:
        # Handle case where code can't be parsed
        return {"error": "Syntax error in code", "raw_code": code_snippet}
    except Exception as e:
        return {"error": str(e), "raw_code": code_snippet}

class TransformerDocGenerator:
    """
    Uses Hugging Face transformers for code documentation generation.
    """
    def __init__(self, model_name="Salesforce/codet5-small-ntp"):
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.model = AutoModelForSeq2SeqLM.from_pretrained(model_name)
        
    def generate_docstring(self, code_snippet, max_length=512):
        # Prepare input
        inputs = self.tokenizer(f"generate docstring: {code_snippet}", 
                              return_tensors="pt", 
                              max_length=512, 
                              truncation=True)
        
        # Generate output
        with torch.no_grad():
            outputs = self.model.generate(
                inputs["input_ids"],
                max_length=max_length,
                num_return_sequences=1,
                early_stopping=True
            )
        
        # Decode and return output
        docstring = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
        return docstring

def run_pipeline(code_snippet):
    llm_config = {
        "config_list": [
            {"model": "gpt-4o-mini", "api_key": os.environ.get("OPENAI_API_KEY")}
        ]
    }

    user_proxy = ConversableAgent(
        "user_proxy",
        llm_config=False,
        system_message="You are the user."
    )

    # Step 1: Parse code with AST
    code_structure = parse_code_with_ast(code_snippet)
    code_structure_str = json.dumps(code_structure, indent=2)
    
    # Step 2: Preprocess dataset
    preprocessed_data = preprocess_python_code_dataset()
    
    # Select examples for reference
    examples = []
    if preprocessed_data and len(preprocessed_data) > 0:
        examples = random.sample(preprocessed_data, min(3, len(preprocessed_data)))
    
    # Prepare examples as a string to send to the data preprocessing agent
    examples_str = json.dumps(examples, indent=2)
    data_preprocessing_agent = get_data_preprocessing_agent(llm_config)
    
    # Inform the agent about the preprocessed data and examples
    preprocess_result = user_proxy.initiate_chat(
        recipient=data_preprocessing_agent,
        message=f"I have executed preprocess_python_code_dataset and have the preprocessed data. Here are some example entries that will be used as reference for docstring generation:\n\n{examples_str}",
        max_turns=2,
        summary_method="last_msg"
    )

    # Step 3: Generate initial docstring with transformer model
    try:
        transformer_gen = TransformerDocGenerator()
        transformer_docstring = transformer_gen.generate_docstring(code_snippet)
        transformer_docstring = f"Initial docstring from transformer model:\n{transformer_docstring}"
    except Exception as e:
        transformer_docstring = f"Transformer model error: {str(e)}"
    
    # Step 4: Generate refined docstring with LLM using transformer output, AST analysis, and examples
    example_context = ""
    if examples:
        example_context = "Here are some examples of good code-docstring pairs to use as reference:\n\n"
        for i, example in enumerate(examples):
            example_context += f"Example {i+1}:\nCode:\n{example['code']}\nDocstring:\n{example['docstring']}\n\n"
    
    # Construct prompt with all the information
    code_doc_prompt = f"""
    Code to document:
    ```python
    {code_snippet}
    ```
    
    Code structure (from AST analysis):
    ```json
    {code_structure_str}
    ```
    
    {transformer_docstring}
    
    {example_context}
    
    Based on the code structure, transformer output, and examples, generate a comprehensive and accurate docstring.
    """
    
    docstring_result = get_code_doc_generation_agent(llm_config).initiate_chat(
        recipient=get_code_doc_generation_agent(llm_config),
        message=code_doc_prompt,
        max_turns=2,
        summary_method="last_msg"
    )
    docstring = docstring_result.summary

    # Step 5: Quality check with enhanced information
    quality_result = get_quality_check_agent(llm_config).initiate_chat(
        recipient=get_quality_check_agent(llm_config),
        message=f"Code:\n{code_snippet}\nCode structure:\n{code_structure_str}\nDocstring:\n{docstring}",
        max_turns=2,
        summary_method="last_msg"
    )

    # Return output for API
    if "good" in quality_result.summary.lower():
        return { "doc": docstring, "code_structure": code_structure }
    else:
        return { "suggestions": quality_result.summary, "code_structure": code_structure }

# Optional: run from terminal
if __name__ == "__main__":
    import sys
    assert len(sys.argv) > 1, "Please provide a Python code snippet as input."
    code_snippet = sys.argv[1]
    result = run_pipeline(code_snippet)
    print(result)
