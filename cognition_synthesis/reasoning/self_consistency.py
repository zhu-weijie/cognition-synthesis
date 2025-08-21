from collections import Counter
from typing import List, Optional, Tuple

from cognition_synthesis.llm.client import LLMClient
from cognition_synthesis.parsing.parser import AnswerParser


class SelfConsistency:
    """
    Implements the self-consistency reasoning technique.
    """

    def __init__(self, llm_client: LLMClient, parser: AnswerParser):
        self.llm_client = llm_client
        self.parser = parser

    def reason(
        self, prompt: str, n_samples: int = 5
    ) -> Tuple[Optional[str], List[str]]:
        """
        Generates multiple reasoning paths and finds the most consistent answer.

        Args:
            prompt: The prompt to send to the LLM.
            n_samples: The number of samples to generate.

        Returns:
            A tuple containing:
            - The most frequent answer (or None if no answers are found).
            - The list of all raw responses from the LLM.
        """
        print(f"\n--- Generating {n_samples} diverse reasoning paths... ---")
        raw_responses = self.llm_client.query_sample_n(prompt, n_samples)

        if not raw_responses:
            return None, []

        answers = []
        for i, resp in enumerate(raw_responses):
            extracted_answer = self.parser.extract_answer(resp)
            if extracted_answer:
                answers.append(extracted_answer)
            print(f"Path {i+1} Answer: {extracted_answer or 'N/A'}")

        if not answers:
            print("Could not extract any valid answers from the paths.")
            return None, raw_responses

        # Tally the answers and find the most common one
        answer_counts = Counter(answers)
        most_common_answer = answer_counts.most_common(1)[0][0]

        print(f"Answer counts: {dict(answer_counts)}")
        print(f"Most consistent answer: {most_common_answer}")

        return most_common_answer, raw_responses
