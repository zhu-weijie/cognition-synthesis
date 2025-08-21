from cognition_synthesis.llm.client import LLMClient
from cognition_synthesis.prompts.manager import PromptManager
from cognition_synthesis.parsing.parser import AnswerParser
from cognition_synthesis.reasoning.self_consistency import SelfConsistency


def run_last_letter_concatenation_task():
    """
    Runs the 'last letter concatenation' task as a demonstration.
    """
    print("--- Running Last Letter Concatenation Task ---")

    # Initialize the client
    # We use gpt-4o-mini as it's capable and cost-effective
    llm_client = LLMClient(model="gpt-4o-mini")
    parser = AnswerParser()
    problem = "What's the output when concatenating the last letter of each word of 'artificial intelligence'?"

    print(f"Problem: {problem}")

    # Query the LLM
    response = llm_client.query(problem)

    print(f"LLM Response: {response}")

    extracted_answer = parser.extract_answer(response)
    print(f"Extracted Answer: {extracted_answer}")
    print("---------------------------------------------\n")


def run_cot_math_task():
    """
    Demonstrates the difference between direct and CoT prompting.
    """
    print("--- Running Chain-of-Thought Math Task ---")

    llm_client = LLMClient(model="gpt-4o-mini")
    prompt_manager = PromptManager()
    parser = AnswerParser()

    problem = "I have 5 apples. I buy 2 more apples. Then I eat 1 apple. How many apples do I have left?"
    print(f"Problem: {problem}\n")

    # 1. Direct query (often fails on multi-step logic)
    print("--- 1. Direct Query ---")
    direct_response = llm_client.query(problem)
    print(f"LLM Response: {direct_response}")
    direct_answer = parser.extract_answer(direct_response)
    print(f"Extracted Answer: {direct_answer}\n")

    # 2. Zero-Shot CoT query
    print("--- 2. Zero-Shot CoT Query ---")
    zero_shot_prompt = prompt_manager.create_zero_shot_cot_prompt(problem)
    zero_shot_response = llm_client.query(zero_shot_prompt)
    print(f"LLM Response:\n{zero_shot_response}")
    zero_shot_answer = parser.extract_answer(zero_shot_response)
    print(f"Extracted Answer: {zero_shot_answer}\n")

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
    few_shot_answer = parser.extract_answer(few_shot_response)
    print(f"Extracted Answer: {few_shot_answer}")
    print("----------------------------------------")


def run_self_consistency_task():
    """
    Demonstrates the self-consistency technique on a more complex problem.
    """
    print("\n\n--- Running Self-Consistency Task ---")

    # Setup
    llm_client = LLMClient(model="gpt-4o-mini")
    prompt_manager = PromptManager()
    parser = AnswerParser()
    self_consistency = SelfConsistency(llm_client, parser)

    # A more complex problem that can sometimes trip up the LLM
    problem = (
        "A grocery store sold 15 apples on Monday. On Tuesday, it sold twice as many "
        "apples as on Monday. On Wednesday, it sold 5 fewer apples than on Tuesday. "
        "How many apples were sold in total over the three days?"
    )
    print(f"Problem: {problem}")

    # Use a zero-shot CoT prompt to encourage reasoning
    cot_prompt = prompt_manager.create_zero_shot_cot_prompt(problem)

    # Run the self-consistency process
    final_answer, raw_responses = self_consistency.reason(cot_prompt, n_samples=5)

    print(f"\nFinal Consolidated Answer: {final_answer}")
    print("-----------------------------------")


if __name__ == "__main__":
    # run_last_letter_concatenation_task()
    # run_cot_math_task()
    run_self_consistency_task()
