# Deployment Guide

## Current Status

✅ **Application Built & Tested**
- All 6 unit tests passing
- Clean Architecture implemented
- TDD approach followed (Red-Green-Refactor)
- CDK infrastructure code complete
- CloudFormation template successfully synthesized

⚠️ **Deployment Blocked**
- AWS account has IAM restrictions (WSParticipantRole)
- Explicit deny policies prevent CDK/CloudFormation operations

## What's Ready

### Application Code
- Domain entities: `Cart`, `CartItem`
- Use case: `AddItemToCart`
- Repository: `DynamoDBCartRepository`
- API handler: Lambda function handler
- All tests passing

### Infrastructure Code
- DynamoDB table definition
- Lambda function with proper IAM roles
- API Gateway REST API with `/cart/add-item` endpoint
- CloudFormation template generated successfully

## Deployment Options

### Option 1: Use an AWS Account with Proper Permissions

Required IAM permissions:
```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "cloudformation:*",
        "dynamodb:*",
        "lambda:*",
        "apigateway:*",
        "iam:CreateRole",
        "iam:AttachRolePolicy",
        "iam:PutRolePolicy",
        "s3:*",
        "ssm:GetParameter"
      ],
      "Resource": "*"
    }
  ]
}
```

**Steps:**
```bash
cd infrastructure
source venv/bin/activate

# Bootstrap CDK (first time only)
cdk bootstrap

# Deploy
cdk deploy

# Output will show API Gateway endpoint
```

### Option 2: Manual Resource Creation

If you have limited permissions but can create individual resources:

1. **Create DynamoDB Table:**
```bash
aws dynamodb create-table \
  --table-name ShoppingCart \
  --attribute-definitions AttributeName=user_id,AttributeType=S \
  --key-schema AttributeName=user_id,KeyType=HASH \
  --billing-mode PAY_PER_REQUEST \
  --region ap-northeast-1
```

2. **Package Lambda Code:**
```bash
cd application
zip -r function.zip domain/ use_cases/ adapters/ -x "**/__pycache__/*" "**/*.pyc"
```

3. **Create Lambda Function:**
```bash
aws lambda create-function \
  --function-name AddItemToCart \
  --runtime python3.11 \
  --role <LAMBDA_EXECUTION_ROLE_ARN> \
  --handler adapters.api.lambda_handler.handler \
  --zip-file fileb://function.zip \
  --environment Variables={CART_TABLE_NAME=ShoppingCart} \
  --region ap-northeast-1
```

4. **Create API Gateway** (via AWS Console or CLI)

### Option 3: Use AWS Console

1. Go to AWS Console
2. Create DynamoDB table manually
3. Create Lambda function (upload zip file)
4. Create API Gateway REST API
5. Connect API Gateway to Lambda

## Testing After Deployment

Once deployed, test the API:

```bash
# Get the API endpoint from CDK output or AWS Console
API_ENDPOINT="https://xxxxx.execute-api.ap-northeast-1.amazonaws.com/prod"

# Test add item to cart
curl -X POST ${API_ENDPOINT}/cart/add-item \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": "user123",
    "product_id": "product1",
    "product_name": "Laptop",
    "price": 999.99,
    "quantity": 1
  }'
```

Expected response:
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

## Current IAM Restrictions

The current AWS account (WSParticipantRole) has explicit deny policies for:
- `cloudformation:CreateChangeSet`
- `ssm:GetParameter`
- `dynamodb:ListTables`
- `lambda:ListFunctions`

These restrictions prevent automated deployment via CDK.

## Next Steps

1. **Contact AWS account administrator** to request deployment permissions
2. **Use a different AWS account** with proper permissions
3. **Deploy manually** using AWS Console if CLI permissions are restricted
4. **Use AWS CloudShell** if available in your account (may have different permissions)
