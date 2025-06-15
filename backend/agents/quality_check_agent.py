from autogen import ConversableAgent

def get_quality_check_agent(llm_config):
    agent = ConversableAgent(
        "quality_check_agent",
        system_message=(
            "You are a code documentation quality checker. "
            "Given Python code and a generated docstring, evaluate the docstring for accuracy, completeness, and clarity. "
            "Suggest improvements if necessary, otherwise reply 'Docstring is good.'"
        ),
        llm_config=llm_config
    )
    return agent
