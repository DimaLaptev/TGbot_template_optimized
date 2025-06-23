"""User domain service."""
from typing import Sequence

from ..entities.user import User
from ..exceptions import InvalidTapCountError


class UserDomainService:
    """User domain service for complex business logic."""
    
    @staticmethod
    def calculate_user_rank(user: User, all_users: Sequence[User]) -> int:
        """Calculate user's rank based on tap count.
        
        Args:
            user: User to calculate rank for
            all_users: All users for comparison
            
        Returns:
            User's rank (1-based, 1 is the best)
        """
        if not all_users:
            return 1
            
        sorted_users = sorted(all_users, key=lambda u: u.taps, reverse=True)
        
        try:
            return sorted_users.index(user) + 1
        except ValueError:
            # User not found in the list, return last rank
            return len(all_users) + 1
    
    @staticmethod
    def calculate_total_taps(users: Sequence[User]) -> int:
        """Calculate total taps across all users.
        
        Args:
            users: All users
            
        Returns:
            Total tap count
        """
        return sum(user.taps for user in users)
    
    @staticmethod
    def get_top_users(users: Sequence[User], limit: int = 10) -> Sequence[User]:
        """Get top users by tap count.
        
        Args:
            users: All users
            limit: Maximum number of users to return
            
        Returns:
            Top users ordered by taps descending
            
        Raises:
            InvalidTapCountError: If limit is negative
        """
        if limit < 0:
            raise InvalidTapCountError(limit)
            
        return sorted(users, key=lambda u: u.taps, reverse=True)[:limit]
    
    @staticmethod
    def is_eligible_for_leaderboard(user: User) -> bool:
        """Check if user is eligible for leaderboard.
        
        Args:
            user: User to check
            
        Returns:
            True if user is eligible (has profile and taps > 0)
        """
        return user.has_profile and user.taps > 0
    
    @staticmethod
    def format_leaderboard_entry(user: User, rank: int) -> str:
        """Format user entry for leaderboard display.
        
        Args:
            user: User to format
            rank: User's rank
            
        Returns:
            Formatted leaderboard entry
        """
        medal = ""
        if rank == 1:
            medal = "🥇"
        elif rank == 2:
            medal = "🥈"
        elif rank == 3:
            medal = "🥉"
        
        username_display = f"@{user.username}" if user.username else "Unknown"
        
        return f"{medal} {rank}. {user.display_name} ({username_display}) - {user.taps} taps" 