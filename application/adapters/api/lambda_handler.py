import json
import os
from use_cases.add_item_to_cart import AddItemToCart, AddItemRequest
from use_cases.remove_item_from_cart import RemoveItemFromCart, RemoveItemRequest
from adapters.repositories.dynamodb_cart_repository import DynamoDBCartRepository


def add_item_handler(event, context):
    table_name = os.environ['CART_TABLE_NAME']
    repository = DynamoDBCartRepository(table_name)
    use_case = AddItemToCart(repository)
    
    body = json.loads(event['body'])
    
    request = AddItemRequest(
        user_id=body['user_id'],
        product_id=body['product_id'],
        product_name=body['product_name'],
        price=float(body['price']),
        quantity=int(body['quantity'])
    )
    
    response = use_case.execute(request)
    
    return {
        'statusCode': 200,
        'headers': {'Content-Type': 'application/json'},
        'body': json.dumps({
            'success': response.success,
            'item_count': response.item_count,
            'subtotal': response.subtotal,
            'items': response.items
        })
    }


def remove_item_handler(event, context):
    table_name = os.environ['CART_TABLE_NAME']
    repository = DynamoDBCartRepository(table_name)
    use_case = RemoveItemFromCart(repository)
    
    body = json.loads(event['body'])
    
    request = RemoveItemRequest(
        user_id=body['user_id'],
        product_id=body['product_id']
    )
    
    response = use_case.execute(request)
    
    return {
        'statusCode': 200 if response.success else 404,
        'headers': {'Content-Type': 'application/json'},
        'body': json.dumps({
            'success': response.success,
            'item_count': response.item_count,
            'subtotal': response.subtotal,
            'items': response.items,
            'message': response.message
        })
    }


# Keep backward compatibility
handler = add_item_handler
