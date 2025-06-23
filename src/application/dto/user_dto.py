"""User DTOs for data transfer between layers."""
from dataclasses import dataclass
from datetime import datetime


@dataclass
class CreateUserRequest:
    """Request to create a new user."""
    
    social_id: int
    username: str | None = None


@dataclass
class UpdateUserProfileRequest:
    """Request to update user profile."""
    
    user_id: int
    name: str | None = None
    info: str | None = None
    photo_file_id: str | None = None


@dataclass
class UserResponse:
    """User data response."""
    
    id: int
    social_id: int
    username: str | None
    registration_date: datetime
    name: str | None
    info: str | None
    photo_file_id: str | None
    taps: int
    has_profile: bool
    display_name: str


@dataclass
class UserTapRequest:
    """Request to increment user taps."""
    
    social_id: int
    count: int = 1


@dataclass
class LeaderboardResponse:
    """Leaderboard data response."""
    
    total_users: int
    total_taps: int
    top_users: list[UserResponse]
    user_rank: int | None = None 