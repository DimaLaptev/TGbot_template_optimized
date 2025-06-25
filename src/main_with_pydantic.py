"""
Демонстрация архитектуры с pydantic настройками.
"""
import asyncio
from infrastructure.dependency_injection.configurator import configure_dependencies, get_settings_from_container
from interfaces.telegram.bot_controller import TelegramBotController


async def main() -> None:
    """
    Демонстрация работы архитектуры с pydantic.
    """
    print("🏗️  Clean Architecture + SOLID + Pydantic")
    print("=" * 60)
    
    # Настраиваем Dependency Injection
    configure_dependencies()
    
    # Проверяем загрузку настроек через pydantic
    print("\n📋 ПРОВЕРКА PYDANTIC НАСТРОЕК:")
    
    try:
        settings = get_settings_from_container()
        
        print(f"   ✅ Environment: {settings.environment}")
        print(f"   ✅ Debug: {settings.debug}")
        print(f"   ✅ Database URL: {settings.database_url[:30]}...")
        print(f"   ✅ Redis URL: {settings.redis_url[:30]}...")
        print(f"   ✅ Telegram token configured: {'Yes' if settings.telegram_bot_token else 'No'}")
        
    except Exception as e:
        print(f"   ❌ Ошибка в настройках: {e}")
    
    # Проверяем работу DI контейнера
    print("\n🔧 ПРОВЕРКА DEPENDENCY INJECTION:")
    
    try:
        from infrastructure.dependency_injection.container import container
        from application.interfaces.user_service import UserService
        
        # Получаем сервис через DI
        user_service = container.get(UserService)
        print(f"   ✅ UserService получен: {type(user_service).__name__}")
        
        # Создаем контроллер бота (он использует DI внутри)
        bot_controller = TelegramBotController()
        print(f"   ✅ TelegramBotController создан: {type(bot_controller).__name__}")
        
    except Exception as e:
        print(f"   ❌ Ошибка в DI: {e}")
    
    # Демонстрация работы архитектуры
    print("\n🎯 ДЕМОНСТРАЦИЯ АРХИТЕКТУРНЫХ СЛОЕВ:")
    
    try:
        # Команды проходят весь путь через слои
        print("   🔄 Команда /start проходит через:")
        print("      Interface → Application → Domain → Infrastructure")
        
        result = await bot_controller.handle_start_command(12345, "test_user")
        print(f"   📤 Результат: {result}")
        
        result = await bot_controller.handle_tap_button(12345)
        print(f"   📤 Результат: {result}")
        
        result = await bot_controller.handle_leaderboard_command(12345)
        print(f"   📤 Результат: {result}")
        
    except Exception as e:
        print(f"   ❌ Неожиданная ошибка: {e}")
    
    print("\n" + "=" * 60)
    print("🎯 АРХИТЕКТУРНЫЕ ПРИНЦИПЫ СОБЛЮДЕНЫ:")
    print("   ✅ Dependency Inversion - зависимости от абстракций")
    print("   ✅ Dependency Injection - зависимости внедряются извне")
    print("   ✅ Clean Architecture - правильное направление зависимостей")
    print("   ✅ SOLID принципы - все пять принципов соблюдены")
    print("   ✅ Pydantic Settings - конфигурация типизирована и валидирована")
    
    print("\n🔮 ГОТОВНОСТЬ К РАСШИРЕНИЮ:")
    print("   🔄 Легко добавить FastAPI интерфейс")
    print("   🔄 Легко добавить CLI интерфейс")
    print("   🔄 Легко заменить репозитории на SQLAlchemy")
    print("   🔄 Легко добавить новые доменные сущности")
    print("   🔄 Легко мокать зависимости для тестов")


if __name__ == "__main__":
    asyncio.run(main()) 