# ABOUTME: Test suite for the Prompt data model in PromptReflex.
# ABOUTME: Validates the functionality of the Prompt class for storing and managing prompt data.

import unittest
from datetime import datetime
import pytest
from models.prompt import Prompt


class TestPromptModel(unittest.TestCase):
    """Test suite for the Prompt model class."""
    
    def test_create_prompt(self):
        """Test creating a valid Prompt object."""
        prompt = Prompt(
            id="2025-05-17-001",
            date="2025-05-17",
            prompt="Write a Python function that checks if a string is a palindrome.",
            response="def is_palindrome(s): return s == s[::-1]",
            tags=["python", "string", "function"],
            notes="Very clean response, good use of slicing."
        )
        
        self.assertEqual(prompt.id, "2025-05-17-001")
        self.assertEqual(prompt.date, "2025-05-17")
        self.assertEqual(prompt.prompt, "Write a Python function that checks if a string is a palindrome.")
        self.assertEqual(prompt.response, "def is_palindrome(s): return s == s[::-1]")
        self.assertEqual(prompt.tags, ["python", "string", "function"])
        self.assertEqual(prompt.notes, "Very clean response, good use of slicing.")
        self.assertIsNone(prompt.evaluation_prompt)
        self.assertIsNone(prompt.evaluation_response)
        self.assertIsNone(prompt.score)
    
    def test_invalid_score(self):
        """Test that an invalid score raises a ValueError."""
        with self.assertRaises(ValueError):
            Prompt(
                id="2025-05-17-001",
                date="2025-05-17",
                prompt="Test prompt",
                response="Test response",
                tags=[],
                notes="",
                score=6  # Invalid score
            )
            
        with self.assertRaises(ValueError):
            Prompt(
                id="2025-05-17-001",
                date="2025-05-17",
                prompt="Test prompt",
                response="Test response",
                tags=[],
                notes="",
                score=0  # Invalid score
            )
    
    def test_invalid_date_format(self):
        """Test that an invalid date format raises a ValueError."""
        with self.assertRaises(ValueError):
            Prompt(
                id="2025-05-17-001",
                date="05/17/2025",  # Invalid format
                prompt="Test prompt",
                response="Test response",
                tags=[],
                notes=""
            )
    
    def test_to_dict(self):
        """Test converting a Prompt object to a dictionary."""
        prompt = Prompt(
            id="2025-05-17-001",
            date="2025-05-17",
            prompt="Test prompt",
            response="Test response",
            tags=["test"],
            notes="Test notes",
            evaluation_prompt="Evaluation prompt",
            evaluation_response="Evaluation response",
            score=5
        )
        
        prompt_dict = prompt.to_dict()
        self.assertEqual(prompt_dict["id"], "2025-05-17-001")
        self.assertEqual(prompt_dict["date"], "2025-05-17")
        self.assertEqual(prompt_dict["prompt"], "Test prompt")
        self.assertEqual(prompt_dict["response"], "Test response")
        self.assertEqual(prompt_dict["tags"], ["test"])
        self.assertEqual(prompt_dict["notes"], "Test notes")
        self.assertEqual(prompt_dict["evaluation_prompt"], "Evaluation prompt")
        self.assertEqual(prompt_dict["evaluation_response"], "Evaluation response")
        self.assertEqual(prompt_dict["score"], 5)
    
    def test_from_dict(self):
        """Test creating a Prompt object from a dictionary."""
        prompt_dict = {
            "id": "2025-05-17-001",
            "date": "2025-05-17",
            "prompt": "Test prompt",
            "response": "Test response",
            "tags": ["test"],
            "notes": "Test notes",
            "evaluation_prompt": "Evaluation prompt",
            "evaluation_response": "Evaluation response",
            "score": 5
        }
        
        prompt = Prompt.from_dict(prompt_dict)
        self.assertEqual(prompt.id, "2025-05-17-001")
        self.assertEqual(prompt.date, "2025-05-17")
        self.assertEqual(prompt.prompt, "Test prompt")
        self.assertEqual(prompt.response, "Test response")
        self.assertEqual(prompt.tags, ["test"])
        self.assertEqual(prompt.notes, "Test notes")
        self.assertEqual(prompt.evaluation_prompt, "Evaluation prompt")
        self.assertEqual(prompt.evaluation_response, "Evaluation response")
        self.assertEqual(prompt.score, 5)
    
    def test_is_evaluated(self):
        """Test checking if a prompt has been evaluated."""
        # Prompt without evaluation
        prompt1 = Prompt(
            id="2025-05-17-001",
            date="2025-05-17",
            prompt="Test prompt",
            response="Test response",
            tags=[],
            notes=""
        )
        self.assertFalse(prompt1.is_evaluated())
        
        # Prompt with evaluation
        prompt2 = Prompt(
            id="2025-05-17-001",
            date="2025-05-17",
            prompt="Test prompt",
            response="Test response",
            tags=[],
            notes="",
            score=4
        )
        self.assertTrue(prompt2.is_evaluated())
    
    def test_update_evaluation(self):
        """Test updating the evaluation data for a prompt."""
        prompt = Prompt(
            id="2025-05-17-001",
            date="2025-05-17",
            prompt="Test prompt",
            response="Test response",
            tags=[],
            notes=""
        )
        
        prompt.update_evaluation(
            evaluation_prompt="Evaluation prompt",
            evaluation_response="Evaluation response",
            score=4
        )
        
        self.assertEqual(prompt.evaluation_prompt, "Evaluation prompt")
        self.assertEqual(prompt.evaluation_response, "Evaluation response")
        self.assertEqual(prompt.score, 4)
        
        # Test updating with invalid score
        with self.assertRaises(ValueError):
            prompt.update_evaluation(
                evaluation_prompt="Evaluation prompt",
                evaluation_response="Evaluation response",
                score=6  # Invalid score
            )


if __name__ == "__main__":
    unittest.main()