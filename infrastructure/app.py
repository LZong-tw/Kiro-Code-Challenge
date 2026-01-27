#!/usr/bin/env python3
import aws_cdk as cdk
from stacks.shopping_cart_stack import ShoppingCartStack

app = cdk.App()
ShoppingCartStack(app, "ShoppingCartStack")
app.synth()
