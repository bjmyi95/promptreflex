# ABOUTME: Data model for storing prompt and response information in PromptReflex.
# ABOUTME: Defines the structure for prompt-response pairs and evaluation data.

from dataclasses import dataclass, asdict
from datetime import datetime
from typing import List, Optional, Dict, Any


@dataclass
class Prompt:
    """
    Data model for a prompt-response pair with evaluation metadata.
    
    Attributes:
        id: Unique identifier for the prompt (format: YYYY-MM-DD-NNN)
        date: The date the prompt was created (format: YYYY-MM-DD)
        prompt: The text of the prompt sent to Claude Code
        response: Claude Code's response to the prompt
        tags: List of tags to categorize the prompt
        notes: Additional notes about the prompt or response
        evaluation_prompt: The prompt used to evaluate this prompt-response pair
        evaluation_response: The evaluation response from Claude
        score: Evaluation score (1-5)
    """
    id: str
    date: str
    prompt: str
    response: str
    tags: List[str]
    notes: str
    evaluation_prompt: Optional[str] = None
    evaluation_response: Optional[str] = None
    score: Optional[int] = None
    
    def __post_init__(self):
        """Validate the prompt data after initialization."""
        # Validate score range if provided
        if self.score is not None and (self.score < 1 or self.score > 5):
            raise ValueError("Score must be between 1 and 5")
            
        # Ensure date format is YYYY-MM-DD
        try:
            if self.date:
                datetime.strptime(self.date, "%Y-%m-%d")
        except ValueError:
            raise ValueError("Date must be in format YYYY-MM-DD")
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert the prompt object to a dictionary for JSON serialization."""
        return asdict(self)
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Prompt':
        """
        Create a Prompt object from a dictionary.
        
        Args:
            data: Dictionary containing prompt data
            
        Returns:
            A new Prompt object
        """
        return cls(**data)
        
    def is_evaluated(self) -> bool:
        """Check if the prompt has been evaluated."""
        return self.score is not None
        
    def update_evaluation(self, evaluation_prompt: str, 
                        evaluation_response: str, score: int) -> None:
        """
        Update the evaluation data for this prompt.
        
        Args:
            evaluation_prompt: The prompt used for evaluation
            evaluation_response: The evaluation response
            score: The score given (1-5)
            
        Raises:
            ValueError: If the score is not between 1 and 5
        """
        if score < 1 or score > 5:
            raise ValueError("Score must be between 1 and 5")
            
        self.evaluation_prompt = evaluation_prompt
        self.evaluation_response = evaluation_response
        self.score = score