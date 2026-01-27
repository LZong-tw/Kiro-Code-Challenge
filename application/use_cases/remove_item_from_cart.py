from dataclasses import dataclass
from typing import List, Optional
from adapters.repositories.cart_repository import CartRepository


@dataclass
class RemoveItemRequest:
    user_id: str
    product_id: str


@dataclass
class RemoveItemResponse:
    success: bool
    item_count: int
    subtotal: float
    items: List[dict]
    message: Optional[str] = None


class RemoveItemFromCart:
    def __init__(self, cart_repository: CartRepository):
        self.cart_repository = cart_repository
    
    def execute(self, request: RemoveItemRequest) -> RemoveItemResponse:
        cart = self.cart_repository.get_cart(request.user_id)
        
        if cart is None:
            return RemoveItemResponse(
                success=False,
                item_count=0,
                subtotal=0.0,
                items=[],
                message="Cart not found"
            )
        
        cart.remove_item(request.product_id)
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
        
        return RemoveItemResponse(
            success=True,
            item_count=cart.item_count,
            subtotal=cart.subtotal,
            items=items
        )
