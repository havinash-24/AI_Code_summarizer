import torch
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
from autogen import ConversableAgent

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

def generate_transformer_docstring(code_snippet):
    """Generate a docstring using a transformer model."""
    try:
        transformer = TransformerDocGenerator()
        return transformer.generate_docstring(code_snippet)
    except Exception as e:
        return f"Error generating transformer docstring: {str(e)}"

def get_transformer_doc_agent(llm_config):
    """Returns an agent that can generate docstrings using transformers."""
    agent = ConversableAgent(
        "transformer_doc_agent",
        system_message="You generate Python docstrings using pre-trained transformer models.",
        llm_config=llm_config
    )
    
    # Register the generate_transformer_docstring function to be callable
    agent.register_for_llm(
        name="generate_transformer_docstring",
        description="Generate a docstring for Python code using a transformer model."
    )(generate_transformer_docstring)
    
    agent.register_for_execution(
        name="generate_transformer_docstring"
    )(generate_transformer_docstring)
    
    return agent