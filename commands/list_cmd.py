# ABOUTME: Command module for listing and filtering prompts in PromptReflex.
# ABOUTME: Provides functionality to view and filter saved prompt-response pairs.

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
    # Implementation will be filled in later
    pass