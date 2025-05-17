# ABOUTME: Main entry point for PromptReflex CLI tool.
# ABOUTME: Defines the CLI structure and commands for tracking and evaluating Claude Code prompts.

import click
import os
import sys
from commands import log_cmd, evaluate_cmd, list_cmd

# Version information
__version__ = '0.1.0'


@click.group(context_settings={"help_option_names": ["-h", "--help"]})
@click.version_option(version=__version__)
def cli():
    """PromptReflex: A tool for tracking and evaluating Claude Code prompts.
    
    This CLI tool helps prompt engineers log interactions, evaluate prompt 
    effectiveness, and build a portfolio of prompt-response pairs with 
    qualitative assessments.
    """
    # Ensure the application directories exist
    os.makedirs(os.path.expanduser("~/.promptreflex"), exist_ok=True)


cli.add_command(log_cmd.log)
cli.add_command(evaluate_cmd.evaluate)
cli.add_command(list_cmd.list_prompts)


if __name__ == "__main__":
    cli()