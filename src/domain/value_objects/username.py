"""
Value Object для имени пользователя в Telegram.
"""
from dataclasses import dataclass
from typing import Optional
import re


@dataclass(frozen=True)
class Username:
    """
    Объект-значение для имени пользователя в Telegram.
    
    Обеспечивает валидацию формата username.
    """
    value: Optional[str]
    
    def __post_init__(self) -> None:
        if self.value is not None:
            if not self._is_valid_username(self.value):
                raise ValueError(f"Некорректный формат username: {self.value}")
    
    @staticmethod
    def _is_valid_username(username: str) -> bool:
        """Проверить валидность username согласно правилам Telegram."""
        if len(username) < 5 or len(username) > 32:
            return False
        # Username может содержать только латинские буквы, цифры и подчеркивания
        pattern = r'^[a-zA-Z][a-zA-Z0-9_]*[a-zA-Z0-9]$'
        return bool(re.match(pattern, username))
    
    def __str__(self) -> str:
        return self.value or "no_username"
    
    @property
    def is_empty(self) -> bool:
        """Проверить, пустое ли имя пользователя."""
        return self.value is None 