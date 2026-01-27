from aws_cdk import (
    Stack,
    aws_dynamodb as dynamodb,
    aws_lambda as lambda_,
    aws_apigateway as apigateway,
    RemovalPolicy
)
from constructs import Construct


class ShoppingCartStack(Stack):
    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)
        
        # DynamoDB Table
        cart_table = dynamodb.Table(
            self, "CartTable",
            partition_key=dynamodb.Attribute(
                name="user_id",
                type=dynamodb.AttributeType.STRING
            ),
            billing_mode=dynamodb.BillingMode.PAY_PER_REQUEST,
            removal_policy=RemovalPolicy.DESTROY
        )
        
        # Lambda Function
        add_item_lambda = lambda_.Function(
            self, "AddItemToCartFunction",
            runtime=lambda_.Runtime.PYTHON_3_11,
            handler="adapters.api.lambda_handler.add_item_handler",
            code=lambda_.Code.from_asset("../application"),
            environment={
                "CART_TABLE_NAME": cart_table.table_name
            }
        )
        
        remove_item_lambda = lambda_.Function(
            self, "RemoveItemFromCartFunction",
            runtime=lambda_.Runtime.PYTHON_3_11,
            handler="adapters.api.lambda_handler.remove_item_handler",
            code=lambda_.Code.from_asset("../application"),
            environment={
                "CART_TABLE_NAME": cart_table.table_name
            }
        )
        
        cart_table.grant_read_write_data(add_item_lambda)
        cart_table.grant_read_write_data(remove_item_lambda)
        
        # API Gateway
        api = apigateway.RestApi(
            self, "ShoppingCartApi",
            rest_api_name="Shopping Cart API"
        )
        
        cart_resource = api.root.add_resource("cart")
        add_item_resource = cart_resource.add_resource("add-item")
        remove_item_resource = cart_resource.add_resource("remove-item")
        
        add_item_resource.add_method(
            "POST",
            apigateway.LambdaIntegration(add_item_lambda)
        )
        
        remove_item_resource.add_method(
            "POST",
            apigateway.LambdaIntegration(remove_item_lambda)
        )
