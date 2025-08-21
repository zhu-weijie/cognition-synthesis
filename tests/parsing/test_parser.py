import pytest
from cognition_synthesis.parsing.parser import AnswerParser


@pytest.fixture
def parser():
    """Provides an AnswerParser instance for tests."""
    return AnswerParser()


@pytest.mark.parametrize(
    "input_text, expected_answer",
    [
        # Test pattern 1: "The final answer is..."
        ("Some reasoning steps... The final answer is 6.", "6"),
        ("Let's think. 2+2=4. The final answer is: 4", "4"),
        ("The final answer is LE.", "LE"),
        # Test pattern 2: "The answer is..."
        ("The answer is 11.", "11"),
        ("After all that, the answer is: six.", "six"),
        # Test pattern 3: Number at the end of the string
        ("He has 5 + 6 = 11 balls.", "11"),
        ("The result is 42", "42"),
        ("Some text that ends with a number 3.14", "3.14"),
        # Test cases that should NOT match
        ("There is no answer here.", None),
        ("The number 6 is in the middle of this sentence.", None),
        ("A final note on the answer.", None),
    ],
)
def test_extract_answer(parser, input_text, expected_answer):
    """
    Tests the extract_answer method with various text formats.
    """
    assert parser.extract_answer(input_text) == expected_answer
