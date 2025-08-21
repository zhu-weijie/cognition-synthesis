# Cognition-Synthesis

[![Python 3.12+](https://img.shields.io/badge/python-3.12+-blue.svg)](https://www.python.org/downloads/)

> "For LLMs, reasoning is always better than no reasoning... Aggregating multiple answers is better than one answer... Retrieval plus reasoning is better than reasoning only." - Denny Zhou, Stanford CS25

This project is a practical implementation of the key techniques for enhancing Large Language Model (LLM) reasoning, as presented in Denny Zhou's talk at Stanford's CS25. It translates theoretical concepts into a working Python application, demonstrating a structured approach to building more reliable and verifiable AI systems.

## Core Concepts Implemented

This repository explores and implements a pipeline of advanced reasoning techniques:

1.  **Chain-of-Thought (CoT) Prompting:** Moving beyond simple queries to encourage models to "think step by step," improving their accuracy on multi-step problems.
2.  **Robust Answer Parsing:** A test-driven parser to reliably extract final answers from an LLM's verbose, natural language output.
3.  **Self-Consistency:** A powerful technique to improve accuracy by generating multiple diverse reasoning paths and selecting the most frequent answer (majority vote).
4.  **Self-Improvement Data Generation:** A pipeline that simulates Reinforcement Learning from AI Feedback (RLAIF) by using a verifier to filter for high-quality, correct reasoning paths, which can then be used for fine-tuning.
5.  **Dockerization:** The entire application is containerized with Docker, ensuring a portable, reproducible, and easy-to-run environment.

## System Architecture

For a deeper dive into the architecture, including Class and Sequence diagrams, please see the [**Architectural Design Document**](./docs/design.md).

## Getting Started

You can run this project either locally with a Python virtual environment or using Docker (recommended).

### Prerequisites

*   Python 3.12+
*   Docker Desktop (for the containerized approach)
*   An [OpenAI API Key](https://platform.openai.com/api-keys)

### 1. Clone the Repository

```bash
git clone https://github.com/zhu-weijie/cognition-synthesis.git
cd cognition-synthesis
```

### 2. Configure Your API Key

Create a `.env` file in the project root by copying the example:

```bash
cp .env.example .env
```

Now, edit the `.env` file and add your OpenAI API key:

```
OPENAI_API_KEY="your-api-key-goes-here"
```

### 3. Choose Your Setup Method

#### Option A: Run with Docker (Recommended)

This is the simplest and most reliable way to run the project.

**1. Build the Docker image:**
```bash
docker build -t cognition-synthesis .
```

**2. Run the application:**
The command below runs the full demonstration and uses a volume (`-v`) to save the generated `training_data.jsonl` file to your local directory.
```bash
docker run --rm --env-file .env -v "$(pwd):/app" cognition-synthesis
```

#### Option B: Run Locally

**1. Create and activate a virtual environment:**
```bash
# Create the environment
python3 -m venv venv

# Activate it (on macOS/Linux)
source venv/bin/activate
```

**2. Install dependencies:**
```bash
pip install -r requirements.txt
```

**3. Run the application:**
```bash
python main.py
```

## How It Works

Executing `main.py` (either locally or via Docker) will run a full demonstration of all the implemented techniques in sequence:
1.  **Basic & Chain-of-Thought Tasks:** Demonstrates the difference between direct queries and CoT prompting.
2.  **Self-Consistency Task:** Shows how majority voting over multiple reasoning paths can correct errors and improve reliability.
3.  **Data Generation Pipeline:** Simulates a self-improvement loop by:
    *   Taking problems with known answers from a `ProblemBank`.
    *   Generating 8 diverse reasoning paths for each problem.
    *   Using a `Verifier` to check which paths lead to the correct answer.
    *   Saving the correct `(problem, reasoning_path)` pairs to `training_data.jsonl`.

The final output is a high-quality, AI-generated dataset ready for fine-tuning.

## Project Structure

```
cognition-synthesis/
├── .dockerignore         # Excludes files from the Docker image
├── .env                  # Stores your API key (gitignored)
├── .env.example          # An example environment file
├── Dockerfile            # Blueprint for the Docker container
├── main.py               # Main entry point for the application
├── requirements.txt      # Project dependencies
├── cognition_synthesis/  # Main application source code
│   ├── llm/              # LLM client wrapper
│   ├── parsing/          # Answer parsing logic
│   ├── pipelines/        # Data generation pipeline orchestrator
│   ├── prompts/          # Prompt management and formatting
│   ├── reasoning/        # Core reasoning techniques (e.g., SelfConsistency)
│   └── verification/     # Verifier and ProblemBank
├── docs/
│   └── design.md         # Detailed architectural diagrams
└── tests/                # Unit tests for the project
```
