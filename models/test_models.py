"""
Tests for the Bill Splitting Application models.

This module contains tests for the Friend and Bill models.
"""

import unittest
from datetime import datetime
from models import Friend, Bill


class TestFriend(unittest.TestCase):
    """Test cases for the Friend model."""
    
    def test_friend_creation(self):
        """Test creating a friend with all parameters."""
        friend = Friend(
            id="123",
            name="John",
            image="https://example.com/john.jpg",
            balance=10.0
        )
        self.assertEqual(friend.id, "123")
        self.assertEqual(friend.name, "John")
        self.assertEqual(friend.image, "https://example.com/john.jpg")
        self.assertEqual(friend.balance, 10.0)
    
    def test_friend_auto_id(self):
        """Test that friend ID is auto-generated if not provided."""
        friend = Friend(name="Jane", image="https://example.com/jane.jpg")
        self.assertIsNotNone(friend.id)
        self.assertGreater(len(friend.id), 0)
    
    def test_friend_default_balance(self):
        """Test that default balance is 0.0."""
        friend = Friend(name="Bob", image="https://example.com/bob.jpg")
        self.assertEqual(friend.balance, 0.0)
    
    def test_friend_empty_name_validation(self):
        """Test that empty name raises ValueError."""
        with self.assertRaises(ValueError):
            Friend(name="", image="https://example.com/test.jpg")
    
    def test_friend_empty_image_validation(self):
        """Test that empty image raises ValueError."""
        with self.assertRaises(ValueError):
            Friend(name="Test", image="")
    
    def test_owes_me(self):
        """Test owes_me method."""
        friend = Friend(name="Test", image="url", balance=15.0)
        self.assertEqual(friend.owes_me(), 15.0)
        
        friend.balance = -10.0
        self.assertEqual(friend.owes_me(), 0.0)
    
    def test_i_owe(self):
        """Test i_owe method."""
        friend = Friend(name="Test", image="url", balance=-15.0)
        self.assertEqual(friend.i_owe(), 15.0)
        
        friend.balance = 10.0
        self.assertEqual(friend.i_owe(), 0.0)
    
    def test_is_even(self):
        """Test is_even method."""
        friend = Friend(name="Test", image="url", balance=0.0)
        self.assertTrue(friend.is_even())
        
        friend.balance = 5.0
        self.assertFalse(friend.is_even())
    
    def test_add_to_balance(self):
        """Test add_to_balance method."""
        friend = Friend(name="Test", image="url", balance=10.0)
        friend.add_to_balance(5.0)
        self.assertEqual(friend.balance, 15.0)
        
        friend.add_to_balance(-8.0)
        self.assertEqual(friend.balance, 7.0)
    
    def test_settle_balance(self):
        """Test settle_balance method."""
        friend = Friend(name="Test", image="url", balance=25.0)
        friend.settle_balance()
        self.assertEqual(friend.balance, 0.0)
    
    def test_get_balance_status(self):
        """Test get_balance_status method."""
        friend = Friend(name="Alice", image="url", balance=10.0)
        self.assertIn("Alice owes you $10.00", friend.get_balance_status())
        
        friend.balance = -10.0
        self.assertIn("You owe Alice $10.00", friend.get_balance_status())
        
        friend.balance = 0.0
        self.assertIn("are even", friend.get_balance_status())
    
    def test_to_dict(self):
        """Test to_dict method."""
        friend = Friend(id="456", name="Charlie", image="url", balance=5.0)
        data = friend.to_dict()
        
        self.assertEqual(data['id'], "456")
        self.assertEqual(data['name'], "Charlie")
        self.assertEqual(data['image'], "url")
        self.assertEqual(data['balance'], 5.0)
    
    def test_from_dict(self):
        """Test from_dict method."""
        data = {
            'id': '789',
            'name': 'Diana',
            'image': 'url',
            'balance': 15.0
        }
        friend = Friend.from_dict(data)
        
        self.assertEqual(friend.id, '789')
        self.assertEqual(friend.name, 'Diana')
        self.assertEqual(friend.image, 'url')
        self.assertEqual(friend.balance, 15.0)


class TestBill(unittest.TestCase):
    """Test cases for the Bill model."""
    
    def test_bill_creation(self):
        """Test creating a bill with all parameters."""
        bill = Bill(
            id="bill123",
            total_amount=100.0,
            paid_by_user=60.0,
            who_is_paying='user',
            friend_id='friend123'
        )
        self.assertEqual(bill.id, "bill123")
        self.assertEqual(bill.total_amount, 100.0)
        self.assertEqual(bill.paid_by_user, 60.0)
        self.assertEqual(bill.who_is_paying, 'user')
        self.assertEqual(bill.friend_id, 'friend123')
    
    def test_bill_auto_id(self):
        """Test that bill ID is auto-generated if not provided."""
        bill = Bill(
            total_amount=50.0,
            paid_by_user=25.0,
            who_is_paying='user',
            friend_id='friend123'
        )
        self.assertIsNotNone(bill.id)
        self.assertGreater(len(bill.id), 0)
    
    def test_bill_created_at(self):
        """Test that created_at is set automatically."""
        bill = Bill(
            total_amount=50.0,
            paid_by_user=25.0,
            who_is_paying='user',
            friend_id='friend123'
        )
        self.assertIsInstance(bill.created_at, datetime)
    
    def test_paid_by_friend(self):
        """Test paid_by_friend property."""
        bill = Bill(
            total_amount=100.0,
            paid_by_user=40.0,
            who_is_paying='user',
            friend_id='friend123'
        )
        self.assertEqual(bill.paid_by_friend, 60.0)
    
    def test_calculate_balance_change_user_paying(self):
        """Test balance change when user is paying."""
        bill = Bill(
            total_amount=100.0,
            paid_by_user=60.0,
            who_is_paying='user',
            friend_id='friend123'
        )
        # Friend owes user 40.0 (friend's share)
        self.assertEqual(bill.calculate_balance_change(), 40.0)
    
    def test_calculate_balance_change_friend_paying(self):
        """Test balance change when friend is paying."""
        bill = Bill(
            total_amount=100.0,
            paid_by_user=60.0,
            who_is_paying='friend',
            friend_id='friend123'
        )
        # User owes friend 60.0 (user's share)
        self.assertEqual(bill.calculate_balance_change(), -60.0)
    
    def test_is_split_evenly(self):
        """Test is_split_evenly method."""
        bill = Bill(
            total_amount=100.0,
            paid_by_user=50.0,
            who_is_paying='user',
            friend_id='friend123'
        )
        self.assertTrue(bill.is_split_evenly())
        
        bill.paid_by_user = 60.0
        self.assertFalse(bill.is_split_evenly())
    
    def test_negative_total_validation(self):
        """Test that negative total amount raises ValueError."""
        with self.assertRaises(ValueError):
            Bill(
                total_amount=-10.0,
                paid_by_user=5.0,
                who_is_paying='user',
                friend_id='friend123'
            )
    
    def test_negative_user_paid_validation(self):
        """Test that negative paid_by_user raises ValueError."""
        with self.assertRaises(ValueError):
            Bill(
                total_amount=100.0,
                paid_by_user=-10.0,
                who_is_paying='user',
                friend_id='friend123'
            )
    
    def test_user_paid_exceeds_total_validation(self):
        """Test that paid_by_user exceeding total raises ValueError."""
        with self.assertRaises(ValueError):
            Bill(
                total_amount=100.0,
                paid_by_user=150.0,
                who_is_paying='user',
                friend_id='friend123'
            )
    
    def test_invalid_payer_validation(self):
        """Test that invalid who_is_paying raises ValueError."""
        with self.assertRaises(ValueError):
            Bill(
                total_amount=100.0,
                paid_by_user=50.0,
                who_is_paying='invalid',
                friend_id='friend123'
            )
    
    def test_empty_friend_id_validation(self):
        """Test that empty friend_id raises ValueError."""
        with self.assertRaises(ValueError):
            Bill(
                total_amount=100.0,
                paid_by_user=50.0,
                who_is_paying='user',
                friend_id=''
            )
    
    def test_to_dict(self):
        """Test to_dict method."""
        bill = Bill(
            id='bill456',
            total_amount=80.0,
            paid_by_user=50.0,
            who_is_paying='friend',
            friend_id='friend456'
        )
        data = bill.to_dict()
        
        self.assertEqual(data['id'], 'bill456')
        self.assertEqual(data['total_amount'], 80.0)
        self.assertEqual(data['paid_by_user'], 50.0)
        self.assertEqual(data['paid_by_friend'], 30.0)
        self.assertEqual(data['who_is_paying'], 'friend')
        self.assertEqual(data['friend_id'], 'friend456')
        self.assertIn('created_at', data)
    
    def test_from_dict(self):
        """Test from_dict method."""
        data = {
            'id': 'bill789',
            'total_amount': 120.0,
            'paid_by_user': 70.0,
            'who_is_paying': 'user',
            'friend_id': 'friend789'
        }
        bill = Bill.from_dict(data)
        
        self.assertEqual(bill.id, 'bill789')
        self.assertEqual(bill.total_amount, 120.0)
        self.assertEqual(bill.paid_by_user, 70.0)
        self.assertEqual(bill.who_is_paying, 'user')
        self.assertEqual(bill.friend_id, 'friend789')


if __name__ == '__main__':
    unittest.main()
