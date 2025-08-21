import re
from typing import Optional


class AnswerParser:
    """
    A utility to extract the final answer from an LLM's text response.
    """

    def __init__(self):
        # Patterns are ordered from most specific to most general.
        # The primary patterns are case-insensitive for robustness.
        self.patterns = [
            # Matches "The final answer is: 123"
            re.compile(r"The final answer is\s*:*\s*(.+)", re.IGNORECASE),
            # Matches "The answer is 123"
            re.compile(r"The answer is\s*:*\s*(.+)", re.IGNORECASE),
            # Fallback: Matches a number at the end of the string, optionally
            # followed by a single word (e.g., "11 balls.") and a period.
            re.compile(r"(\b\d+(?:\.\d+)?\b)\s*\w*\.?\s*$", re.IGNORECASE),
        ]

    def extract_answer(self, text: str) -> Optional[str]:
        """
        Extracts the answer from the text using a series of regex patterns.

        Args:
            text: The block of text from the LLM response.

        Returns:
            The extracted answer as a string, or None if no answer is found.
        """
        text = text.strip()

        for pattern in self.patterns:
            match = pattern.search(text)
            if match:
                # The answer is the first captured group.
                answer = match.group(1).strip()
                # Clean up a potential trailing period if it's part of a broader match
                if answer.endswith("."):
                    answer = answer[:-1]
                return answer.strip()

        return None
