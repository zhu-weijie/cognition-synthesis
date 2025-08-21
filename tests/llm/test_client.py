from unittest.mock import MagicMock, patch
from cognition_synthesis.llm.client import LLMClient


# This is a decorator to mock the OpenAI class during our test
@patch("cognition_synthesis.llm.client.OpenAI")
def test_llm_client_query(MockOpenAI):
    """
    Tests the query method of the LLMClient.
    It checks if the client is initialized and if it calls the API correctly.
    """
    # Arrange: Set up the mock
    mock_api_instance = MagicMock()
    mock_response = MagicMock()
    mock_response.choices[0].message.content = " LE"
    mock_api_instance.chat.completions.create.return_value = mock_response
    MockOpenAI.return_value = mock_api_instance

    # Act: Instantiate the client and call the method
    client = LLMClient(model="gpt-4o-mini")
    prompt = "Test prompt"
    result = client.query(prompt)

    # Assert: Check if the mocks were called as expected and result is correct
    MockOpenAI.assert_called_once()

    mock_api_instance.chat.completions.create.assert_called_once_with(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt},
        ],
        temperature=0.0,
    )

    assert result == "LE"
