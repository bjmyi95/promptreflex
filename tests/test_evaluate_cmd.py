# ABOUTME: Test suite for the evaluate command in PromptReflex.
# ABOUTME: Validates the functionality for evaluating logged prompts and responses.

import unittest
import os
import json
import tempfile
import shutil
from unittest.mock import patch, MagicMock
from click.testing import CliRunner
from commands.evaluate_cmd import evaluate, extract_score_from_response
from models.prompt import Prompt
from utils.file_manager import save_prompt


class TestEvaluateCommand(unittest.TestCase):
    """Test suite for the evaluate command."""
    
    def setUp(self):
        """Set up a temporary directory for test files."""
        self.temp_dir = tempfile.mkdtemp()
        self.old_prompts_dir = os.environ.get('PROMPTREFLEX_PROMPTS_DIR')
        os.environ['PROMPTREFLEX_PROMPTS_DIR'] = self.temp_dir
        
        # Create a templates directory for testing
        self.templates_dir = os.path.join(self.temp_dir, 'templates')
        os.makedirs(self.templates_dir, exist_ok=True)
        
        # Create a test template
        self.template_path = os.path.join(self.templates_dir, 'judge_prompt.txt')
        with open(self.template_path, 'w') as f:
            f.write('Evaluate this prompt:\n\nPROMPT:\n{{prompt}}\n\nRESPONSE:\n{{response}}\n')
        
        # Create a custom template for testing
        self.custom_template_path = os.path.join(self.templates_dir, 'custom_template.txt')
        with open(self.custom_template_path, 'w') as f:
            f.write('Custom template. PROMPT: {{prompt}}, RESPONSE: {{response}}')
        
        # Create a test prompt for evaluation
        self.test_prompt = Prompt(
            id="2025-05-17-001",
            date="2025-05-17",
            prompt="Test prompt for evaluation",
            response="Test response for evaluation",
            tags=["test"],
            notes="Test notes"
        )
        self.prompt_path = save_prompt(self.test_prompt)
        
        # Create a pre-evaluated prompt
        self.evaluated_prompt = Prompt(
            id="2025-05-17-002",
            date="2025-05-17",
            prompt="Already evaluated prompt",
            response="Already evaluated response",
            tags=["test", "evaluated"],
            notes="Test notes",
            evaluation_prompt="Evaluation prompt",
            evaluation_response="Score: 3\nReasoning: Average prompt",
            score=3
        )
        self.evaluated_prompt_path = save_prompt(self.evaluated_prompt)
        
        self.runner = CliRunner()
    
    def tearDown(self):
        """Clean up temporary files after tests."""
        if self.old_prompts_dir:
            os.environ['PROMPTREFLEX_PROMPTS_DIR'] = self.old_prompts_dir
        else:
            del os.environ['PROMPTREFLEX_PROMPTS_DIR']
        shutil.rmtree(self.temp_dir)
    
    @patch('commands.evaluate_cmd.get_template')
    def test_generate_template_flag(self, mock_get_template):
        """Test generating an evaluation template without evaluating."""
        mock_template = 'Evaluate this prompt:\n\nPROMPT:\n{{prompt}}\n\nRESPONSE:\n{{response}}\n'
        mock_get_template.return_value = mock_template
        
        # Run the command with generate_template flag
        result = self.runner.invoke(evaluate, [
            '2025-05-17-001',
            '--generate-template'
        ])
        
        # Check exit code
        self.assertEqual(result.exit_code, 0)
        
        # Check that the template was rendered correctly
        self.assertIn('Test prompt for evaluation', result.output)
        self.assertIn('Test response for evaluation', result.output)
    
    @patch('commands.evaluate_cmd.update_prompt')
    @patch('commands.evaluate_cmd.load_prompt')
    def test_evaluate_with_response_and_score(self, mock_load_prompt, mock_update_prompt):
        """Test evaluating a prompt with a response and score."""
        # Mock the load_prompt function to return our test prompt
        mock_load_prompt.return_value = self.test_prompt
        
        # Run the command
        result = self.runner.invoke(evaluate, [
            '2025-05-17-001',
            '--response', 'Score: 4\nReasoning: Good prompt and response.',
            '--score', '4'
        ])
        
        # Check exit code
        self.assertEqual(result.exit_code, 0)
        
        # Check that update_prompt was called with the right arguments
        mock_update_prompt.assert_called_once()
        updated_prompt = mock_update_prompt.call_args[0][0]
        self.assertEqual(updated_prompt.score, 4)
        self.assertEqual(updated_prompt.evaluation_response, 'Score: 4\nReasoning: Good prompt and response.')
    
    def test_evaluate_invalid_prompt_id(self):
        """Test evaluating with an invalid prompt ID."""
        result = self.runner.invoke(evaluate, [
            'non-existent-id',
            '--response', 'Test evaluation',
            '--score', '4'
        ])
        
        # Check for error
        self.assertNotEqual(result.exit_code, 0)
        self.assertIn('not found', result.output.lower())
    
    def test_evaluate_invalid_score(self):
        """Test evaluating with an invalid score."""
        result = self.runner.invoke(evaluate, [
            '2025-05-17-001',
            '--response', 'Test evaluation',
            '--score', '6'  # Invalid score, should be 1-5
        ])
        
        # Check for error
        self.assertNotEqual(result.exit_code, 0)
        self.assertIn('score must be between 1 and 5', result.output.lower())
    
    def test_evaluate_missing_response(self):
        """Test evaluating without providing a response."""
        result = self.runner.invoke(evaluate, [
            '2025-05-17-001',
            '--score', '4'
        ])
        
        # Check for error
        self.assertNotEqual(result.exit_code, 0)
        self.assertIn('response is required', result.output.lower())
    
    def test_evaluate_missing_score(self):
        """Test evaluating without providing a score."""
        result = self.runner.invoke(evaluate, [
            '2025-05-17-001',
            '--response', 'Test evaluation'
        ])
        
        # Check for error
        self.assertNotEqual(result.exit_code, 0)
        self.assertIn('score is required', result.output.lower())
    
    @patch('commands.evaluate_cmd.get_template')
    def test_custom_template(self, mock_get_template):
        """Test using a custom template for evaluation."""
        mock_template = 'Custom template. PROMPT: {{prompt}}, RESPONSE: {{response}}'
        mock_get_template.return_value = mock_template
        
        # Run the command with custom template
        result = self.runner.invoke(evaluate, [
            '2025-05-17-001',
            '--generate-template',
            '--template', 'custom_template.txt'
        ])
        
        # Check exit code
        self.assertEqual(result.exit_code, 0)
        
        # Check that the correct template was used
        self.assertIn('Custom template', result.output)
    
    def test_extract_score_from_response(self):
        """Test extracting score from different response formats."""
        # Test various score formats
        self.assertEqual(extract_score_from_response("Score: 4"), 4)
        self.assertEqual(extract_score_from_response("Rating: 5"), 5)
        self.assertEqual(extract_score_from_response("3/5"), 3)
        self.assertEqual(extract_score_from_response("I give it 2 out of 5"), 2)
        
        # Test with more complex text
        self.assertEqual(
            extract_score_from_response(
                "The prompt was good, but the response could be better.\nScore: 3\nHere's why..."
            ),
            3
        )
        
        # Test with invalid formats
        self.assertIsNone(extract_score_from_response("No score here"))
        self.assertIsNone(extract_score_from_response("Score: invalid"))
        self.assertIsNone(extract_score_from_response("Score: 6"))  # Out of range
    
    @patch('commands.evaluate_cmd.update_prompt')
    @patch('commands.evaluate_cmd.get_template')
    def test_auto_extract_score(self, mock_get_template, mock_update_prompt):
        """Test auto-extracting score from response."""
        mock_template = 'Evaluate this prompt:\n\nPROMPT:\n{{prompt}}\n\nRESPONSE:\n{{response}}\n'
        mock_get_template.return_value = mock_template
        
        # Run the command with auto-extract score
        result = self.runner.invoke(evaluate, [
            '2025-05-17-001',
            '--response', 'Score: 4\nReasoning: Good prompt and response.',
            '--auto-extract-score'
        ])
        
        # Check exit code
        self.assertEqual(result.exit_code, 0)
        
        # Check that the score was extracted
        self.assertIn('Auto-extracted score: 4', result.output)
        
        # Check that update_prompt was called with the correct score
        mock_update_prompt.assert_called_once()
        updated_prompt = mock_update_prompt.call_args[0][0]
        self.assertEqual(updated_prompt.score, 4)
    
    def test_auto_extract_score_failure(self):
        """Test auto-extract score failure."""
        # Run the command with auto-extract score but no extractable score
        result = self.runner.invoke(evaluate, [
            '2025-05-17-001',
            '--response', 'This is a response with no score.',
            '--auto-extract-score'
        ])
        
        # Check for error
        self.assertNotEqual(result.exit_code, 0)
        self.assertIn('could not automatically extract score', result.output.lower())
    
    @patch('commands.evaluate_cmd.click.confirm')
    def test_overwrite_existing_evaluation(self, mock_confirm):
        """Test overwriting an existing evaluation."""
        # Mock confirm to return True
        mock_confirm.return_value = True
        
        # Run the command to overwrite existing evaluation
        result = self.runner.invoke(evaluate, [
            '2025-05-17-002',  # ID of pre-evaluated prompt
            '--response', 'Score: 5\nNew evaluation.',
            '--score', '5'
        ])
        
        # Check exit code
        self.assertEqual(result.exit_code, 0)
        
        # Check that the prompt was updated
        updated_prompt = json.load(open(os.path.join(self.temp_dir, "2025-05-17-002.json")))
        self.assertEqual(updated_prompt["score"], 5)
        self.assertEqual(updated_prompt["evaluation_response"], 'Score: 5\nNew evaluation.')
    
    @patch('commands.evaluate_cmd.click.confirm')
    def test_cancel_overwrite(self, mock_confirm):
        """Test cancelling overwrite of existing evaluation."""
        # Mock confirm to return False
        mock_confirm.return_value = False
        
        # Run the command to attempt overwrite
        result = self.runner.invoke(evaluate, [
            '2025-05-17-002',  # ID of pre-evaluated prompt
            '--response', 'Score: 5\nNew evaluation.',
            '--score', '5'
        ])
        
        # Check exit code
        self.assertEqual(result.exit_code, 0)
        
        # Check that the prompt was not updated
        updated_prompt = json.load(open(os.path.join(self.temp_dir, "2025-05-17-002.json")))
        self.assertEqual(updated_prompt["score"], 3)  # Original score
        self.assertEqual(updated_prompt["evaluation_response"], 'Score: 3\nReasoning: Average prompt')


if __name__ == "__main__":
    unittest.main()