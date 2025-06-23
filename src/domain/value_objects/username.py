"""Username value object."""
import re
from dataclasses import dataclass


@dataclass(frozen=True)
class Username:
    """Username value object with validation."""
    
    value: str
    
    def __post_init__(self) -> None:
        """Validate username."""
        if not self.value:
            raise ValueError("Username cannot be empty")
        
        if len(self.value) > 32:
            raise ValueError("Username too long (max 32 characters)")
        
        # Telegram username pattern
        if not re.match(r"^[a-zA-Z0-9_]+$", self.value):
            raise ValueError("Username can only contain letters, numbers, and underscores")
    
    def __str__(self) -> str:
        """String representation."""
        return self.value 