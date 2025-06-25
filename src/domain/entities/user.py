"""
Доменная сущность User - основной объект предметной области.
"""
from datetime import datetime
from typing import Optional
from dataclasses import dataclass

from domain.value_objects.user_id import UserId
from domain.value_objects.username import Username
from domain.value_objects.user_profile import UserProfile


@dataclass
class User:
    """
    Доменная сущность пользователя.
    
    Инкапсулирует бизнес-логику работы с пользователем,
    не зависит от инфраструктурных деталей.
    """
    id: UserId
    username: Username
    registration_date: datetime
    taps: int = 0
    profile: Optional[UserProfile] = None
    
    def increment_taps(self) -> None:
        """Увеличить количество нажатий на кнопку."""
        self.taps += 1
    
    def update_profile(self, profile: UserProfile) -> None:
        """Обновить профиль пользователя."""
        self.profile = profile
    
    def has_profile(self) -> bool:
        """Проверить, заполнен ли профиль пользователя."""
        return self.profile is not None
    
    @classmethod
    def create_new(cls, user_id: UserId, username: Username) -> "User":
        """Создать нового пользователя."""
        return cls(
            id=user_id,
            username=username,
            registration_date=datetime.now(),
            taps=0,
            profile=None
        ) 