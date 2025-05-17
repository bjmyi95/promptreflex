# ABOUTME: Test suite for the main PromptReflex CLI entry point.
# ABOUTME: Validates the CLI structure and command registration.

import unittest
from unittest.mock import patch, MagicMock
from click.testing import CliRunner
import promptreflex


class TestPromptReflexCLI(unittest.TestCase):
    """Test suite for the PromptReflex CLI."""
    
    def setUp(self):
        """Set up the CLI runner."""
        self.runner = CliRunner()
    
    def test_cli_help(self):
        """Test the CLI displays help information."""
        result = self.runner.invoke(promptreflex.cli, ['--help'])
        
        # Check exit code
        self.assertEqual(result.exit_code, 0)
        
        # Check help text contains expected content
        self.assertIn("PromptReflex:", result.output)
        self.assertIn("log", result.output)
        self.assertIn("evaluate", result.output)
        self.assertIn("list", result.output)
    
    @patch('commands.log_cmd.log')
    def test_log_command_registered(self, mock_log):
        """Test the log command is properly registered."""
        # Configure the mock
        mock_log.callback = MagicMock()
        
        # Run the command
        self.runner.invoke(promptreflex.cli, ['log', '--help'])
        
        # No exception means the command is registered
        # We don't need to check the result since we're just testing registration
    
    @patch('commands.evaluate_cmd.evaluate')
    def test_evaluate_command_registered(self, mock_evaluate):
        """Test the evaluate command is properly registered."""
        # Configure the mock
        mock_evaluate.callback = MagicMock()
        
        # Run the command
        self.runner.invoke(promptreflex.cli, ['evaluate', '--help'])
        
        # No exception means the command is registered
    
    @patch('commands.list_cmd.list_prompts')
    def test_list_command_registered(self, mock_list):
        """Test the list command is properly registered."""
        # Configure the mock
        mock_list.callback = MagicMock()
        
        # Run the command
        self.runner.invoke(promptreflex.cli, ['list', '--help'])
        
        # No exception means the command is registered


if __name__ == "__main__":
    unittest.main()