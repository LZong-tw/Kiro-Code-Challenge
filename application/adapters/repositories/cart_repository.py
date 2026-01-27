from abc import ABC, abstractmethod
from domain.cart import Cart


class CartRepository(ABC):
    @abstractmethod
    def get_cart(self, user_id: str) -> Cart:
        pass
    
    @abstractmethod
    def save_cart(self, cart: Cart) -> None:
        pass
