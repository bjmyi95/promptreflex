# ABOUTME: Utility functions for file operations in PromptReflex.
# ABOUTME: Handles generating IDs, loading and saving prompt data, and template handling.

import json
import os
import glob
from datetime import datetime
from typing import Dict, Optional, List
from models.prompt import Prompt


# Counter for generating unique IDs within the same date
_id_counter = {}


def generate_id(date: Optional[datetime] = None) -> str:
    """
    Generate a unique ID based on timestamp and counter.
    
    Args:
        date: Optional datetime object to use for the ID (default: current date)
        
    Returns:
        A unique ID in the format YYYY-MM-DD-NNN
    """
    if date is None:
        date = datetime.now()
    
    date_str = date.strftime("%Y-%m-%d")
    
    # Initialize or increment counter for this date
    if date_str not in _id_counter:
        _id_counter[date_str] = 1
    else:
        _id_counter[date_str] += 1
    
    # Format as YYYY-MM-DD-NNN with leading zeros
    return f"{date_str}-{_id_counter[date_str]:03d}"


def get_prompts_dir() -> str:
    """
    Get the prompts directory, creating it if it doesn't exist.
    
    Returns:
        The absolute path to the prompts directory
    """
    # Check environment variable first
    prompts_dir = os.environ.get('PROMPTREFLEX_PROMPTS_DIR')
    
    if not prompts_dir:
        # Default to a directory in the user's home
        prompts_dir = os.path.join(os.path.expanduser('~'), 'toy', 'promptreflex', 'prompts')
    
    # Create directory if it doesn't exist
    os.makedirs(prompts_dir, exist_ok=True)
    
    return prompts_dir


def get_templates_dir() -> str:
    """
    Get the templates directory.
    
    Returns:
        The absolute path to the templates directory
    """
    # Check environment variable first
    base_dir = os.environ.get('PROMPTREFLEX_DIR')
    
    if not base_dir:
        # Default to the package directory
        base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    
    templates_dir = os.path.join(base_dir, 'templates')
    
    # Ensure directory exists
    if not os.path.isdir(templates_dir):
        raise FileNotFoundError(f"Templates directory not found: {templates_dir}")
    
    return templates_dir


def save_prompt(prompt_obj: Prompt) -> str:
    """
    Save a prompt object to a JSON file.
    
    Args:
        prompt_obj: The Prompt object to save
        
    Returns:
        The path to the saved file
    """
    # Get the prompts directory
    prompts_dir = get_prompts_dir()
    
    # Convert to dictionary for serialization
    prompt_dict = prompt_obj.to_dict()
    
    # Create filename
    filename = f"{prompt_obj.id}.json"
    file_path = os.path.join(prompts_dir, filename)
    
    # Write to file
    with open(file_path, 'w') as f:
        json.dump(prompt_dict, f, indent=2)
    
    return file_path


def load_prompt(prompt_id: str) -> Prompt:
    """
    Load a prompt by ID.
    
    Args:
        prompt_id: The ID of the prompt to load
        
    Returns:
        The loaded Prompt object
        
    Raises:
        FileNotFoundError: If the prompt file doesn't exist
    """
    # Get the prompts directory
    prompts_dir = get_prompts_dir()
    
    # Construct file path
    file_path = os.path.join(prompts_dir, f"{prompt_id}.json")
    
    # Check if file exists
    if not os.path.isfile(file_path):
        raise FileNotFoundError(f"Prompt with ID {prompt_id} not found")
    
    # Read the file
    with open(file_path, 'r') as f:
        prompt_dict = json.load(f)
    
    # Convert to Prompt object
    return Prompt.from_dict(prompt_dict)


def update_prompt(prompt_obj: Prompt) -> str:
    """
    Update an existing prompt JSON file.
    
    Args:
        prompt_obj: The Prompt object with updated data
        
    Returns:
        The path to the updated file
        
    Raises:
        FileNotFoundError: If the prompt file doesn't exist
    """
    # Get the prompts directory
    prompts_dir = get_prompts_dir()
    
    # Construct file path
    file_path = os.path.join(prompts_dir, f"{prompt_obj.id}.json")
    
    # Check if file exists
    if not os.path.isfile(file_path):
        raise FileNotFoundError(f"Prompt with ID {prompt_obj.id} not found")
    
    # Convert to dictionary for serialization
    prompt_dict = prompt_obj.to_dict()
    
    # Write to file
    with open(file_path, 'w') as f:
        json.dump(prompt_dict, f, indent=2)
    
    return file_path


def get_template(template_name: str = "judge_prompt.txt") -> str:
    """
    Get the content of a template file.
    
    Args:
        template_name: The name of the template file
        
    Returns:
        The content of the template file
        
    Raises:
        FileNotFoundError: If the template file doesn't exist
    """
    # Get the templates directory
    templates_dir = get_templates_dir()
    
    # Construct file path
    template_path = os.path.join(templates_dir, template_name)
    
    # Check if file exists
    if not os.path.isfile(template_path):
        raise FileNotFoundError(f"Template file {template_name} not found")
    
    # Read the template file
    with open(template_path, 'r') as f:
        template_content = f.read()
    
    return template_content


def list_prompts(tag: Optional[str] = None, 
                min_score: Optional[int] = None,
                max_score: Optional[int] = None) -> List[Prompt]:
    """
    List and filter prompts.
    
    Args:
        tag: Optional tag to filter by
        min_score: Optional minimum score to filter by
        max_score: Optional maximum score to filter by
        
    Returns:
        A list of Prompt objects matching the filters
    """
    # Get the prompts directory
    prompts_dir = get_prompts_dir()
    
    # Get all JSON files
    json_files = glob.glob(os.path.join(prompts_dir, "*.json"))
    
    prompts = []
    
    # Load each file
    for file_path in json_files:
        try:
            with open(file_path, 'r') as f:
                prompt_dict = json.load(f)
                prompt = Prompt.from_dict(prompt_dict)
                
                # Apply filters
                if tag and tag not in prompt.tags:
                    continue
                    
                if min_score is not None and (prompt.score is None or prompt.score < min_score):
                    continue
                    
                if max_score is not None and (prompt.score is None or prompt.score > max_score):
                    continue
                
                prompts.append(prompt)
        except (json.JSONDecodeError, KeyError):
            # Skip invalid files
            continue
    
    # Sort by ID (which includes date)
    prompts.sort(key=lambda p: p.id, reverse=True)
    
    return prompts