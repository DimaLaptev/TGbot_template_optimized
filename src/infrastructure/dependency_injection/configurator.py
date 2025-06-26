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
from infrastructure.database.connection import DatabaseConnection
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
    
    # Database connection
    db_connection = DatabaseConnection(settings)
    container.register_singleton(DatabaseConnection, db_connection)
    
    # Infrastructure layer - Repository implementations
    user_repo_impl = UserRepositoryImpl(db_connection)
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


def get_database_connection() -> DatabaseConnection:
    """Получить подключение к базе данных из DI контейнера."""
    return container.get(DatabaseConnection) 