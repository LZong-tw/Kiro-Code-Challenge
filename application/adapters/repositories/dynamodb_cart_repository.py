import os
import boto3
from typing import Optional
from domain.cart import Cart, CartItem
from adapters.repositories.cart_repository import CartRepository


class DynamoDBCartRepository(CartRepository):
    def __init__(self, table_name: str):
        self.dynamodb = boto3.resource('dynamodb')
        self.table = self.dynamodb.Table(table_name)
    
    def get_cart(self, user_id: str) -> Optional[Cart]:
        response = self.table.get_item(Key={'user_id': user_id})
        
        if 'Item' not in response:
            return None
        
        item = response['Item']
        cart = Cart(user_id=user_id)
        
        for cart_item in item.get('items', []):
            cart.items.append(CartItem(
                product_id=cart_item['product_id'],
                product_name=cart_item['product_name'],
                price=float(cart_item['price']),
                quantity=int(cart_item['quantity'])
            ))
        
        return cart
    
    def save_cart(self, cart: Cart) -> None:
        items = [
            {
                'product_id': item.product_id,
                'product_name': item.product_name,
                'price': str(item.price),
                'quantity': item.quantity
            }
            for item in cart.items
        ]
        
        self.table.put_item(Item={
            'user_id': cart.user_id,
            'items': items
        })
