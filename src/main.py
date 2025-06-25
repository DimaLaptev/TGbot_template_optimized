"""
Основная точка входа приложения.
"""
import asyncio
from infrastructure.dependency_injection.configurator import configure_dependencies
from interfaces.telegram.bot_controller import TelegramBotController


async def main() -> None:
    """
    Главная функция приложения.
    
    Демонстрирует работу чистой архитектуры с DI.
    """
    # Настраиваем Dependency Injection
    configure_dependencies()
    
    # Создаем контроллер бота (он получает зависимости через DI)
    bot_controller = TelegramBotController()
    
    # Демонстрация работы архитектуры
    print("🏗️  Архитектура настроена!")
    print("📋 Демонстрация работы слоев:")
    
    try:
        # Симуляция команды /start
        result = await bot_controller.handle_start_command(12345, "test_user")
        print(f"✅ /start: {result}")
        
        # Симуляция нажатия кнопки
        result = await bot_controller.handle_tap_button(12345)
        print(f"✅ Tap: {result}")
        
        # Симуляция рейтинга
        result = await bot_controller.handle_leaderboard_command(12345)
        print(f"✅ Leaderboard: {result}")
        
    except NotImplementedError as e:
        print(f"⚠️  Ожидаемая ошибка (заглушки): {e}")
        print("💡 Это нормально - репозиторий еще не реализован")
    except Exception as e:
        print(f"❌ Неожиданная ошибка: {e}")
    
    print("\n🎯 Архитектурные принципы реализованы:")
    print("   ✅ Dependency Inversion (абстракции не зависят от деталей)")
    print("   ✅ Dependency Injection (зависимости внедряются извне)")
    print("   ✅ Separation of Concerns (четкое разделение ответственности)")
    print("   ✅ Clean Architecture (слои не зависят от внешних деталей)")


if __name__ == "__main__":
    asyncio.run(main()) 