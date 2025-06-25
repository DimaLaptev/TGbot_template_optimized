"""
Value Object для идентификатора пользователя.
"""
from dataclasses import dataclass


@dataclass(frozen=True)
class UserId:
    """
    Объект-значение для идентификатора пользователя в Telegram.
    
    Обеспечивает типобезопасность и валидацию.
    """
    value: int
    
    def __post_init__(self) -> None:
        if self.value <= 0:
            raise ValueError("User ID должен быть положительным числом")
    
    def __str__(self) -> str:
        return str(self.value)
    
    def __int__(self) -> int:
        return self.value 