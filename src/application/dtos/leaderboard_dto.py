"""
DTO для рейтинга пользователей.
"""
from dataclasses import dataclass
from typing import List

from application.dtos.user_dto import UserDto


@dataclass
class LeaderboardEntryDto:
    """Запись в рейтинге."""
    position: int
    user: UserDto


@dataclass
class LeaderboardDto:
    """DTO для рейтинга пользователей."""
    entries: List[LeaderboardEntryDto]
    total_taps: int
    
    @property
    def top_user(self) -> UserDto | None:
        """Получить лучшего пользователя."""
        if not self.entries:
            return None
        return self.entries[0].user
    
    @property
    def is_empty(self) -> bool:
        """Проверить, пуст ли рейтинг."""
        return len(self.entries) == 0 