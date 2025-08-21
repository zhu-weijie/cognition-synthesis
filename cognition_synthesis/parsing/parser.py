import re
from typing import Optional


class AnswerParser:
    """
    A utility to extract the final answer from an LLM's text response.
    """

    def __init__(self):
        # Patterns are ordered from most specific to most general.
        self.patterns = [
            # Matches "The final answer is: 123" or "The final answer is 123."
            re.compile(r"The final answer is\s*:*\s*([^\n\.]+)\.?"),
            # Matches "The answer is 123"
            re.compile(r"The answer is\s*:*\s*([^\n\.]+)\.?"),
            # Matches a number (integer or float) at the very end of the string,
            # possibly followed by a period.
            re.compile(r"(\b\d+(?:\.\d+)?\b)[.\s]*$"),
        ]

    def extract_answer(self, text: str) -> Optional[str]:
        """
        Extracts the answer from the text using a series of regex patterns.

        Args:
            text: The block of text from the LLM response.

        Returns:
            The extracted answer as a string, or None if no answer is found.
        """
        # A simple normalization for consistency
        text = text.strip()

        for pattern in self.patterns:
            match = pattern.search(text)
            if match:
                # Return the first capturing group of the match
                return match.group(1).strip()

        return None
