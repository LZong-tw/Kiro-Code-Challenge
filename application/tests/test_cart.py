import pytest
from domain.cart import Cart, CartItem


class TestAddItemToCart:
    def test_add_item_to_empty_cart(self):
        cart = Cart(user_id="user123")
        cart.add_item("product1", "Laptop", 999.99, 1)
        
        assert cart.item_count == 1
        assert len(cart.items) == 1
        assert cart.items[0].product_id == "product1"
        assert cart.items[0].product_name == "Laptop"
        assert cart.items[0].price == 999.99
        assert cart.items[0].quantity == 1
        assert cart.subtotal == 999.99
    
    def test_add_multiple_quantities(self):
        cart = Cart(user_id="user123")
        cart.add_item("product1", "Mouse", 25.50, 3)
        
        assert cart.item_count == 3
        assert cart.items[0].quantity == 3
        assert cart.subtotal == 76.50
    
    def test_add_same_item_increases_quantity(self):
        cart = Cart(user_id="user123")
        cart.add_item("product1", "Keyboard", 50.00, 2)
        cart.add_item("product1", "Keyboard", 50.00, 1)
        
        assert len(cart.items) == 1
        assert cart.items[0].quantity == 3
        assert cart.item_count == 3
        assert cart.subtotal == 150.00
    
    def test_add_different_items(self):
        cart = Cart(user_id="user123")
        cart.add_item("product1", "Monitor", 300.00, 1)
        cart.add_item("product2", "Cable", 15.00, 2)
        
        assert len(cart.items) == 2
        assert cart.item_count == 3
        assert cart.subtotal == 330.00


class TestRemoveItemFromCart:
    def test_remove_item_from_cart(self):
        cart = Cart(user_id="user123")
        cart.add_item("product1", "Laptop", 999.99, 1)
        cart.add_item("product2", "Mouse", 29.99, 2)
        
        cart.remove_item("product1")
        
        assert len(cart.items) == 1
        assert cart.item_count == 2
        assert cart.subtotal == 59.98
        assert cart.items[0].product_id == "product2"
    
    def test_remove_nonexistent_item(self):
        cart = Cart(user_id="user123")
        cart.add_item("product1", "Laptop", 999.99, 1)
        
        cart.remove_item("product999")
        
        assert len(cart.items) == 1
        assert cart.item_count == 1
    
    def test_remove_all_items(self):
        cart = Cart(user_id="user123")
        cart.add_item("product1", "Laptop", 999.99, 1)
        
        cart.remove_item("product1")
        
        assert len(cart.items) == 0
        assert cart.item_count == 0
        assert cart.subtotal == 0.0
