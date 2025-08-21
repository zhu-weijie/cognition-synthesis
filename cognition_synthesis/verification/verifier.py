from typing import List, Dict, Any, Optional


class ProblemBank:
    """A simple container for problems with known ground truth answers."""

    def __init__(self):
        self.problems: List[Dict[str, Any]] = [
            {
                "id": "math_001",
                "problem": "A grocery store sold 15 apples on Monday. On Tuesday, it sold twice as many "
                "apples as on Monday. On Wednesday, it sold 5 fewer apples than on Tuesday. "
                "How many apples were sold in total over the three days?",
                "ground_truth_answer": "70",
            },
            {
                "id": "math_002",
                "problem": "A car travels at 60 km/h for 2 hours, then at 80 km/h for 3 hours. "
                "What is the total distance traveled?",
                "ground_truth_answer": "360",
            },
        ]

    def get_problem(self, problem_id: str) -> Optional[Dict[str, Any]]:
        for p in self.problems:
            if p["id"] == problem_id:
                return p
        return None


class Verifier:
    """Checks if a model's extracted answer matches the ground truth."""

    def verify(self, extracted_answer: str, ground_truth_answer: str) -> bool:
        """
        Compares the extracted answer to the ground truth.
        Handles basic numeric and string comparison.
        """
        if not extracted_answer:
            return False

        try:
            # Try to compare as floats for robustness (e.g., "70" == "70.0")
            return float(extracted_answer) == float(ground_truth_answer)
        except (ValueError, TypeError):
            # Fallback to case-insensitive string comparison
            return (
                extracted_answer.lower().strip() == ground_truth_answer.lower().strip()
            )
