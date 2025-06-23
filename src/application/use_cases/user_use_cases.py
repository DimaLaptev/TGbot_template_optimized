"""User use cases implementation."""
from datetime import datetime, timezone
from typing import Sequence

from ...domain.entities.user import User
from ...domain.exceptions import UserAlreadyExistsError, UserNotFoundError
from ...domain.repositories.unit_of_work import UnitOfWork
from ...domain.services.user_service import UserDomainService
from ...domain.value_objects.social_id import SocialId
from ...domain.value_objects.user_id import UserId
from ...domain.value_objects.username import Username
from ..dto.user_dto import (
    CreateUserRequest,
    LeaderboardResponse,
    UpdateUserProfileRequest,
    UserResponse,
    UserTapRequest,
)


class UserUseCases:
    """User use cases for business operations."""
    
    def __init__(self, uow: UnitOfWork) -> None:
        """Initialize use cases with unit of work.
        
        Args:
            uow: Unit of work for data access
        """
        self._uow = uow
        self._domain_service = UserDomainService()
    
    async def create_user(self, request: CreateUserRequest) -> UserResponse:
        """Create a new user.
        
        Args:
            request: User creation request
            
        Returns:
            Created user data
            
        Raises:
            UserAlreadyExistsError: If user already exists
        """
        async with self._uow as uow:
            social_id = SocialId(request.social_id)
            
            # Check if user already exists
            existing_user = await uow.users.get_by_social_id(social_id)
            if existing_user:
                raise UserAlreadyExistsError(request.social_id)
            
            # Create new user
            username = Username(request.username) if request.username else None
            user = User(
                id=UserId(0),  # Will be set by repository
                social_id=social_id,
                username=username,
                registration_date=datetime.now(timezone.utc),
            )
            
            created_user = await uow.users.create(user)
            await uow.commit()
            
            return self._map_user_to_response(created_user)
    
    async def get_user_by_social_id(self, social_id: int) -> UserResponse | None:
        """Get user by social ID.
        
        Args:
            social_id: Social media identifier
            
        Returns:
            User data or None if not found
        """
        async with self._uow as uow:
            user = await uow.users.get_by_social_id(SocialId(social_id))
            return self._map_user_to_response(user) if user else None
    
    async def update_user_profile(self, request: UpdateUserProfileRequest) -> UserResponse:
        """Update user profile.
        
        Args:
            request: Profile update request
            
        Returns:
            Updated user data
            
        Raises:
            UserNotFoundError: If user not found
        """
        async with self._uow as uow:
            user = await uow.users.get_by_id(UserId(request.user_id))
            if not user:
                raise UserNotFoundError(str(request.user_id))
            
            user.update_profile(
                name=request.name,
                info=request.info,
                photo_file_id=request.photo_file_id,
            )
            
            updated_user = await uow.users.update(user)
            await uow.commit()
            
            return self._map_user_to_response(updated_user)
    
    async def increment_user_taps(self, request: UserTapRequest) -> UserResponse:
        """Increment user tap count.
        
        Args:
            request: Tap increment request
            
        Returns:
            Updated user data
            
        Raises:
            UserNotFoundError: If user not found
        """
        async with self._uow as uow:
            user = await uow.users.get_by_social_id(SocialId(request.social_id))
            if not user:
                raise UserNotFoundError(str(request.social_id))
            
            user.increment_taps(request.count)
            updated_user = await uow.users.update(user)
            await uow.commit()
            
            return self._map_user_to_response(updated_user)
    
    async def get_leaderboard(self, limit: int = 10) -> LeaderboardResponse:
        """Get user leaderboard.
        
        Args:
            limit: Maximum number of top users to return
            
        Returns:
            Leaderboard data
        """
        async with self._uow as uow:
            top_users = await uow.users.get_top_by_taps(limit)
            all_users = await uow.users.get_all()
            
            total_taps = self._domain_service.calculate_total_taps(all_users)
            
            return LeaderboardResponse(
                total_users=len(all_users),
                total_taps=total_taps,
                top_users=[self._map_user_to_response(user) for user in top_users],
            )
    
    async def get_user_rank(self, social_id: int) -> int | None:
        """Get user's rank in leaderboard.
        
        Args:
            social_id: User's social ID
            
        Returns:
            User's rank or None if user not found
        """
        async with self._uow as uow:
            user = await uow.users.get_by_social_id(SocialId(social_id))
            if not user:
                return None
            
            all_users = await uow.users.get_all()
            return self._domain_service.calculate_user_rank(user, all_users)
    
    async def get_all_users_for_digest(self) -> Sequence[UserResponse]:
        """Get all users for daily digest.
        
        Returns:
            All users data
        """
        async with self._uow as uow:
            users = await uow.users.get_all()
            return [self._map_user_to_response(user) for user in users]
    
    def _map_user_to_response(self, user: User) -> UserResponse:
        """Map user entity to response DTO.
        
        Args:
            user: User entity
            
        Returns:
            User response DTO
        """
        return UserResponse(
            id=user.id.value,
            social_id=user.social_id.value,
            username=user.username.value if user.username else None,
            registration_date=user.registration_date,
            name=user.name,
            info=user.info,
            photo_file_id=user.photo_file_id,
            taps=user.taps,
            has_profile=user.has_profile,
            display_name=user.display_name,
        ) 