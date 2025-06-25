"""
Контроллер Telegram бота.
"""
from typing import Optional

from application.interfaces.user_service import UserService
from application.dtos.user_dto import CreateUserDto, UserProfileDto
from infrastructure.dependency_injection.configurator import get_user_service


class TelegramBotController:
    """
    Контроллер для обработки команд Telegram бота.
    
    Использует Dependency Injection для получения сервисов,
    не зависит от конкретных реализаций.
    """
    
    def __init__(self) -> None:
        # Получаем сервис через DI
        self._user_service: UserService = get_user_service()
    
    async def handle_start_command(self, user_id: int, username: Optional[str]) -> str:
        """
        Обработать команду /start.
        
        Регистрирует пользователя, если он новый.
        """
        try:
            # Проверяем, существует ли пользователь
            if await self._user_service.user_exists(user_id):
                return "Добро пожаловать обратно! 🎉"
            
            # Регистрируем нового пользователя
            create_dto = CreateUserDto(user_id=user_id, username=username)
            user_dto = await self._user_service.register_user(create_dto)
            
            return f"Добро пожаловать в игру, {user_dto.display_name}! 🚀"
            
        except Exception as e:
            return f"Ошибка при регистрации: {str(e)}"
    
    async def handle_tap_button(self, user_id: int) -> str:
        """Обработать нажатие на кнопку."""
        try:
            user_dto = await self._user_service.increment_taps(user_id)
            
            if user_dto is None:
                return "Пользователь не найден. Используйте /start"
            
            return f"Нажатий: {user_dto.taps} 🎯"
            
        except Exception as e:
            return f"Ошибка при нажатии: {str(e)}"
    
    async def handle_update_profile(
        self, 
        user_id: int, 
        name: str, 
        info: str, 
        photo_id: Optional[str] = None
    ) -> str:
        """Обработать обновление профиля."""
        try:
            profile_dto = UserProfileDto(name=name, info=info, photo_id=photo_id)
            user_dto = await self._user_service.update_profile(user_id, profile_dto)
            
            if user_dto is None:
                return "Пользователь не найден. Используйте /start"
            
            return "Профиль успешно обновлен! ✅"
            
        except ValueError as e:
            return f"Ошибка валидации: {str(e)}"
        except Exception as e:
            return f"Ошибка при обновлении профиля: {str(e)}"
    
    async def handle_leaderboard_command(self, user_id: int) -> str:
        """Обработать команду рейтинга."""
        try:
            leaderboard = await self._user_service.get_leaderboard()
            
            if leaderboard.is_empty:
                return "Рейтинг пуст. Станьте первым!"
            
            # Формируем сообщение с топом
            message_lines = ["🏆 Топ игроков:", ""]
            
            for entry in leaderboard.entries[:10]:  # Показываем топ-10
                user = entry.user
                emoji = "🥇" if entry.position == 1 else "🥈" if entry.position == 2 else "🥉" if entry.position == 3 else "🔸"
                message_lines.append(
                    f"{emoji} {entry.position}. {user.display_name} - {user.taps} нажатий"
                )
            
            message_lines.extend(["", f"Общее количество нажатий: {leaderboard.total_taps}"])
            
            return "\n".join(message_lines)
            
        except Exception as e:
            return f"Ошибка при получении рейтинга: {str(e)}" 