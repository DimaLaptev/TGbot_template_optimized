"""User domain entity."""
from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import TYPE_CHECKING

from ..value_objects.user_id import UserId
from ..value_objects.username import Username

if TYPE_CHECKING:
    from ..value_objects.social_id import SocialId


@dataclass
class User:
    """User domain entity.
    
    Represents a user in the system with their profile information
    and game statistics.
    """
    
    id: UserId
    social_id: SocialId
    username: Username | None
    registration_date: datetime
    name: str | None = None
    info: str | None = None
    photo_file_id: str | None = None
    taps: int = 0
    
    def __post_init__(self) -> None:
        """Validate entity state after initialization."""
        if self.taps < 0:
            raise ValueError("Taps count cannot be negative")
    
    def update_profile(
        self,
        *,
        name: str | None = None,
        info: str | None = None,
        photo_file_id: str | None = None,
    ) -> None:
        """Update user profile information.
        
        Args:
            name: User's display name
            info: User's bio/description
            photo_file_id: Telegram file ID for user's photo
        """
        if name is not None:
            self.name = name.strip() if name else None
        if info is not None:
            self.info = info.strip() if info else None
        if photo_file_id is not None:
            self.photo_file_id = photo_file_id
    
    def increment_taps(self, count: int = 1) -> None:
        """Increment user's tap count.
        
        Args:
            count: Number of taps to add (default: 1)
            
        Raises:
            ValueError: If count is negative
        """
        if count < 0:
            raise ValueError("Tap count increment cannot be negative")
        self.taps += count
    
    def reset_taps(self) -> None:
        """Reset user's tap count to zero."""
        self.taps = 0
    
    @property
    def has_profile(self) -> bool:
        """Check if user has completed their profile."""
        return bool(self.name and self.info and self.photo_file_id)
    
    @property
    def display_name(self) -> str:
        """Get user's display name or fallback to username."""
        if self.name:
            return self.name
        if self.username:
            return self.username.value
        return f"User{self.social_id.value}" 