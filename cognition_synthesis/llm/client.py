import os
from openai import OpenAI
from dotenv import load_dotenv


class LLMClient:
    """A wrapper for the OpenAI API client."""

    def __init__(self, model: str = "gpt-4o-mini"):
        """
        Initializes the LLMClient.

        Args:
            model: The name of the model to use (e.g., "gpt-4o-mini").
        """
        load_dotenv()
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("OPENAI_API_KEY environment variable not set.")

        self.client = OpenAI(api_key=api_key)
        self.model = model

    def query(self, prompt: str) -> str:
        """
        Sends a prompt to the LLM and returns the response.

        Args:
            prompt: The input prompt for the LLM.

        Returns:
            The content of the LLM's response as a string.
        """
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are a helpful assistant."},
                    {"role": "user", "content": prompt},
                ],
                temperature=0.0,
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            # Basic error handling
            return f"An error occurred: {e}"
