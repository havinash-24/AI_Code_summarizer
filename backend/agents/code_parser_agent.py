import ast
import json
from autogen import ConversableAgent

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

def get_code_parser_agent(llm_config):
    """Returns an agent that can parse code using AST."""
    agent = ConversableAgent(
        "code_parser_agent",
        system_message="You analyze Python code structure using Abstract Syntax Tree (AST) parsing.",
        llm_config=llm_config
    )
    
    # Register the parse_code_with_ast function to be callable
    agent.register_for_llm(
        name="parse_code_with_ast",
        description="Parse Python code using AST to extract function/class names and parameters."
    )(parse_code_with_ast)
    
    agent.register_for_execution(
        name="parse_code_with_ast"
    )(parse_code_with_ast)
    
    return agent