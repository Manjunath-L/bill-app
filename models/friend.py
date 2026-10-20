"""
Friend model for the Bill Splitting Application.

This module defines the Friend class that represents a person
who can split bills with the user.
"""

from dataclasses import dataclass, field
from typing import Optional
from uuid import uuid4


@dataclass
class Friend:
    """
    Represents a friend in the bill-splitting application.
    
    Attributes:
        id: Unique identifier for the friend
        name: Friend's name
        image: URL to the friend's avatar/profile image
        balance: Current balance - positive means friend owes you,
                 negative means you owe the friend, zero means even
    """
    name: str
    image: str
    balance: float = 0.0
    id: Optional[str] = field(default_factory=lambda: str(uuid4()))
    
    def __post_init__(self):
        """Validate the friend data after initialization."""
        if not self.name or not self.name.strip():
            raise ValueError("Friend name cannot be empty")
        
        if not self.image or not self.image.strip():
            raise ValueError("Friend image URL cannot be empty")
    
    def owes_me(self) -> float:
        """
        Calculate how much this friend owes the user.
        
        Returns:
            Positive amount if friend owes the user, 0 otherwise
        """
        return max(0, self.balance)
    
    def i_owe(self) -> float:
        """
        Calculate how much the user owes this friend.
        
        Returns:
            Positive amount if user owes the friend, 0 otherwise
        """
        return max(0, -self.balance)
    
    def is_even(self) -> bool:
        """
        Check if the user and friend are even (no debt either way).
        
        Returns:
            True if balance is zero, False otherwise
        """
        return self.balance == 0.0
    
    def add_to_balance(self, amount: float) -> None:
        """
        Add an amount to the friend's balance.
        
        Args:
            amount: Amount to add (positive or negative)
        """
        self.balance += amount
    
    def settle_balance(self) -> None:
        """Reset the balance to zero (settle all debts)."""
        self.balance = 0.0
    
    def get_balance_status(self) -> str:
        """
        Get a human-readable description of the balance status.
        
        Returns:
            String describing the balance status
        """
        if self.balance < 0:
            return f"You owe {self.name} ${abs(self.balance):.2f}"
        elif self.balance > 0:
            return f"{self.name} owes you ${self.balance:.2f}"
        else:
            return f"You and {self.name} are even"
    
    def to_dict(self) -> dict:
        """
        Convert the Friend object to a dictionary.
        
        Returns:
            Dictionary representation of the friend
        """
        return {
            'id': self.id,
            'name': self.name,
            'image': self.image,
            'balance': self.balance
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> 'Friend':
        """
        Create a Friend object from a dictionary.
        
        Args:
            data: Dictionary containing friend data
            
        Returns:
            Friend object
        """
        return cls(
            id=data.get('id'),
            name=data['name'],
            image=data['image'],
            balance=data.get('balance', 0.0)
        )
