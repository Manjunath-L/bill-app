"""
Bill model for the Bill Splitting Application.

This module defines the Bill class that represents a bill
to be split between the user and a friend.
"""

from dataclasses import dataclass, field
from typing import Optional, Literal
from datetime import datetime
from uuid import uuid4


@dataclass
class Bill:
    """
    Represents a bill to be split between user and friend.
    
    Attributes:
        total_amount: Total bill amount
        paid_by_user: Amount paid by the user
        who_is_paying: Who is paying the bill ('user' or 'friend')
        friend_id: ID of the friend splitting the bill with
        id: Unique identifier for the bill
        created_at: Timestamp when the bill was created
    """
    total_amount: float
    paid_by_user: float
    who_is_paying: Literal['user', 'friend']
    friend_id: str
    id: Optional[str] = field(default_factory=lambda: str(uuid4()))
    created_at: datetime = field(default_factory=lambda: datetime.now())
    
    def __post_init__(self):
        """Validate the bill data after initialization."""
        if self.total_amount <= 0:
            raise ValueError("Total bill amount must be positive")
        
        if self.paid_by_user < 0:
            raise ValueError("Amount paid by user cannot be negative")
        
        if self.paid_by_user > self.total_amount:
            raise ValueError("Amount paid by user cannot exceed total bill amount")
        
        if self.who_is_paying not in ['user', 'friend']:
            raise ValueError("who_is_paying must be either 'user' or 'friend'")
        
        if not self.friend_id:
            raise ValueError("friend_id cannot be empty")
    
    @property
    def paid_by_friend(self) -> float:
        """
        Calculate the amount paid by the friend.
        
        Returns:
            Amount paid by the friend (total - user's amount)
        """
        return self.total_amount - self.paid_by_user
    
    def calculate_balance_change(self) -> float:
        """
        Calculate the change in balance for the friend.
        
        This determines how much the balance should change:
        - Positive value means friend owes the user
        - Negative value means user owes the friend
        
        Returns:
            Balance change amount
        """
        if self.who_is_paying == 'user':
            # User paid the bill, so friend owes the user for friend's share
            return self.paid_by_friend
        else:
            # Friend paid the bill, so user owes the friend for user's share
            return -self.paid_by_user
    
    def get_user_share(self) -> float:
        """
        Get the amount paid by the user.
        
        Note: This returns the amount paid by the user, which may be
        different from their actual share depending on who is paying.
        
        Returns:
            Amount paid by the user
        """
        return self.paid_by_user
    
    def get_friend_share(self) -> float:
        """
        Get the amount paid by the friend.
        
        Note: This returns the amount paid by the friend (calculated as
        total - user's payment), which may be different from their actual
        share depending on who is paying.
        
        Returns:
            Amount paid by the friend
        """
        return self.paid_by_friend
    
    def is_split_evenly(self) -> bool:
        """
        Check if the bill is split evenly (50/50).
        
        Returns:
            True if split evenly, False otherwise
        """
        half = self.total_amount / 2
        return abs(self.paid_by_user - half) < 0.01  # Allow for small floating point differences
    
    def get_split_summary(self) -> str:
        """
        Get a human-readable summary of the bill split.
        
        Returns:
            String describing the bill split
        """
        payer = "You" if self.who_is_paying == 'user' else "Friend"
        return (f"Bill of ${self.total_amount:.2f} - "
                f"Your share: ${self.paid_by_user:.2f}, "
                f"Friend's share: ${self.paid_by_friend:.2f}, "
                f"Paid by: {payer}")
    
    def to_dict(self) -> dict:
        """
        Convert the Bill object to a dictionary.
        
        Returns:
            Dictionary representation of the bill
        """
        return {
            'id': self.id,
            'total_amount': self.total_amount,
            'paid_by_user': self.paid_by_user,
            'paid_by_friend': self.paid_by_friend,
            'who_is_paying': self.who_is_paying,
            'friend_id': self.friend_id,
            'created_at': self.created_at.isoformat()
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> 'Bill':
        """
        Create a Bill object from a dictionary.
        
        Args:
            data: Dictionary containing bill data
            
        Returns:
            Bill object
        """
        created_at = data.get('created_at')
        if isinstance(created_at, str):
            created_at = datetime.fromisoformat(created_at)
        elif created_at is None:
            created_at = datetime.now()
        
        return cls(
            id=data.get('id'),
            total_amount=data['total_amount'],
            paid_by_user=data['paid_by_user'],
            who_is_paying=data['who_is_paying'],
            friend_id=data['friend_id'],
            created_at=created_at
        )
