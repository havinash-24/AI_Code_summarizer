from autogen import ConversableAgent
import json
import os

# Loads locally preprocessed data
def preprocess_python_code_dataset():
    print("Loading local preprocessed dataset...")

    dataset_path = "processed_code_doc_pairs.json"

    if not os.path.exists(dataset_path):
        raise FileNotFoundError(f"{dataset_path} not found. Please run the preprocessing script first.")

    with open(dataset_path, "r", encoding="utf-8") as f:
        processed_data = json.load(f)

    # Return the first 1000 samples or however many are available
    return processed_data[:1000]

def get_data_preprocessing_agent(llm_config):
    agent = ConversableAgent(
        "data_preprocessing_agent",
        system_message="You load and return the locally saved, cleaned version of the jtatman/python-code-dataset-500k dataset.",
        llm_config=llm_config
    )

    # Make the function available to the LLM and callable by user_proxy
    agent.register_for_llm(
        name="preprocess_python_code_dataset",
        description="Loads and returns the locally saved, cleaned Python code dataset."
    )(preprocess_python_code_dataset)

    agent.register_for_execution(
        name="preprocess_python_code_dataset"
    )(preprocess_python_code_dataset)

    return agent
