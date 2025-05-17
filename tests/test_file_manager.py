# ABOUTME: Test suite for the file manager utility functions in PromptReflex.
# ABOUTME: Validates the functionality for prompt file operations and ID generation.

import unittest
import json
import os
import shutil
import tempfile
from datetime import datetime, timedelta
from unittest.mock import patch
from models.prompt import Prompt
from utils.file_manager import (
    generate_id, get_prompts_dir, save_prompt, load_prompt, 
    update_prompt, get_template
)


class TestFileManager(unittest.TestCase):
    """Test suite for the file manager utility functions."""
    
    def setUp(self):
        """Set up a temporary directory for test files."""
        self.temp_dir = tempfile.mkdtemp()
        self.old_prompts_dir = os.environ.get('PROMPTREFLEX_PROMPTS_DIR')
        os.environ['PROMPTREFLEX_PROMPTS_DIR'] = self.temp_dir
        
        # Create a temporary templates directory
        self.templates_dir = os.path.join(self.temp_dir, 'templates')
        os.makedirs(self.templates_dir, exist_ok=True)
        
        # Create a test template file
        self.test_template_path = os.path.join(self.templates_dir, 'test_template.txt')
        with open(self.test_template_path, 'w') as f:
            f.write('Test template content with {{placeholder}}')
    
    def tearDown(self):
        """Clean up temporary files after tests."""
        if self.old_prompts_dir:
            os.environ['PROMPTREFLEX_PROMPTS_DIR'] = self.old_prompts_dir
        else:
            del os.environ['PROMPTREFLEX_PROMPTS_DIR']
        shutil.rmtree(self.temp_dir)
    
    def test_generate_id(self):
        """Test generating unique IDs."""
        # Test format with default date
        id1 = generate_id()
        self.assertRegex(id1, r'\d{4}-\d{2}-\d{2}-\d{3}')
        
        # Test format with specific date
        test_date = datetime(2025, 5, 17)
        id2 = generate_id(test_date)
        self.assertRegex(id2, r'2025-05-17-\d{3}')
        
        # Test uniqueness
        id3 = generate_id()
        self.assertNotEqual(id1, id3)
        
        # Test consecutive IDs on same date
        with patch('utils.file_manager.datetime') as mock_datetime:
            mock_datetime.now.return_value = test_date
            mock_datetime.side_effect = lambda *args, **kw: datetime(*args, **kw)
            
            consecutive_id1 = generate_id()
            consecutive_id2 = generate_id()
            
            # Extract counter parts
            counter1 = int(consecutive_id1.split('-')[-1])
            counter2 = int(consecutive_id2.split('-')[-1])
            
            # Verify second counter is incrementing
            self.assertEqual(counter2, counter1 + 1)
    
    def test_get_prompts_dir(self):
        """Test getting the prompts directory."""
        prompts_dir = get_prompts_dir()
        
        # Verify the directory exists
        self.assertTrue(os.path.isdir(prompts_dir))
        
        # Verify it's using our environment variable
        self.assertEqual(prompts_dir, self.temp_dir)
        
        # Test with no environment variable
        del os.environ['PROMPTREFLEX_PROMPTS_DIR']
        default_dir = get_prompts_dir()
        
        # Verify default directory is created in user's home
        self.assertTrue(os.path.isdir(default_dir))
        self.assertIn('promptreflex', default_dir.lower())
        
        # Reset for other tests
        os.environ['PROMPTREFLEX_PROMPTS_DIR'] = self.temp_dir
    
    def test_save_prompt(self):
        """Test saving a prompt to a file."""
        test_prompt = Prompt(
            id="2025-05-17-001",
            date="2025-05-17",
            prompt="Test prompt",
            response="Test response",
            tags=["test"],
            notes="Test notes"
        )
        
        # Save the prompt
        file_path = save_prompt(test_prompt)
        
        # Verify file exists
        self.assertTrue(os.path.isfile(file_path))
        
        # Verify content
        with open(file_path, 'r') as f:
            content = json.load(f)
            self.assertEqual(content["id"], "2025-05-17-001")
            self.assertEqual(content["prompt"], "Test prompt")
            self.assertEqual(content["tags"], ["test"])
    
    def test_load_prompt(self):
        """Test loading a prompt from a file."""
        # Create a test prompt file
        test_prompt = Prompt(
            id="2025-05-17-002",
            date="2025-05-17",
            prompt="Test prompt for loading",
            response="Test response for loading",
            tags=["load", "test"],
            notes="Test loading notes"
        )
        file_path = save_prompt(test_prompt)
        
        # Load the prompt
        loaded_prompt = load_prompt("2025-05-17-002")
        
        # Verify loaded content
        self.assertEqual(loaded_prompt.id, "2025-05-17-002")
        self.assertEqual(loaded_prompt.prompt, "Test prompt for loading")
        self.assertEqual(loaded_prompt.tags, ["load", "test"])
        
        # Test loading non-existent prompt
        with self.assertRaises(FileNotFoundError):
            load_prompt("non-existent-id")
    
    def test_update_prompt(self):
        """Test updating an existing prompt."""
        # Create a test prompt file
        test_prompt = Prompt(
            id="2025-05-17-003",
            date="2025-05-17",
            prompt="Original prompt",
            response="Original response",
            tags=["original"],
            notes="Original notes"
        )
        save_prompt(test_prompt)
        
        # Update the prompt
        test_prompt.notes = "Updated notes"
        test_prompt.tags = ["original", "updated"]
        test_prompt.score = 5
        
        # Save the update
        updated_path = update_prompt(test_prompt)
        
        # Load and verify update
        updated_prompt = load_prompt("2025-05-17-003")
        self.assertEqual(updated_prompt.notes, "Updated notes")
        self.assertEqual(updated_prompt.tags, ["original", "updated"])
        self.assertEqual(updated_prompt.score, 5)
        
        # Test updating non-existent prompt
        non_existent = Prompt(
            id="non-existent-id",
            date="2025-05-17",
            prompt="Non-existent prompt",
            response="Non-existent response",
            tags=[],
            notes=""
        )
        with self.assertRaises(FileNotFoundError):
            update_prompt(non_existent)
    
    def test_get_template(self):
        """Test getting a template file."""
        # Patch the template directory
        with patch('utils.file_manager.get_templates_dir', return_value=self.templates_dir):
            # Load the test template
            template_content = get_template('test_template.txt')
            self.assertEqual(template_content, 'Test template content with {{placeholder}}')
            
            # Test loading non-existent template
            with self.assertRaises(FileNotFoundError):
                get_template('non_existent_template.txt')


if __name__ == "__main__":
    unittest.main()