#!/usr/bin/env python3
"""
Integration Test - Tests the complete flow without AWS deployment
Uses in-memory repository instead of DynamoDB
"""
import json
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'application'))

from domain.cart import Cart
from use_cases.add_item_to_cart import AddItemToCart, AddItemRequest
from use_cases.remove_item_from_cart import RemoveItemFromCart, RemoveItemRequest
from adapters.repositories.cart_repository import CartRepository

class InMemoryCartRepository(CartRepository):
    """In-memory implementation for testing"""
    def __init__(self):
        self.carts = {}
    
    def get_cart(self, user_id: str):
        return self.carts.get(user_id)
    
    def save_cart(self, cart: Cart):
        self.carts[cart.user_id] = cart

def test_api_flow():
    """Test the complete API flow"""
    print("Test 1: Add first item to cart")
    print("-" * 50)
    
    repo = InMemoryCartRepository()
    add_use_case = AddItemToCart(repo)
    remove_use_case = RemoveItemFromCart(repo)
    
    # Test 1: Add first item
    result = add_use_case.execute(
        AddItemRequest(
            user_id="user123",
            product_id="product1",
            product_name="Laptop",
            price=999.99,
            quantity=1
        )
    )
    
    print(f"✅ Item count: {result.item_count}")
    print(f"✅ Subtotal: ${result.subtotal}")
    print(f"✅ Items: {json.dumps(result.items, indent=2)}")
    
    assert result.item_count == 1
    assert result.subtotal == 999.99
    assert len(result.items) == 1
    
    print("\nTest 2: Add second item to cart")
    print("-" * 50)
    
    # Test 2: Add second item
    result = add_use_case.execute(
        AddItemRequest(
            user_id="user123",
            product_id="product2",
            product_name="Mouse",
            price=29.99,
            quantity=2
        )
    )
    
    print(f"✅ Item count: {result.item_count}")
    print(f"✅ Subtotal: ${result.subtotal}")
    print(f"✅ Items: {json.dumps(result.items, indent=2)}")
    
    assert result.item_count == 3  # 1 laptop + 2 mice
    assert result.subtotal == 1059.97
    assert len(result.items) == 2
    
    print("\nTest 3: Add same item (increase quantity)")
    print("-" * 50)
    
    # Test 3: Add same item
    result = add_use_case.execute(
        AddItemRequest(
            user_id="user123",
            product_id="product1",
            product_name="Laptop",
            price=999.99,
            quantity=1
        )
    )
    
    print(f"✅ Item count: {result.item_count}")
    print(f"✅ Subtotal: ${result.subtotal}")
    print(f"✅ Laptop quantity: {result.items[0]['quantity']}")
    
    assert result.item_count == 4  # 2 laptops + 2 mice
    assert result.subtotal == 2059.96
    assert result.items[0]['quantity'] == 2
    
    print("\nTest 4: Remove item from cart")
    print("-" * 50)
    
    # Test 4: Remove item
    result = remove_use_case.execute(
        RemoveItemRequest(
            user_id="user123",
            product_id="product2"
        )
    )
    
    print(f"✅ Success: {result.success}")
    print(f"✅ Item count: {result.item_count}")
    print(f"✅ Subtotal: ${result.subtotal}")
    print(f"✅ Items: {json.dumps(result.items, indent=2)}")
    
    assert result.success is True
    assert result.item_count == 2  # 2 laptops only
    assert result.subtotal == 1999.98
    assert len(result.items) == 1
    
    return True

if __name__ == "__main__":
    print("=" * 60)
    print("INTEGRATION TEST - Complete API Flow")
    print("=" * 60)
    print()
    
    try:
        success = test_api_flow()
        print()
        print("=" * 60)
        print("✅ All integration tests passed!")
        print("=" * 60)
        sys.exit(0)
    except AssertionError as e:
        print()
        print("=" * 60)
        print(f"❌ Test failed: {e}")
        print("=" * 60)
        sys.exit(1)
    except Exception as e:
        print()
        print("=" * 60)
        print(f"❌ Error: {e}")
        print("=" * 60)
        sys.exit(1)
