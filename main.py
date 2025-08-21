from cognition_synthesis.llm.client import LLMClient
from cognition_synthesis.prompts.manager import PromptManager


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
    print("---------------------------------------------\n")


def run_cot_math_task():
    """
    Demonstrates the difference between direct and CoT prompting.
    """
    print("--- Running Chain-of-Thought Math Task ---")

    llm_client = LLMClient(model="gpt-4o-mini")
    prompt_manager = PromptManager()

    problem = "I have 5 apples. I buy 2 more apples. Then I eat 1 apple. How many apples do I have left?"
    print(f"Problem: {problem}\n")

    # 1. Direct query (often fails on multi-step logic)
    print("--- 1. Direct Query ---")
    direct_response = llm_client.query(problem)
    print(f"LLM Response: {direct_response}\n")

    # 2. Zero-Shot CoT query
    print("--- 2. Zero-Shot CoT Query ---")
    zero_shot_prompt = prompt_manager.create_zero_shot_cot_prompt(problem)
    zero_shot_response = llm_client.query(zero_shot_prompt)
    print(f"LLM Response:\n{zero_shot_response}\n")

    # 3. Few-Shot CoT query
    print("--- 3. Few-Shot CoT Query ---")
    examples = [
        {
            "problem": "Roger has 5 tennis balls. He buys 2 cans of tennis balls. Each can has 3 tennis balls. How many tennis balls does he have now?",
            "reasoning": "Roger started with 5 balls. 2 cans of 3 tennis balls each is 2 * 3 = 6 balls. So in total he has 5 + 6 = 11 balls.",
            "answer": "11",
        }
    ]
    few_shot_prompt = prompt_manager.create_few_shot_cot_prompt(problem, examples)
    few_shot_response = llm_client.query(few_shot_prompt)
    print(f"LLM Response:\n{few_shot_response}")
    print("----------------------------------------")


if __name__ == "__main__":
    run_last_letter_concatenation_task()
    run_cot_math_task()
