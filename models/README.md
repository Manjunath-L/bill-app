# Python Models for Bill Splitting Application

This directory contains Python data models that represent the core entities used in the bill-splitting React application.

## Models

### Friend Model (`friend.py`)

Represents a friend in the bill-splitting application.

**Attributes:**
- `id` (str): Unique identifier for the friend (auto-generated UUID if not provided)
- `name` (str): Friend's name (required, cannot be empty)
- `image` (str): URL to the friend's avatar/profile image (required, cannot be empty)
- `balance` (float): Current balance (default: 0.0)
  - Positive value: friend owes you
  - Negative value: you owe the friend
  - Zero: you are even

**Methods:**
- `owes_me()`: Returns how much the friend owes you (0 if negative balance)
- `i_owe()`: Returns how much you owe the friend (0 if positive balance)
- `is_even()`: Returns True if balance is zero
- `add_to_balance(amount)`: Adds an amount to the balance
- `settle_balance()`: Resets balance to zero
- `get_balance_status()`: Returns human-readable balance description
- `to_dict()`: Converts to dictionary format
- `from_dict(data)`: Creates Friend from dictionary

**Example:**
```python
from models import Friend

# Create a new friend
friend = Friend(
    name="Sarah",
    image="https://i.pravatar.cc/48?u=933372",
    balance=20.0
)

# Check balance status
print(friend.get_balance_status())  # "Sarah owes you $20.00"

# Add to balance
friend.add_to_balance(15.0)
print(f"New balance: ${friend.balance}")  # "New balance: $35.0"
```

### Bill Model (`bill.py`)

Represents a bill to be split between the user and a friend.

**Attributes:**
- `id` (str): Unique identifier for the bill (auto-generated UUID if not provided)
- `total_amount` (float): Total bill amount (must be positive)
- `paid_by_user` (float): Amount paid by the user (0 to total_amount)
- `who_is_paying` (str): Who paid the bill - either 'user' or 'friend'
- `friend_id` (str): ID of the friend splitting the bill (required)
- `created_at` (datetime): Timestamp when bill was created (auto-generated)

**Properties:**
- `paid_by_friend`: Calculated amount paid by friend (total - user's amount)

**Methods:**
- `calculate_balance_change()`: Returns how much the friend's balance should change
  - Positive: friend owes user
  - Negative: user owes friend
- `get_user_share()`: Returns user's share of the bill
- `get_friend_share()`: Returns friend's share of the bill
- `is_split_evenly()`: Returns True if split 50/50
- `get_split_summary()`: Returns human-readable summary
- `to_dict()`: Converts to dictionary format
- `from_dict(data)`: Creates Bill from dictionary

**Example:**
```python
from models import Bill, Friend

# Create a friend
friend = Friend(name="John", image="https://example.com/john.jpg")

# Create a bill
bill = Bill(
    total_amount=100.0,
    paid_by_user=60.0,
    who_is_paying='user',
    friend_id=friend.id
)

# Calculate balance change
balance_change = bill.calculate_balance_change()
print(f"Balance change: ${balance_change}")  # "Balance change: $40.0"

# Update friend's balance
friend.add_to_balance(balance_change)
print(friend.get_balance_status())  # "John owes you $40.00"
```

## Usage

### Installation

No external dependencies are required. The models use Python's standard library:
- `dataclasses` for data classes
- `typing` for type hints
- `uuid` for generating unique IDs
- `datetime` for timestamps

### Running the Example

```bash
cd models
python example.py
```

This will demonstrate:
- Creating friends with different balances
- Splitting bills
- Updating balances
- Serialization/deserialization
- Helper methods

### Running Tests

```bash
cd models
python test_models.py
```

Or with verbose output:
```bash
python test_models.py -v
```

## Integration with React App

These Python models mirror the data structures used in the React application (`src/App.js`):

**React Friend Object:**
```javascript
{
  id: 118836,
  name: "Clark",
  image: "https://i.pravatar.cc/48?u=118836",
  balance: -7,
}
```

**Python Friend Model:**
```python
Friend(
    id="118836",
    name="Clark",
    image="https://i.pravatar.cc/48?u=118836",
    balance=-7.0
)
```

The models can be used for:
- Backend API development
- Data validation
- Database models (with ORM adapters)
- Testing and simulation
- Data processing and analysis

## Design Patterns

The models follow these Python best practices:

1. **Dataclasses**: Modern Python approach for data containers
2. **Type Hints**: Clear type annotations for better IDE support
3. **Validation**: Input validation in `__post_init__` methods
4. **Properties**: Computed properties for derived values
5. **Serialization**: Easy conversion to/from dictionaries for JSON APIs
6. **Immutability**: Core attributes are set at initialization
7. **Helper Methods**: Convenient methods for common operations

## Future Enhancements

Potential improvements:
- Add database ORM integration (SQLAlchemy, Django ORM)
- Add Pydantic models for API validation
- Add export to various formats (JSON, CSV, Excel)
- Add transaction history tracking
- Add currency support
- Add multi-way bill splitting (more than 2 people)
