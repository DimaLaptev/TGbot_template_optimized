"""User ID value object."""
from dataclasses import dataclass


@dataclass(frozen=True)
class UserId:
    """User identifier value object."""
    
    value: int
    
    def __post_init__(self) -> None:
        """Validate user ID."""
        if self.value <= 0:
            raise ValueError("User ID must be positive")
    
    def __str__(self) -> str:
        """String representation."""
        return str(self.value) 