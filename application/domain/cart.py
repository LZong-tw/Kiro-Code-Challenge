from dataclasses import dataclass
from typing import List


@dataclass
class CartItem:
    product_id: str
    product_name: str
    price: float
    quantity: int
    
    @property
    def total(self) -> float:
        return self.price * self.quantity


class Cart:
    def __init__(self, user_id: str):
        self.user_id = user_id
        self.items: List[CartItem] = []
    
    def add_item(self, product_id: str, product_name: str, price: float, quantity: int):
        for item in self.items:
            if item.product_id == product_id:
                item.quantity += quantity
                return
        
        self.items.append(CartItem(product_id, product_name, price, quantity))
    
    def remove_item(self, product_id: str):
        self.items = [item for item in self.items if item.product_id != product_id]
    
    @property
    def item_count(self) -> int:
        return sum(item.quantity for item in self.items)
    
    @property
    def subtotal(self) -> float:
        return sum(item.total for item in self.items)
