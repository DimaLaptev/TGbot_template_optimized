"""
Подключение к базе данных.
"""
from contextlib import asynccontextmanager
from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, async_sessionmaker, create_async_engine

from infrastructure.config.settings import AppSettings


class DatabaseConnection:
    """Менеджер подключения к базе данных."""
    
    def __init__(self, settings: AppSettings) -> None:
        """Инициализация подключения."""
        self._engine: AsyncEngine = create_async_engine(
            settings.database_url,
            echo=settings.debug,  # Логируем SQL запросы в debug режиме
            pool_pre_ping=True,   # Проверяем соединения перед использованием
            pool_size=20,         # Размер пула соединений
            max_overflow=0,       # Дополнительные соединения
        )
        self._session_factory: async_sessionmaker[AsyncSession] = async_sessionmaker(
            bind=self._engine,
            class_=AsyncSession,
            expire_on_commit=False,
            autoflush=True,
            autocommit=False,
        )
    
    @property
    def engine(self) -> AsyncEngine:
        """Возвращает движок базы данных."""
        return self._engine
    
    @asynccontextmanager
    async def get_session(self) -> AsyncGenerator[AsyncSession, None]:
        """Возвращает сессию базы данных."""
        async with self._session_factory() as session:
            try:
                yield session
                await session.commit()
            except Exception:
                await session.rollback()
                raise
            finally:
                await session.close()
    
    async def close(self) -> None:
        """Закрывает подключение к базе данных."""
        await self._engine.dispose() 