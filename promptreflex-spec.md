# PromptReflex Technical Specification for Claude Code

## Project Overview
PromptReflex is a command-line tool for tracking, evaluating, and analyzing prompt performance with Claude Code. It allows prompt engineers to log interactions, evaluate prompt effectiveness, and build a portfolio of prompt-response pairs with qualitative assessments.

## Technical Requirements

### Core Components
1. Command-line interface for prompt logging
2. Command-line interface for prompt evaluation
3. File-based storage using JSON
4. Templated evaluation system
5. Basic reporting capabilities

### Technology Stack
- Python 3.11+
- CLI Framework: Click (preferred for more intuitive command structure)
- Storage: JSON files (organized by date/ID)
- LLM Integration: Manual copy-paste for MVP, with hooks for future API integration
- Project Structure: Modular design with separate modules for logging, evaluation, and utilities

## Detailed Implementation Specifications

### 1. Main CLI Structure

```python
# Main entry point: promptreflex.py

import click
from commands import log_cmd, evaluate_cmd, list_cmd

@click.group()
def cli():
    """PromptReflex: A tool for tracking and evaluating Claude Code prompts."""
    pass

cli.add_command(log_cmd.log)
cli.add_command(evaluate_cmd.evaluate)
cli.add_command(list_cmd.list_prompts)

if __name__ == "__main__":
    cli()
```

### 2. Prompt Logging Module

The logging module should:
- Generate unique IDs for prompts based on timestamp and counter
- Accept prompt text, response text, tags, and notes as input
- Save to JSON with proper formatting
- Handle file I/O with appropriate error handling

```python
# commands/log_cmd.py

import click
import json
import os
from datetime import datetime
from utils.file_manager import save_prompt, generate_id

@click.command("log")
@click.option("--prompt", "-p", required=True, help="The prompt sent to Claude Code")
@click.option("--response", "-r", required=True, help="Claude Code's response")
@click.option("--tags", "-t", multiple=True, help="Tags to categorize the prompt")
@click.option("--notes", "-n", default="", help="Additional notes about the prompt or response")
def log(prompt, response, tags, notes):
    """Log a new prompt and response pair."""
    # Implementation details...
```

### 3. Evaluation Module

The evaluation module should:
- Load a specific prompt by ID
- Generate an evaluation prompt using a template
- Accept evaluation response and score
- Update the original JSON file with evaluation data

```python
# commands/evaluate_cmd.py

import click
import json
import os
from utils.file_manager import load_prompt, update_prompt, get_template

@click.command("evaluate")
@click.argument("prompt_id")
@click.option("--response", "-r", help="Evaluation response from Claude")
@click.option("--score", "-s", type=int, help="Score from 1-5")
@click.option("--generate-template", "-g", is_flag=True, help="Generate evaluation template only")
def evaluate(prompt_id, response, score, generate_template):
    """Evaluate a logged prompt by ID."""
    # Implementation details...
```

### 4. Data Models

Define the core data structure for prompts:

```python
# models/prompt.py

from dataclasses import dataclass, asdict
from datetime import datetime
from typing import List, Optional

@dataclass
class Prompt:
    id: str
    date: str
    prompt: str
    response: str
    tags: List[str]
    notes: str
    evaluation_prompt: Optional[str] = None
    evaluation_response: Optional[str] = None
    score: Optional[int] = None
    
    def to_dict(self):
        return asdict(self)
    
    @classmethod
    def from_dict(cls, data):
        return cls(**data)
```

### 5. File Management Utilities

Utilities for handling file operations:

```python
# utils/file_manager.py

import json
import os
from datetime import datetime
from models.prompt import Prompt

def generate_id():
    """Generate a unique ID based on timestamp and counter."""
    # Implementation details...

def get_prompts_dir():
    """Get the prompts directory, creating it if it doesn't exist."""
    # Implementation details...

def save_prompt(prompt_obj):
    """Save a prompt object to a JSON file."""
    # Implementation details...

def load_prompt(prompt_id):
    """Load a prompt by ID."""
    # Implementation details...

def update_prompt(prompt_obj):
    """Update an existing prompt JSON file."""
    # Implementation details...

def get_template(template_name="judge_prompt.txt"):
    """Get the content of a template file."""
    # Implementation details...
```

### 6. List and Report Module

Functionality to list and filter saved prompts:

```python
# commands/list_cmd.py

import click
import json
import os
import glob
from tabulate import tabulate
from utils.file_manager import get_prompts_dir

@click.command("list")
@click.option("--tag", "-t", help="Filter prompts by tag")
@click.option("--min-score", type=int, help="Filter by minimum score")
@click.option("--max-score", type=int, help="Filter by maximum score")
@click.option("--format", "-f", type=click.Choice(["table", "json"]), default="table", help="Output format")
def list_prompts(tag, min_score, max_score, format):
    """List all logged prompts with optional filtering."""
    # Implementation details...
```

## File Structure

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

## JSON File Format

Each prompt will be stored as a separate JSON file with this structure:

```json
{
  "id": "2025-05-17-001",
  "date": "2025-05-17",
  "prompt": "Write a Python function that checks if a string is a palindrome.",
  "response": "def is_palindrome(s): return s == s[::-1]",
  "tags": ["python", "string", "function"],
  "notes": "Very clean response, good use of slicing.",
  "evaluation_prompt": "<the LLM-as-a-Judge prompt sent>",
  "evaluation_response": "Score: 5\nReason: Elegant and correct one-liner.",
  "score": 5
}
```

## Implementation Approach

When implementing with Claude Code:

1. Start by creating the project structure and basic files
2. Implement the core data model and file utilities
3. Build the logging command functionality
4. Implement the evaluation command
5. Add the list/reporting functionality
6. Add error handling and documentation
7. Create unit tests for core functionality

## Error Handling

Implement robust error handling for:
- File I/O operations
- Invalid input validation
- Missing templates or directories
- Invalid prompt IDs
- Score validation (must be 1-5)

## Future Extensions

The code should be designed with these future enhancements in mind:
- API integration with Claude
- SQLite database for more complex querying
- Visualization capabilities
- Extended reporting and analytics
- Web interface

## Environment Setup

```
# requirements.txt
click>=8.1.7
tabulate>=0.9.0
python-dotenv>=1.0.0
```

This specification provides a comprehensive blueprint for implementing PromptReflex using Claude Code. The modular structure allows for easy extension and maintenance as the project evolves.
