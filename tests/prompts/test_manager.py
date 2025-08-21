import pytest
from cognition_synthesis.prompts.manager import PromptManager


@pytest.fixture
def manager():
    """Provides a PromptManager instance for tests."""
    return PromptManager()


def test_create_zero_shot_cot_prompt(manager):
    """
    Tests that the zero-shot prompt is formatted correctly.
    """
    problem = "How many apples are there?"
    expected = "How many apples are there?\n\nLet's think step by step."
    assert manager.create_zero_shot_cot_prompt(problem) == expected


def test_create_few_shot_cot_prompt(manager):
    """
    Tests that the few-shot prompt is formatted correctly with examples.
    """
    problem = "A third problem."
    examples = [
        {
            "problem": "First example problem.",
            "reasoning": "Step 1 reasoning.",
            "answer": "A",
        },
        {
            "problem": "Second example problem.",
            "reasoning": "Step 2 reasoning.",
            "answer": "B",
        },
    ]

    expected_prompt = (
        "Problem: First example problem.\n"
        "Answer: Step 1 reasoning.\n"
        "The final answer is A."
        "\n\n---\n\n"
        "Problem: Second example problem.\n"
        "Answer: Step 2 reasoning.\n"
        "The final answer is B."
        "\n\n---\n\n"
        "Problem: A third problem.\n"
        "Answer:"
    )

    assert manager.create_few_shot_cot_prompt(problem, examples) == expected_prompt
