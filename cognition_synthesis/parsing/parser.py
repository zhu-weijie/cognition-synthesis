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
            # Priority 1: Explicit phrases (case-insensitive)
            re.compile(r"The final answer is\s*:*\s*(.+)", re.IGNORECASE),
            # Matches "The answer is 123"
            re.compile(r"The answer is\s*:*\s*(.+)", re.IGNORECASE),
            re.compile(r"The output is\s*:*\s*(.+)", re.IGNORECASE),
            # Priority 2: A number at the end of the string, allowing for a few
            # trailing words (e.g., "6 apples left."). This is anchored to the
            # end of the string (`$`) to avoid false positives.
            # It matches a number, followed by 0 to 3 "word-like" segments.
            re.compile(
                r".*?(\b\d+(?:\.\d+)?\b)(?:\s*\w+){0,3}\.?\s*$",
                re.IGNORECASE | re.DOTALL,
            ),
        ]

    def extract_answer(self, text: str) -> Optional[str]:
        """
        Extracts the answer from the text using a series of regex patterns.

        Args:
            text: The block of text from the LLM response.

        Returns:
            The extracted answer as a string, or None if no answer is found.
        """
        # Pre-process to remove common markdown and strip whitespace
        text = text.strip().replace("**", "")

        for pattern in self.patterns:
            match = pattern.search(text)
            if match:
                # The answer is the last captured group. For our fallback regex,
                # it's group(1). For others, it's also group(1).
                answer = match.groups()[-1].strip()
                if answer.endswith("."):
                    answer = answer[:-1]
                return answer.strip('""')

        return None
