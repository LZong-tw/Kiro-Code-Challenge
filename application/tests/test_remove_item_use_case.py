import pytest
from domain.cart import Cart
from use_cases.remove_item_from_cart import RemoveItemFromCart, RemoveItemRequest
from adapters.repositories.cart_repository import CartRepository


class InMemoryCartRepository(CartRepository):
    def __init__(self):
        self.carts = {}
    
    def get_cart(self, user_id: str):
        return self.carts.get(user_id)
    
    def save_cart(self, cart: Cart):
        self.carts[cart.user_id] = cart


class TestRemoveItemFromCartUseCase:
    def test_remove_item_from_existing_cart(self):
        repo = InMemoryCartRepository()
        cart = Cart(user_id="user123")
        cart.add_item("product1", "Laptop", 999.99, 1)
        cart.add_item("product2", "Mouse", 29.99, 2)
        repo.save_cart(cart)
        
        use_case = RemoveItemFromCart(repo)
        request = RemoveItemRequest(user_id="user123", product_id="product1")
        response = use_case.execute(request)
        
        assert response.success is True
        assert response.item_count == 2
        assert response.subtotal == 59.98
        assert len(response.items) == 1
        assert response.items[0]["product_id"] == "product2"
    
    def test_remove_item_from_nonexistent_cart(self):
        repo = InMemoryCartRepository()
        use_case = RemoveItemFromCart(repo)
        request = RemoveItemRequest(user_id="user999", product_id="product1")
        
        response = use_case.execute(request)
        
        assert response.success is False
        assert response.message == "Cart not found"
