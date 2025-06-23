"""Social ID value object."""
from dataclasses import dataclass


@dataclass(frozen=True)
class SocialId:
    """Social media identifier value object (e.g., Telegram user ID)."""
    
    value: int
    
    def __post_init__(self) -> None:
        """Validate social ID."""
        if self.value <= 0:
            raise ValueError("Social ID must be positive")
    
    def __str__(self) -> str:
        """String representation."""
        return str(self.value) 