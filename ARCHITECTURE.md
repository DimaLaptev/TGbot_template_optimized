# Архитектура проекта

## Обзор

Проект реорганизован по принципам **Clean Architecture** (Чистая архитектура) с акцентом на **SOLID принципы**, особенно **Dependency Inversion** и **Dependency Injection**.

## Структура проекта

```
src/
├── domain/                     # 🏛️ ДОМЕННЫЙ СЛОЙ
│   ├── entities/              # Доменные сущности
│   │   └── user.py           # Сущность пользователя
│   ├── value_objects/         # Объекты-значения
│   │   ├── user_id.py        # ID пользователя
│   │   ├── username.py       # Имя пользователя
│   │   └── user_profile.py   # Профиль пользователя
│   ├── repositories/          # Абстракции репозиториев
│   │   └── user_repository.py # Интерфейс репозитория
│   └── services/              # Доменные сервисы
│       └── user_domain_service.py # Бизнес-логика
│
├── application/               # 🎯 ПРИКЛАДНОЙ СЛОЙ
│   ├── interfaces/            # Интерфейсы сервисов
│   │   └── user_service.py   # Интерфейс сервиса пользователей
│   ├── services/              # Реализации сервисов
│   │   └── user_service_impl.py # Реализация сервиса
│   └── dtos/                  # Data Transfer Objects
│       ├── user_dto.py       # DTO пользователя
│       └── leaderboard_dto.py # DTO рейтинга
│
├── infrastructure/            # 🔧 ИНФРАСТРУКТУРНЫЙ СЛОЙ
│   ├── database/              # Работа с БД
│   │   └── repositories/      # Реализации репозиториев
│   │       └── user_repository_impl.py
│   ├── config/                # Конфигурация
│   │   └── settings.py       # Настройки приложения
│   └── dependency_injection/  # DI контейнер
│       ├── container.py      # DI контейнер
│       └── configurator.py   # Настройка зависимостей
│
├── interfaces/                # 🌐 ИНТЕРФЕЙСНЫЙ СЛОЙ
│   ├── telegram/              # Telegram интерфейс
│   │   └── bot_controller.py # Контроллер бота
│   ├── api/                   # HTTP API (будущее)
│   └── cli/                   # CLI интерфейс (будущее)
│
└── main.py                    # 🚀 Точка входа
```

## Архитектурные принципы

### 1. Clean Architecture (Чистая архитектура)

**Правило зависимостей**: Зависимости должны направляться внутрь, к доменному слою.

- **Domain** не зависит ни от чего
- **Application** зависит только от Domain
- **Infrastructure** зависит от Domain и Application
- **Interfaces** зависит от Application

### 2. SOLID принципы

#### Dependency Inversion Principle (DIP)
- **Абстракции не зависят от деталей** ✅
- **Детали зависят от абстракций** ✅

Примеры:
```python
# ❌ НЕПРАВИЛЬНО: зависимость от конкретной реализации
class UserService:
    def __init__(self):
        self.repo = PostgreSQLUserRepository()  # Привязка к PostgreSQL

# ✅ ПРАВИЛЬНО: зависимость от абстракции
class UserService:
    def __init__(self, user_repo: UserRepository):  # Абстракция
        self.repo = user_repo
```

#### Dependency Injection (DI)
Зависимости внедряются извне через DI контейнер:

```python
# Регистрация зависимостей
container.register_singleton(UserRepository, UserRepositoryImpl())
container.register_transient(UserService, lambda: UserServiceImpl())

# Получение сервиса
user_service = container.get(UserService)
```

### 3. Разделение ответственности

#### Доменный слой (Domain)
- **Entities**: Основные бизнес-объекты с поведением
- **Value Objects**: Неизменяемые объекты-значения
- **Domain Services**: Бизнес-логика, не принадлежащая сущностям
- **Repository Interfaces**: Абстракции для доступа к данным

#### Прикладной слой (Application)
- **Application Services**: Координация между доменом и внешним миром
- **DTOs**: Объекты передачи данных между слоями
- **Interfaces**: Контракты для внешних сервисов

#### Инфраструктурный слой (Infrastructure)
- **Repository Implementations**: Конкретные реализации доступа к данным
- **External Services**: Интеграции с внешними системами
- **Configuration**: Настройки приложения

#### Интерфейсный слой (Interfaces)
- **Controllers**: Обработчики внешних запросов
- **API Endpoints**: HTTP эндпоинты
- **CLI Commands**: Команды командной строки

## Примеры использования

### Создание пользователя
```python
# 1. Контроллер получает запрос
async def handle_start_command(user_id: int, username: str):
    # 2. Создается DTO
    create_dto = CreateUserDto(user_id=user_id, username=username)
    
    # 3. Вызывается сервис приложения
    user_dto = await self._user_service.register_user(create_dto)
    
    # 4. Возвращается результат
    return f"Пользователь {user_dto.display_name} создан!"
```

### Поток данных
```
Telegram Bot (Interface)
    ↓ CreateUserDto
Application Service
    ↓ Domain Objects (UserId, Username)
Domain Service
    ↓ User Entity
Repository Interface
    ↓ (DI resolves to)
Repository Implementation
    ↓ SQL
Database
```

## Преимущества новой архитектуры

1. **Тестируемость**: Каждый слой можно тестировать изолированно
2. **Расширяемость**: Легко добавлять новые интерфейсы (API, CLI)
3. **Замещаемость**: Можно менять реализации не затрагивая бизнес-логику
4. **Читаемость**: Четкое разделение ответственности
5. **SOLID**: Следование принципам объектно-ориентированного дизайна

## Следующие шаги

1. ✅ **Архитектура по SOLID** - Реализована
2. ✅ **Доменный слой** - Создан
3. 🔄 **Repository + Unit of Work** - В процессе
4. 🔄 **SQLAlchemy + Alembic** - Планируется
5. 🔄 **E2E тесты** - Планируется
6. 🔄 **FastAPI + CLI интерфейсы** - Планируется

## Запуск демонстрации

```bash
cd src
python main.py
```

Это продемонстрирует работу архитектуры с заглушками репозитория. 