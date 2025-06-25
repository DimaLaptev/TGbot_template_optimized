"""
Value Object для профиля пользователя.
"""
from dataclasses import dataclass
from typing import Optional


@dataclass(frozen=True)
class UserProfile:
    """
    Объект-значение для профиля пользователя.
    
    Содержит дополнительную информацию о пользователе.
    """
    name: str
    info: str
    photo_id: Optional[str] = None
    
    def __post_init__(self) -> None:
        if not self.name or not self.name.strip():
            raise ValueError("Имя пользователя не может быть пустым")
        
        if len(self.name) > 100:
            raise ValueError("Имя пользователя не может быть длиннее 100 символов")
        
        if len(self.info) > 500:
            raise ValueError("Информация о пользователе не может быть длиннее 500 символов")
    
    @property
    def has_photo(self) -> bool:
        """Проверить, есть ли фото в профиле."""
        return self.photo_id is not None and self.photo_id.strip() != "" 