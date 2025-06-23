"""User repository implementation with SQLAlchemy Core."""
from datetime import datetime, timezone
from typing import Sequence

from sqlalchemy import and_, desc, select
from sqlalchemy.ext.asyncio import AsyncConnection

from ....domain.entities.user import User
from ....domain.exceptions import UserNotFoundError
from ....domain.repositories.user_repository import UserRepository
from ....domain.value_objects.social_id import SocialId
from ....domain.value_objects.user_id import UserId
from ....domain.value_objects.username import Username
from ..models import users_table


class SQLAlchemyUserRepository(UserRepository):
    """SQLAlchemy implementation of user repository."""
    
    def __init__(self, connection: AsyncConnection) -> None:
        """Initialize repository with database connection.
        
        Args:
            connection: Database connection
        """
        self._connection = connection
    
    async def create(self, user: User) -> User:
        """Create a new user."""
        query = users_table.insert().values(
            social_id=user.social_id.value,
            username=user.username.value if user.username else None,
            registration_date=user.registration_date,
            name=user.name,
            info=user.info,
            photo_file_id=user.photo_file_id,
            taps=user.taps,
        )
        
        result = await self._connection.execute(query)
        user_id = result.inserted_primary_key[0]
        
        # Return user with assigned ID
        return User(
            id=UserId(user_id),
            social_id=user.social_id,
            username=user.username,
            registration_date=user.registration_date,
            name=user.name,
            info=user.info,
            photo_file_id=user.photo_file_id,
            taps=user.taps,
        )
    
    async def get_by_id(self, user_id: UserId) -> User | None:
        """Get user by ID."""
        query = select(users_table).where(users_table.c.id == user_id.value)
        result = await self._connection.execute(query)
        row = result.fetchone()
        
        return self._map_row_to_user(row) if row else None
    
    async def get_by_social_id(self, social_id: SocialId) -> User | None:
        """Get user by social ID."""
        query = select(users_table).where(users_table.c.social_id == social_id.value)
        result = await self._connection.execute(query)
        row = result.fetchone()
        
        return self._map_row_to_user(row) if row else None
    
    async def update(self, user: User) -> User:
        """Update existing user."""
        query = (
            users_table.update()
            .where(users_table.c.id == user.id.value)
            .values(
                social_id=user.social_id.value,
                username=user.username.value if user.username else None,
                registration_date=user.registration_date,
                name=user.name,
                info=user.info,
                photo_file_id=user.photo_file_id,
                taps=user.taps,
            )
        )
        
        result = await self._connection.execute(query)
        if result.rowcount == 0:
            raise UserNotFoundError(str(user.id.value))
        
        return user
    
    async def delete(self, user_id: UserId) -> None:
        """Delete user by ID."""
        query = users_table.delete().where(users_table.c.id == user_id.value)
        result = await self._connection.execute(query)
        
        if result.rowcount == 0:
            raise UserNotFoundError(str(user_id.value))
    
    async def get_all(self, *, limit: int | None = None, offset: int = 0) -> Sequence[User]:
        """Get all users with pagination."""
        query = select(users_table).offset(offset)
        
        if limit is not None:
            query = query.limit(limit)
        
        result = await self._connection.execute(query)
        rows = result.fetchall()
        
        return [self._map_row_to_user(row) for row in rows]
    
    async def get_top_by_taps(self, limit: int = 10) -> Sequence[User]:
        """Get top users by tap count."""
        query = (
            select(users_table)
            .order_by(desc(users_table.c.taps))
            .limit(limit)
        )
        
        result = await self._connection.execute(query)
        rows = result.fetchall()
        
        return [self._map_row_to_user(row) for row in rows]
    
    async def count(self) -> int:
        """Get total number of users."""
        query = select(users_table.c.id).count()
        result = await self._connection.execute(query)
        
        return result.scalar() or 0
    
    def _map_row_to_user(self, row: any) -> User:
        """Map database row to User entity.
        
        Args:
            row: Database row
            
        Returns:
            User entity
        """
        username = Username(row.username) if row.username else None
        
        return User(
            id=UserId(row.id),
            social_id=SocialId(row.social_id),
            username=username,
            registration_date=row.registration_date.replace(tzinfo=timezone.utc)
            if row.registration_date.tzinfo is None
            else row.registration_date,
            name=row.name,
            info=row.info,
            photo_file_id=row.photo_file_id,
            taps=row.taps,
        ) 