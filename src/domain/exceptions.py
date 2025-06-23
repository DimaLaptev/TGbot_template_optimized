"""Domain exceptions."""


class DomainError(Exception):
    """Base domain error."""
    
    def __init__(self, message: str) -> None:
        """Initialize domain error.
        
        Args:
            message: Error message
        """
        self.message = message
        super().__init__(self.message)


class UserError(DomainError):
    """Base user-related error."""


class UserNotFoundError(UserError):
    """User not found error."""
    
    def __init__(self, identifier: str) -> None:
        """Initialize user not found error.
        
        Args:
            identifier: User identifier (ID or social_id)
        """
        super().__init__(f"User not found: {identifier}")


class UserAlreadyExistsError(UserError):
    """User already exists error."""
    
    def __init__(self, social_id: int) -> None:
        """Initialize user already exists error.
        
        Args:
            social_id: Social media identifier
        """
        super().__init__(f"User with social_id {social_id} already exists")


class InvalidTapCountError(UserError):
    """Invalid tap count error."""
    
    def __init__(self, count: int) -> None:
        """Initialize invalid tap count error.
        
        Args:
            count: Invalid tap count
        """
        super().__init__(f"Invalid tap count: {count}. Must be non-negative") 