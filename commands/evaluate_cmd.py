# ABOUTME: Command module for evaluating logged prompts in PromptReflex.
# ABOUTME: Provides functionality to score and analyze prompt-response pairs.

import click
import json
import os
import string
import re
from datetime import datetime
from utils.file_manager import load_prompt, update_prompt, get_template

@click.command("evaluate")
@click.argument("prompt_id")
@click.option("--response", "-r", help="Evaluation response from Claude")
@click.option("--score", "-s", type=int, help="Score from 1-5")
@click.option("--generate-template", "-g", is_flag=True, help="Generate evaluation template only")
@click.option("--template", "-t", default="judge_prompt.txt", help="Template file to use for evaluation")
@click.option("--auto-extract-score", "-a", is_flag=True, help="Automatically extract score from response")
def evaluate(prompt_id, response, score, generate_template, template, auto_extract_score):
    """Evaluate a logged prompt by ID.
    
    This command allows you to evaluate a previously logged prompt-response pair.
    You can generate an evaluation template to send to Claude, or provide Claude's
    evaluation response and a score.
    
    The score must be an integer between 1 and 5, where:
    - 1 = Poor
    - 2 = Below Average
    - 3 = Average
    - 4 = Good
    - 5 = Excellent
    
    Examples:
        promptreflex evaluate 2025-05-17-001 --generate-template
        promptreflex evaluate 2025-05-17-001 --response "Score: 4\\nReason: Good response" --score 4
        promptreflex evaluate 2025-05-17-001 --response "Score: 4\\nReason: Good response" --auto-extract-score
    """
    try:
        # Load the prompt
        prompt = load_prompt(prompt_id)
        
        if generate_template:
            # Get the template
            try:
                template_content = get_template(template)
            except FileNotFoundError:
                raise click.BadParameter(f"Template file '{template}' not found")
            
            # Replace placeholders with actual content
            template_content = template_content.replace("{{prompt}}", prompt.prompt)
            template_content = template_content.replace("{{response}}", prompt.response)
            
            # Print the filled template
            click.echo(template_content)
            return
        
        # Validation for evaluation
        if not response:
            raise click.BadParameter("Response is required for evaluation")
        
        # If auto-extract-score is enabled, try to extract the score from the response
        if auto_extract_score:
            extracted_score = extract_score_from_response(response)
            if extracted_score:
                score = extracted_score
                click.echo(f"Auto-extracted score: {score}")
            else:
                raise click.BadParameter("Could not automatically extract score from response. Please specify a score manually.")
        
        if score is None:
            raise click.BadParameter("Score is required for evaluation")
            
        if score < 1 or score > 5:
            raise click.BadParameter("Score must be between 1 and 5")
        
        # Check if the prompt is already evaluated
        if prompt.is_evaluated():
            confirm = click.confirm(f"Prompt {prompt_id} is already evaluated with score {prompt.score}. Overwrite?")
            if not confirm:
                click.echo("Evaluation cancelled.")
                return
        
        # Generate evaluation prompt for reference
        try:
            template_content = get_template(template)
        except FileNotFoundError:
            raise click.BadParameter(f"Template file '{template}' not found")
            
        evaluation_prompt = template_content.replace("{{prompt}}", prompt.prompt)
        evaluation_prompt = evaluation_prompt.replace("{{response}}", prompt.response)
        
        # Update the prompt with evaluation data
        prompt.evaluation_prompt = evaluation_prompt
        prompt.evaluation_response = response
        prompt.score = score
        
        # Save the updated prompt
        file_path = update_prompt(prompt)
        
        click.echo(f"Prompt {prompt_id} evaluated successfully with score: {score}")
        
        # Print a score summary
        click.echo("\nEvaluation Summary:")
        click.echo(f"ID: {prompt.id}")
        click.echo(f"Date: {prompt.date}")
        click.echo(f"Score: {prompt.score}/5")
        click.echo(f"Tags: {', '.join(prompt.tags) if prompt.tags else 'None'}")
        
    except FileNotFoundError as e:
        raise click.BadParameter(f"Error: {str(e)}")
    except ValueError as e:
        raise click.BadParameter(f"Error: {str(e)}")
    except Exception as e:
        raise click.BadParameter(f"An unexpected error occurred: {str(e)}")


def extract_score_from_response(response):
    """
    Attempt to extract a score (1-5) from an evaluation response.
    
    Args:
        response (str): The evaluation response text
        
    Returns:
        int or None: The extracted score, or None if no score could be extracted
    """
    # Look for common score patterns
    patterns = [
        r"Score:\s*(\d+)",  # Score: N
        r"Rating:\s*(\d+)",  # Rating: N
        r"^(\d+)\s*\/\s*5",  # N/5
        r"(\d+)\s*out of\s*5",  # N out of 5
    ]
    
    for pattern in patterns:
        match = re.search(pattern, response, re.IGNORECASE | re.MULTILINE)
        if match:
            try:
                score = int(match.group(1))
                if 1 <= score <= 5:
                    return score
            except ValueError:
                pass
    
    return None