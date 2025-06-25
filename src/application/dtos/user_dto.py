"""
Data Transfer Objects для работы с пользователями.
"""
from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class UserProfileDto:
    """DTO для профиля пользователя."""
    name: str
    info: str
    photo_id: Optional[str] = None


@dataclass
class CreateUserDto:
    """DTO для создания пользователя."""
    user_id: int
    username: Optional[str]


@dataclass
class UserDto:
    """DTO для пользователя."""
    id: int
    username: Optional[str]
    registration_date: datetime
    taps: int
    profile: Optional[UserProfileDto] = None
    
    @property
    def has_profile(self) -> bool:
        """Проверить, заполнен ли профиль."""
        return self.profile is not None
    
    @property
    def display_name(self) -> str:
        """Получить отображаемое имя пользователя."""
        if self.profile and self.profile.name:
            return self.profile.name
        return self.username or f"User {self.id}" 