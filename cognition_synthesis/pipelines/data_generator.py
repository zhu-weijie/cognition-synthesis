import json

from cognition_synthesis.llm.client import LLMClient
from cognition_synthesis.prompts.manager import PromptManager
from cognition_synthesis.reasoning.self_consistency import SelfConsistency
from cognition_synthesis.verification.verifier import Verifier, ProblemBank
from cognition_synthesis.parsing.parser import AnswerParser


class DataGenerator:
    """
    Orchestrates the generation of a fine-tuning dataset by using a verifier
    to select correct reasoning paths from an LLM.
    """

    def __init__(self, llm_client: LLMClient, output_file: str):
        self.prompt_manager = PromptManager()
        self.parser = AnswerParser()
        self.self_consistency = SelfConsistency(llm_client, self.parser)
        self.problem_bank = ProblemBank()
        self.verifier = Verifier()
        self.output_file = output_file

    def run(self, problem_id: str, n_samples: int = 8):
        """
        Runs the data generation pipeline for a single problem.
        """
        problem_data = self.problem_bank.get_problem(problem_id)
        if not problem_data:
            print(f"Error: Problem with ID '{problem_id}' not found.")
            return

        problem = problem_data["problem"]
        ground_truth = problem_data["ground_truth_answer"]

        print(f"\n--- Generating dataset for problem: {problem_id} ---")
        print(f"Problem: {problem}")
        print(f"Ground Truth Answer: {ground_truth}\n")

        cot_prompt = self.prompt_manager.create_zero_shot_cot_prompt(problem)

        # We don't need the final answer from self_consistency, just the raw paths
        _, raw_responses = self.self_consistency.reason(cot_prompt, n_samples)

        correct_paths = 0
        with open(self.output_file, "a") as f:
            for response in raw_responses:
                extracted_answer = self.parser.extract_answer(response)

                # Use the verifier to check correctness
                if self.verifier.verify(extracted_answer, ground_truth):
                    correct_paths += 1
                    # Format the data point as a JSON object for fine-tuning
                    data_point = {
                        "problem": problem,
                        "reasoning_path": response,
                    }
                    # Write the JSON object as a single line in the output file
                    f.write(json.dumps(data_point) + "\n")

        print(
            f"\nFinished. Found and saved {correct_paths}/{n_samples} correct reasoning paths to '{self.output_file}'."
        )
        print("-------------------------------------------------")
