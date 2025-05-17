# ABOUTME: Test suite for the log command in PromptReflex.
# ABOUTME: Validates the functionality for logging prompts and responses.

import unittest
import os
import json
import tempfile
import shutil
from unittest.mock import patch, MagicMock
from click.testing import CliRunner
from commands.log_cmd import log
from models.prompt import Prompt


class TestLogCommand(unittest.TestCase):
    """Test suite for the log command."""
    
    def setUp(self):
        """Set up a temporary directory for test files."""
        self.temp_dir = tempfile.mkdtemp()
        self.old_prompts_dir = os.environ.get('PROMPTREFLEX_PROMPTS_DIR')
        os.environ['PROMPTREFLEX_PROMPTS_DIR'] = self.temp_dir
        self.runner = CliRunner()
    
    def tearDown(self):
        """Clean up temporary files after tests."""
        if self.old_prompts_dir:
            os.environ['PROMPTREFLEX_PROMPTS_DIR'] = self.old_prompts_dir
        else:
            del os.environ['PROMPTREFLEX_PROMPTS_DIR']
        shutil.rmtree(self.temp_dir)
    
    @patch('commands.log_cmd.generate_id')
    def test_log_command_basic(self, mock_generate_id):
        """Test basic log command functionality."""
        mock_generate_id.return_value = "2025-05-17-001"
        
        # Run the command
        result = self.runner.invoke(log, [
            '--prompt', 'Test prompt',
            '--response', 'Test response'
        ])
        
        # Check exit code
        self.assertEqual(result.exit_code, 0)
        
        # Check output
        self.assertIn("Prompt logged with ID: 2025-05-17-001", result.output)
        
        # Verify file was created
        file_path = os.path.join(self.temp_dir, "2025-05-17-001.json")
        self.assertTrue(os.path.isfile(file_path))
        
        # Verify file contents
        with open(file_path, 'r') as f:
            content = json.load(f)
            self.assertEqual(content["prompt"], "Test prompt")
            self.assertEqual(content["response"], "Test response")
            self.assertEqual(content["tags"], [])
            self.assertEqual(content["notes"], "")
    
    @patch('commands.log_cmd.generate_id')
    def test_log_command_with_tags_and_notes(self, mock_generate_id):
        """Test log command with tags and notes."""
        mock_generate_id.return_value = "2025-05-17-002"
        
        # Run the command
        result = self.runner.invoke(log, [
            '--prompt', 'Test prompt with tags',
            '--response', 'Test response with tags',
            '--tags', 'tag1', '--tags', 'tag2',
            '--notes', 'Test notes'
        ])
        
        # Check exit code
        self.assertEqual(result.exit_code, 0)
        
        # Verify file contents
        file_path = os.path.join(self.temp_dir, "2025-05-17-002.json")
        with open(file_path, 'r') as f:
            content = json.load(f)
            self.assertEqual(content["tags"], ["tag1", "tag2"])
            self.assertEqual(content["notes"], "Test notes")
    
    def test_log_command_missing_required(self):
        """Test log command with missing required parameters."""
        # Test missing prompt
        result = self.runner.invoke(log, [
            '--response', 'Test response'
        ])
        self.assertNotEqual(result.exit_code, 0)
        
        # Test missing response
        result = self.runner.invoke(log, [
            '--prompt', 'Test prompt'
        ])
        self.assertNotEqual(result.exit_code, 0)
    
    @patch('commands.log_cmd.save_prompt')
    def test_log_command_file_error(self, mock_save_prompt):
        """Test log command handling file errors."""
        # Mock save_prompt to raise an exception
        mock_save_prompt.side_effect = IOError("Test file error")
        
        # Run the command
        result = self.runner.invoke(log, [
            '--prompt', 'Test prompt',
            '--response', 'Test response'
        ])
        
        # Check error is handled
        self.assertNotEqual(result.exit_code, 0)
        self.assertIn("Error saving prompt", result.output)
    
    @patch('commands.log_cmd.datetime')
    @patch('commands.log_cmd.generate_id')
    def test_log_command_date_format(self, mock_generate_id, mock_datetime):
        """Test log command correctly formats the date."""
        # Mock the current date
        mock_datetime.now.return_value.strftime.return_value = "2025-05-17"
        mock_generate_id.return_value = "2025-05-17-003"
        
        # Run the command
        self.runner.invoke(log, [
            '--prompt', 'Test prompt',
            '--response', 'Test response'
        ])
        
        # Verify file contents
        file_path = os.path.join(self.temp_dir, "2025-05-17-003.json")
        with open(file_path, 'r') as f:
            content = json.load(f)
            self.assertEqual(content["date"], "2025-05-17")


if __name__ == "__main__":
    unittest.main()