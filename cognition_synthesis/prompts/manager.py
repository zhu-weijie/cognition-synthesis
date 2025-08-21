from typing import List, Dict, Any


class PromptManager:
    """
    Manages the creation of different types of prompts.
    """

    ZERO_SHOT_COT_PHRASE = "Let's think step by step."

    def create_zero_shot_cot_prompt(self, problem: str) -> str:
        """
        Creates a zero-shot Chain-of-Thought prompt.

        Args:
            problem: The user's problem statement.

        Returns:
            A prompt formatted with the zero-shot CoT phrase.
        """
        return f"{problem}\n\n{self.ZERO_SHOT_COT_PHRASE}"

    def create_few_shot_cot_prompt(
        self, problem: str, examples: List[Dict[str, Any]]
    ) -> str:
        """
        Creates a few-shot Chain-of-Thought prompt from examples.

        Args:
            problem: The user's new problem statement.
            examples: A list of dictionaries, where each dict has 'problem',
                      'reasoning', and 'answer' keys.

        Returns:
            A prompt formatted with the provided examples.
        """
        formatted_examples = []
        for ex in examples:
            formatted_example = (
                f"Problem: {ex['problem']}\n"
                f"Answer: {ex['reasoning']}\n"
                f"The final answer is {ex['answer']}."
            )
            formatted_examples.append(formatted_example)

        prompt = "\n\n---\n\n".join(formatted_examples)
        prompt += f"\n\n---\n\nProblem: {problem}\nAnswer:"

        return prompt
