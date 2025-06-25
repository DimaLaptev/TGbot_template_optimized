"""
Упрощенная демонстрация архитектуры без внешних зависимостей.
"""
import asyncio


async def main() -> None:
    """
    Демонстрация принципов Clean Architecture и SOLID.
    """
    print("🏗️  Демонстрация Clean Architecture + SOLID")
    print("=" * 50)
    
    # Демонстрация доменных объектов
    print("\n1. 🏛️  ДОМЕННЫЙ СЛОЙ")
    print("   📦 Value Objects:")
    
    try:
        from domain.value_objects.user_id import UserId
        from domain.value_objects.username import Username
        from domain.value_objects.user_profile import UserProfile
        
        # Создаем доменные объекты
        user_id = UserId(12345)
        username = Username("test_user")
        profile = UserProfile("Тестовый Пользователь", "Описание тестового пользователя")
        
        print(f"   ✅ UserId: {user_id}")
        print(f"   ✅ Username: {username}")
        print(f"   ✅ UserProfile: {profile.name}")
        
    except Exception as e:
        print(f"   ❌ Ошибка в доменных объектах: {e}")
    
    print("\n   🧩 Entities:")
    try:
        from domain.entities.user import User
        
        # Создаем доменную сущность
        user = User.create_new(user_id, username)
        user.update_profile(profile)
        user.increment_taps()
        user.increment_taps()
        
        print(f"   ✅ User Entity: {user.username.value}, taps: {user.taps}")
        print(f"   ✅ Has profile: {user.has_profile()}")
        
    except Exception as e:
        print(f"   ❌ Ошибка в сущностях: {e}")
    
    print("\n2. 🎯 ПРИКЛАДНОЙ СЛОЙ")
    print("   📋 DTOs:")
    
    try:
        from application.dtos.user_dto import UserDto, CreateUserDto
        
        # Создаем DTO
        create_dto = CreateUserDto(user_id=12345, username="test_user")
        user_dto = UserDto(
            id=12345,
            username="test_user",
            registration_date=user.registration_date,
            taps=2
        )
        
        print(f"   ✅ CreateUserDto: user_id={create_dto.user_id}")
        print(f"   ✅ UserDto: {user_dto.display_name}, taps={user_dto.taps}")
        
    except Exception as e:
        print(f"   ❌ Ошибка в DTOs: {e}")
    
    print("\n3. 🔧 ИНФРАСТРУКТУРНЫЙ СЛОЙ")
    print("   🏗️  Dependency Injection:")
    
    try:
        from infrastructure.dependency_injection.container import DIContainer
        
        # Демонстрация DI контейнера
        container = DIContainer()
        
        # Регистрируем тестовый сервис
        class TestService:
            def get_name(self):
                return "Test Service"
        
        container.register_singleton(TestService, TestService())
        service = container.get(TestService)
        
        print(f"   ✅ DI Container работает: {service.get_name()}")
        
    except Exception as e:
        print(f"   ❌ Ошибка в DI: {e}")
    
    print("\n" + "=" * 50)
    print("🎯 ПРИНЦИПЫ SOLID РЕАЛИЗОВАНЫ:")
    print("   ✅ Single Responsibility - каждый класс имеет одну ответственность")
    print("   ✅ Open/Closed - открыты для расширения, закрыты для модификации")
    print("   ✅ Liskov Substitution - подтипы заменяемы базовыми типами")
    print("   ✅ Interface Segregation - интерфейсы разделены по назначению")
    print("   ✅ Dependency Inversion - зависимость от абстракций, не деталей")
    
    print("\n🏛️  CLEAN ARCHITECTURE СТРУКТУРА:")
    print("   Domain ← Application ← Infrastructure")
    print("                ↑")
    print("            Interfaces")
    
    print("\n💡 СЛЕДУЮЩИЕ ШАГИ:")
    print("   🔄 Реализовать SQLAlchemy репозитории")
    print("   🔄 Добавить Unit of Work паттерн")
    print("   🔄 Создать e2e тесты")
    print("   🔄 Добавить FastAPI и CLI интерфейсы")


if __name__ == "__main__":
    asyncio.run(main()) 