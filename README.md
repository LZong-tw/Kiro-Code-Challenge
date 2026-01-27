# Shopping Cart API

A shopping cart service built with Clean Architecture and TDD approach.

## Features

✅ **Add Items to Cart** - Add products with quantity  
✅ **Remove Items from Cart** - Remove products completely

## Architecture

Clean Architecture with clear separation:

```
application/
├── domain/              # Cart, CartItem entities
├── use_cases/           # AddItemToCart, RemoveItemFromCart
├── adapters/
│   ├── repositories/    # DynamoDB adapter
│   └── api/            # Lambda handlers
└── tests/              # 11 unit tests

infrastructure/
├── stacks/             # CDK stack
└── app.py             # CDK app
```

## Setup

### Application
```bash
cd application
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Infrastructure
```bash
cd infrastructure
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Run Tests

### Unit Tests
```bash
cd application
source venv/bin/activate
pytest tests/ -v
```

### Integration Tests
```bash
cd application
source venv/bin/activate
python3 ../test_integration.py
```

This runs a complete flow test with in-memory repository (no AWS required).

## Deploy

⚠️ **Note:** Deployment requires AWS account with proper IAM permissions. See `DEPLOYMENT.md` for details.

```bash
cd infrastructure
source venv/bin/activate
cdk bootstrap  # First time only
cdk deploy
```

If deployment is blocked by IAM restrictions, see `DEPLOYMENT.md` for alternative deployment options.

## API Usage

### Add Item to Cart

**Endpoint**: `POST /cart/add-item`

**Request**:
```json
{
  "user_id": "user123",
  "product_id": "product1",
  "product_name": "Laptop",
  "price": 999.99,
  "quantity": 1
}
```

**Response**:
```json
{
  "success": true,
  "item_count": 1,
  "subtotal": 999.99,
  "items": [
    {
      "product_id": "product1",
      "product_name": "Laptop",
      "price": 999.99,
      "quantity": 1
    }
  ]
}
```

### Remove Item from Cart

**Endpoint**: `POST /cart/remove-item`

**Request**:
```json
{
  "user_id": "user123",
  "product_id": "product1"
}
```

**Response**:
```json
{
  "success": true,
  "item_count": 0,
  "subtotal": 0.0,
  "items": [],
  "message": null
}
```

## Test Results

**11 unit tests passing** ✅  
**4 integration test scenarios passing** ✅

## AWS Resources

- **API Gateway**: REST API endpoint
- **Lambda**: Python 3.11 function handlers
- **DynamoDB**: NoSQL table (partition key: user_id)
