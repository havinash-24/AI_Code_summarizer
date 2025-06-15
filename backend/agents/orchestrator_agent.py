from autogen import ConversableAgent

def get_orchestrator_agent(llm_config):
    return ConversableAgent(
        "orchestrator_agent",
        system_message=(
            "You are the orchestrator for the code documentation generator. "
            "Coordinate the workflow: (1) ensure data is preprocessed, (2) accept user code input, "
            "(3) send code to the doc generator agent, (4) send the result to the quality checker, "
            "(5) return the final docstring or suggestions."
        ),
        llm_config=llm_config
    )
