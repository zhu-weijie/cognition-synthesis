# Cognition-Synthesis: Architectural Design

This document outlines the software architecture for the `cognition-synthesis` project. The diagrams are created using Mermaid to provide a clear visual reference for the system's components and their interactions.

## 1. Class Diagram

The Class Diagram shows the static structure of the project, detailing the key classes and their relationships. It highlights how responsibilities are divided among different components.

-   `DataGenerator` is the main orchestrator.
-   It uses a `ProblemBank` to get problems and a `Verifier` to check answers.
-   It relies on `SelfConsistency` to manage the reasoning process.
-   `SelfConsistency` in turn uses the `LLMClient` to interact with the external API and the `AnswerParser` to extract results from the responses.

```mermaid
classDiagram
    direction TD
    class DataGenerator {
        -prompt_manager: PromptManager
        -parser: AnswerParser
        -self_consistency: SelfConsistency
        -problem_bank: ProblemBank
        -verifier: Verifier
        -output_file: str
        +run(problem_id, n_samples) void
    }
    class ProblemBank {
        +get_problem(problem_id) Dict
    }
    class Verifier {
        +verify(extracted_answer, ground_truth) bool
    }
    class SelfConsistency {
        -llm_client: LLMClient
        -parser: AnswerParser
        +reason(prompt, n_samples) Tuple[str, List~str~]
    }
    class LLMClient {
        -client: OpenAI
        -model: str
        +query(prompt) str
        +query_sample_n(prompt, n) List~str~
    }
    class AnswerParser {
        +extract_answer(text) str
    }
    class PromptManager {
        +create_zero_shot_cot_prompt(problem) str
        +create_few_shot_cot_prompt(problem, examples) str
    }

    DataGenerator *-- "1" SelfConsistency : composes
    DataGenerator *-- "1" ProblemBank : composes
    DataGenerator *-- "1" Verifier : composes
    DataGenerator *-- "1" PromptManager : composes
    
    SelfConsistency *-- "1" LLMClient : composes
    SelfConsistency *-- "1" AnswerParser : composes
```

## 2. Sequence Diagram

This Sequence Diagram illustrates the dynamic interactions between objects when the `run_data_generation_pipeline()` function is executed. It shows the flow of calls from the main script through the components to generate and verify a single correct reasoning path.

```mermaid
sequenceDiagram
    participant Main as main.py
    participant DG as DataGenerator
    participant PM as PromptManager
    participant PB as ProblemBank
    participant SC as SelfConsistency
    participant LLM as LLMClient
    participant AP as AnswerParser
    participant V as Verifier

    Main->>DG: run("math_001")
    DG->>PB: get_problem("math_001")
    PB-->>DG: problem_data
    
    DG->>PM: create_zero_shot_cot_prompt(problem)
    PM-->>DG: cot_prompt

    DG->>SC: reason(cot_prompt, 8)
    SC->>LLM: query_sample_n(prompt, 8)
    LLM-->>SC: raw_responses
    
    %% The SelfConsistency component processes each raw response to create a list of structured objects
    loop For each raw_response
        SC->>AP: extract_answer(raw_response)
        AP-->>SC: extracted_answer
        SC->>SC: Bundles (raw_response, extracted_answer)
    end
    
    %% It returns the fully processed list, avoiding redundant work in DataGenerator
    SC-->>DG: Returns List of (response, answer) pairs

    loop For each (response, answer) pair
        DG->>V: verify(answer, ground_truth)
        V-->>DG: is_correct
        alt if is_correct
            DG->>DG: save_to_file(response)
        end
    end
```

## 3. C4 Component Diagram

The C4 model helps to visualize software architecture at different levels of abstraction. This Component Diagram shows the main components within the `cognition-synthesis` system. It provides a high-level view of how the system is structured.

```mermaid
C4Component
    title Component diagram for Cognition-Synthesis System

    Person(user, "User", "A developer running the script via the command line or an IDE.")

    Container_Boundary(app, "Cognition-Synthesis Application") {
        Component(main, "main.py", "Python Script", "Main entry point. Orchestrates the full demonstration.")
        Component(pipeline, "DataGenerator", "Python Class", "Orchestrates the data generation process for a given problem.")
        Component(reasoning, "SelfConsistency", "Python Class", "Implements the core reasoning technique by generating and evaluating multiple paths.")
        Component(verification, "Verifier & ProblemBank", "Python Classes", "Provides problems with ground-truth answers and validates model outputs.")
        Component(llm_wrapper, "LLMClient", "Python Class", "A dedicated wrapper for handling all communication with the external OpenAI API.")
        Component(utils, "Parser & Prompter", "Python Classes", "A collection of utility classes for building prompts and parsing text responses.")
    }

    System_Ext(openai, "OpenAI API", "External Service", "The Large Language Model API used for generation.")

    Rel(user, main, "Executes")
    Rel(main, pipeline, "Invokes")
    
    Rel(pipeline, reasoning, "Uses")
    Rel(pipeline, verification, "Uses")
    Rel(pipeline, utils, "Uses")

    Rel(reasoning, llm_wrapper, "Makes API calls via")
    Rel(reasoning, utils, "Uses")

    Rel(llm_wrapper, openai, "Sends prompts to", "HTTPS/JSON")
```

## 4. State Diagram

This State Diagram models the states of a single "Problem" as it moves through our data generation pipeline. It provides a simple, clear view of the lifecycle of a problem during processing.

```mermaid
stateDiagram-v2
    direction LR

    [*] --> Pending: Problem is loaded from bank
    
    Pending --> GeneratingPaths: generator.run() is called
    
    GeneratingPaths --> VerifyingPaths: LLM returns all responses
    
    state VerifyingPaths {
        direction LR
        [*] --> CheckingPath
        CheckingPath --> SavingPath: [Path is correct]
        CheckingPath --> CheckingPath: [Next path]
        SavingPath --> CheckingPath: [Save complete]
        CheckingPath --> [*]: [All paths processed]
    }
    
    VerifyingPaths --> Completed
    
    Completed --> [*]
```
