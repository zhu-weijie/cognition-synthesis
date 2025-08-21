from cognition_synthesis.llm.client import LLMClient


def run_last_letter_concatenation_task():
    """
    Runs the 'last letter concatenation' task as a demonstration.
    """
    print("--- Running Last Letter Concatenation Task ---")

    # Initialize the client
    # We use gpt-4o-mini as it's capable and cost-effective
    llm_client = LLMClient(model="gpt-4o-mini")

    # Define the problem
    problem = "What's the output when concatenating the last letter of each word of 'artificial intelligence'?"

    print(f"Problem: {problem}")

    # Query the LLM
    response = llm_client.query(problem)

    print(f"LLM Response: {response}")
    print("---------------------------------------------")


if __name__ == "__main__":
    run_last_letter_concatenation_task()
