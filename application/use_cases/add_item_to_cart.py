from dataclasses import dataclass
from typing import List, Dict
from domain.cart import Cart
from adapters.repositories.cart_repository import CartRepository


@dataclass
class AddItemRequest:
    user_id: str
    product_id: str
    product_name: str
    price: float
    quantity: int


@dataclass
class AddItemResponse:
    success: bool
    item_count: int
    subtotal: float
    items: List[Dict]


class AddItemToCart:
    def __init__(self, cart_repository: CartRepository):
        self.cart_repository = cart_repository
    
    def execute(self, request: AddItemRequest) -> AddItemResponse:
        cart = self.cart_repository.get_cart(request.user_id)
        
        if cart is None:
            cart = Cart(user_id=request.user_id)
        
        cart.add_item(
            request.product_id,
            request.product_name,
            request.price,
            request.quantity
        )
        
        self.cart_repository.save_cart(cart)
        
        items = [
            {
                "product_id": item.product_id,
                "product_name": item.product_name,
                "price": item.price,
                "quantity": item.quantity
            }
            for item in cart.items
        ]
        
        return AddItemResponse(
            success=True,
            item_count=cart.item_count,
            subtotal=cart.subtotal,
            items=items
        )
