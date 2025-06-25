"""
Конфигуратор Dependency Injection контейнера.
"""
from .container import container

# Domain layer
from domain.repositories.user_repository import UserRepository
from domain.services.user_domain_service import UserDomainService

# Application layer
from application.interfaces.user_service import UserService
from application.services.user_service_impl import UserServiceImpl

# Infrastructure layer
from infrastructure.database.repositories.user_repository_impl import UserRepositoryImpl
from infrastructure.config.settings import AppSettings, get_settings


def configure_dependencies() -> None:
    """
    Настроить все зависимости в DI контейнере.
    
    Здесь происходит связывание абстракций с их реализациями,
    что обеспечивает выполнение принципа Dependency Inversion.
    """
    
    # Настройки приложения
    settings = get_settings()
    container.register_singleton(AppSettings, settings)
    
    # Infrastructure layer - Repository implementations
    # TODO: Заменить None на реальное подключение к БД
    database_connection = None  # Будет создаваться в зависимости от настроек
    user_repo_impl = UserRepositoryImpl(database_connection)
    container.register_singleton(UserRepository, user_repo_impl)
    
    # Domain layer - Domain services
    container.register_transient(
        UserDomainService,
        lambda: UserDomainService(container.get(UserRepository))
    )
    
    # Application layer - Application services
    container.register_transient(
        UserService,
        lambda: UserServiceImpl(container.get(UserDomainService))
    )


def get_user_service() -> UserService:
    """Получить сервис пользователей из DI контейнера."""
    return container.get(UserService)


def get_settings_from_container() -> AppSettings:
    """Получить настройки из DI контейнера."""
    return container.get(AppSettings) 