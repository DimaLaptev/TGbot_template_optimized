"""
Реализация репозитория пользователей с SQLAlchemy.
"""
from typing import List, Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from domain.entities.user import User
from domain.repositories.user_repository import UserRepository
from domain.value_objects.user_id import UserId
from domain.value_objects.username import Username
from infrastructure.database.connection import DatabaseConnection
from infrastructure.database.models import UserModel


class UserRepositoryImpl(UserRepository):
    """Реализация репозитория пользователей с SQLAlchemy."""
    
    def __init__(self, db_connection: DatabaseConnection) -> None:
        """Инициализация репозитория."""
        self._db_connection = db_connection
    
    async def find_by_id(self, user_id: UserId) -> Optional[User]:
        """Найти пользователя по ID."""
        async with self._db_connection.get_session() as session:
            stmt = select(UserModel).where(UserModel.user_id == user_id.value)
            result = await session.execute(stmt)
            user_model = result.scalar_one_or_none()
            
            if user_model is None:
                return None
            
            return self._model_to_entity(user_model)
    
    async def find_by_username(self, username: Username) -> Optional[User]:
        """Найти пользователя по username."""
        async with self._db_connection.get_session() as session:
            stmt = select(UserModel).where(UserModel.username == username.value)
            result = await session.execute(stmt)
            user_model = result.scalar_one_or_none()
            
            if user_model is None:
                return None
            
            return self._model_to_entity(user_model)
    
    async def save(self, user: User) -> User:
        """Сохранить пользователя."""
        async with self._db_connection.get_session() as session:
            # Проверяем существует ли пользователь
            stmt = select(UserModel).where(UserModel.user_id == user.user_id.value)
            result = await session.execute(stmt)
            user_model = result.scalar_one_or_none()
            
            if user_model is None:
                # Создаем нового пользователя
                user_model = self._entity_to_model(user)
                session.add(user_model)
            else:
                # Обновляем существующего
                user_model.username = user.profile.username.value if user.profile.username else None
                user_model.first_name = user.profile.first_name
                user_model.last_name = user.profile.last_name
                user_model.taps_count = user.taps_count
            
            await session.flush()
            await session.refresh(user_model)
            
            return self._model_to_entity(user_model)
    
    async def delete(self, user_id: UserId) -> bool:
        """Удалить пользователя."""
        async with self._db_connection.get_session() as session:
            stmt = select(UserModel).where(UserModel.user_id == user_id.value)
            result = await session.execute(stmt)
            user_model = result.scalar_one_or_none()
            
            if user_model is None:
                return False
            
            await session.delete(user_model)
            return True
    
    async def find_top_users(self, limit: int = 10) -> List[User]:
        """Найти топ пользователей по количеству нажатий."""
        async with self._db_connection.get_session() as session:
            stmt = (
                select(UserModel)
                .order_by(UserModel.taps_count.desc())
                .limit(limit)
            )
            result = await session.execute(stmt)
            user_models = result.scalars().all()
            
            return [self._model_to_entity(model) for model in user_models]
    
    def _model_to_entity(self, model: UserModel) -> User:
        """Конвертировать модель в доменную сущность."""
        from domain.value_objects.user_profile import UserProfile
        
        profile = UserProfile(
            username=Username(model.username) if model.username else None,
            first_name=model.first_name,
            last_name=model.last_name,
        )
        
        return User(
            user_id=UserId(model.user_id),
            profile=profile,
            taps_count=model.taps_count,
        )
    
    def _entity_to_model(self, entity: User) -> UserModel:
        """Конвертировать доменную сущность в модель."""
        return UserModel(
            user_id=entity.user_id.value,
            username=entity.profile.username.value if entity.profile.username else None,
            first_name=entity.profile.first_name,
            last_name=entity.profile.last_name,
            taps_count=entity.taps_count,
        ) 