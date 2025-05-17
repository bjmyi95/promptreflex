# ABOUTME: Command module for logging prompts and responses in PromptReflex.
# ABOUTME: Provides functionality to save prompt-response pairs with tags and notes.

import click
import json
import os
import sys
from datetime import datetime
from utils.file_manager import save_prompt, generate_id
from models.prompt import Prompt


@click.command("log")
@click.option("--prompt", "-p", required=True, help="The prompt sent to Claude Code")
@click.option("--response", "-r", required=True, help="Claude Code's response")
@click.option("--tags", "-t", multiple=True, help="Tags to categorize the prompt")
@click.option("--notes", "-n", default="", help="Additional notes about the prompt or response")
def log(prompt, response, tags, notes):
    """Log a new prompt and response pair."""
    try:
        # Generate a unique ID
        prompt_id = generate_id()
        
        # Get the current date in YYYY-MM-DD format
        date = datetime.now().strftime("%Y-%m-%d")
        
        # Create the Prompt object
        prompt_obj = Prompt(
            id=prompt_id,
            date=date,
            prompt=prompt,
            response=response,
            tags=list(tags),  # Convert tuple to list
            notes=notes
        )
        
        # Save the prompt to a file
        file_path = save_prompt(prompt_obj)
        
        # Output success message
        click.echo(f"Prompt logged with ID: {prompt_id}")
        click.echo(f"Saved to: {file_path}")
        
        return prompt_id
    
    except ValueError as e:
        # Handle validation errors
        click.echo(f"Error: {str(e)}", err=True)
        sys.exit(1)
    
    except (IOError, OSError) as e:
        # Handle file I/O errors
        click.echo(f"Error saving prompt: {str(e)}", err=True)
        sys.exit(1)
    
    except Exception as e:
        # Handle unexpected errors
        click.echo(f"Unexpected error: {str(e)}", err=True)
        sys.exit(1)