# PromptReflex

A command-line tool for tracking, evaluating, and analyzing prompt performance with Claude Code.

## Overview

PromptReflex helps prompt engineers log interactions, evaluate prompt effectiveness, and build a portfolio of prompt-response pairs with qualitative assessments.

## Features

- Log prompts and responses with tags and notes
- Evaluate prompts using a standardized template
- Score and analyze prompt effectiveness
- List and filter prompts by various criteria
- Store data in JSON format for easy portability

## Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/promptreflex.git
cd promptreflex

# Install dependencies
pip install -r requirements.txt
```

## Usage

### Logging a Prompt

```bash
python promptreflex.py log --prompt "Your prompt text" --response "Claude's response" --tags tag1 tag2 --notes "Optional notes"
```

### Evaluating a Prompt

```bash
# Generate an evaluation template
python promptreflex.py evaluate PROMPT_ID --generate-template

# Log the evaluation
python promptreflex.py evaluate PROMPT_ID --response "Evaluation response" --score 4
```

### Listing Prompts

```bash
# List all prompts
python promptreflex.py list

# Filter by tag
python promptreflex.py list --tag python

# Filter by score
python promptreflex.py list --min-score 4

# Output as JSON
python promptreflex.py list --format json
```

## Project Structure

```
promptreflex/
├── README.md
├── requirements.txt
├── promptreflex.py            # Main CLI entry point
├── prompts/                   # Directory for stored prompts
├── commands/                  # CLI command modules
│   ├── __init__.py
│   ├── log_cmd.py
│   ├── evaluate_cmd.py
│   └── list_cmd.py
├── models/                    # Data models
│   ├── __init__.py
│   └── prompt.py
├── utils/                     # Utility functions
│   ├── __init__.py
│   └── file_manager.py
└── templates/                 # Template files
    └── judge_prompt.txt
```

## License

MIT