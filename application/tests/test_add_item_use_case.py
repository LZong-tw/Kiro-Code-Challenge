import pytest
from use_cases.add_item_to_cart import AddItemToCart, AddItemRequest
from domain.cart import Cart


class MockCartRepository:
    def __init__(self):
        self.carts = {}
    
    def get_cart(self, user_id):
        return self.carts.get(user_id)
    
    def save_cart(self, cart):
        self.carts[cart.user_id] = cart


class TestAddItemToCartUseCase:
    def test_add_item_creates_new_cart_if_not_exists(self):
        repo = MockCartRepository()
        use_case = AddItemToCart(repo)
        
        request = AddItemRequest(
            user_id="user123",
            product_id="product1",
            product_name="Laptop",
            price=999.99,
            quantity=1
        )
        
        response = use_case.execute(request)
        
        assert response.success is True
        assert response.item_count == 1
        assert response.subtotal == 999.99
        assert len(response.items) == 1
    
    def test_add_item_to_existing_cart(self):
        repo = MockCartRepository()
        existing_cart = Cart(user_id="user123")
        existing_cart.add_item("product1", "Mouse", 25.00, 1)
        repo.save_cart(existing_cart)
        
        use_case = AddItemToCart(repo)
        request = AddItemRequest(
            user_id="user123",
            product_id="product2",
            product_name="Keyboard",
            price=50.00,
            quantity=2
        )
        
        response = use_case.execute(request)
        
        assert response.success is True
        assert response.item_count == 3
        assert response.subtotal == 125.00
