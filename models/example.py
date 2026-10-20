"""
Example usage of the Bill Splitting Application models.

This module demonstrates how to use the Friend and Bill models.
"""

from models import Friend, Bill


def main():
    """Demonstrate the usage of Friend and Bill models."""
    
    print("=" * 60)
    print("Bill Splitting Application - Python Models Demo")
    print("=" * 60)
    print()
    
    # Create friends
    print("1. Creating Friends:")
    print("-" * 40)
    
    clark = Friend(
        id="118836",
        name="Clark",
        image="https://i.pravatar.cc/48?u=118836",
        balance=-7.0
    )
    print(f"✓ Created: {clark.name}")
    print(f"  Status: {clark.get_balance_status()}")
    print()
    
    sarah = Friend(
        id="933372",
        name="Sarah",
        image="https://i.pravatar.cc/48?u=933372",
        balance=20.0
    )
    print(f"✓ Created: {sarah.name}")
    print(f"  Status: {sarah.get_balance_status()}")
    print()
    
    anthony = Friend(
        id="499476",
        name="Anthony",
        image="https://i.pravatar.cc/48?u=499476",
        balance=0.0
    )
    print(f"✓ Created: {anthony.name}")
    print(f"  Status: {anthony.get_balance_status()}")
    print()
    
    # Create a new friend dynamically
    print("2. Adding a New Friend:")
    print("-" * 40)
    new_friend = Friend(
        name="Emma",
        image="https://i.pravatar.cc/48?u=12345"
    )
    print(f"✓ Created: {new_friend.name} (ID: {new_friend.id})")
    print(f"  Status: {new_friend.get_balance_status()}")
    print()
    
    # Create and split a bill
    print("3. Splitting a Bill:")
    print("-" * 40)
    bill = Bill(
        total_amount=100.0,
        paid_by_user=60.0,
        who_is_paying='user',
        friend_id=anthony.id
    )
    print(f"✓ {bill.get_split_summary()}")
    print(f"  Balance change: ${bill.calculate_balance_change():.2f}")
    print()
    
    # Update friend balance after bill split
    print("4. Updating Friend Balance:")
    print("-" * 40)
    print(f"Before: {anthony.get_balance_status()}")
    anthony.add_to_balance(bill.calculate_balance_change())
    print(f"After:  {anthony.get_balance_status()}")
    print()
    
    # Convert to/from dictionary
    print("5. Serialization Example:")
    print("-" * 40)
    friend_dict = clark.to_dict()
    print(f"Friend as dict: {friend_dict}")
    
    restored_friend = Friend.from_dict(friend_dict)
    print(f"Restored friend: {restored_friend.name} (balance: ${restored_friend.balance})")
    print()
    
    bill_dict = bill.to_dict()
    print(f"Bill as dict: {bill_dict}")
    print()
    
    # Demonstrate helper methods
    print("6. Helper Methods:")
    print("-" * 40)
    print(f"Clark owes me: ${clark.owes_me():.2f}")
    print(f"I owe Clark: ${clark.i_owe():.2f}")
    print(f"Is even: {clark.is_even()}")
    print()
    
    print(f"Sarah owes me: ${sarah.owes_me():.2f}")
    print(f"I owe Sarah: ${sarah.i_owe():.2f}")
    print(f"Is even: {sarah.is_even()}")
    print()
    
    # Settle a balance
    print("7. Settling Balance:")
    print("-" * 40)
    print(f"Before settling: {sarah.get_balance_status()}")
    sarah.settle_balance()
    print(f"After settling:  {sarah.get_balance_status()}")
    print()
    
    print("=" * 60)
    print("Demo completed successfully!")
    print("=" * 60)


if __name__ == "__main__":
    main()
