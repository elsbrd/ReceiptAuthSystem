# FastAPI Receipt Management API

This API is built using FastAPI and SQLAlchemy. It provides user registration, login, and receipt management features, including JWT-based authentication. The receipts can be viewed in both JSON and text formats.

## Table of Contents

- [Installation](#installation)
- [Running the Application](#running-the-application)
- [API Endpoints](#api-endpoints)
- [Example Requests](#example-requests)
- [Testing](#testing)

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/elsbrd/ReceiptAuthSystem.git
   cd ReceiptAuthSystem/src
   ```

2. Set up a virtual environment and activate it:

   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install the dependencies:

   ```bash
   pip install -r requirements.txt
   ```

4. Set up the environment variables:

   Create a `.env` file in the root of your project with the following variables:

   ```env
   DATABASE_URL=database_url
   SECRET_KEY=secret_key
   ACCESS_TOKEN_EXPIRE_MINUTES=30
   REFRESH_TOKEN_EXPIRE_MINUTES=10080
   ```

## Running the Application

1. Apply the migrations to set up the database schema:

   ```bash
   alembic upgrade head
   ```

2. Run the application:

   ```bash
   uvicorn src.main:app --reload
   ```

The application will be available at `http://127.0.0.1:8000`.

## API Documentation
Once the application is running, you can access the automatically generated API documentation (Swagger UI) at:

Swagger UI: `http://127.0.0.1:8000/docs`.

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/api/auth/signup` | Register a new user |
| `POST` | `/api/auth/signin` | Log in and get a JWT token |
| `POST` | `/api/receipts` | Create a new receipt |
| `GET`  | `/api/receipts` | Get the current user's receipts with optional filters and pagination |
| `GET`  | `/api/receipts/{receipt_id}` | Get a specific receipt by its ID |
| `GET`  | `/api/receipts/{public_id}/view` | View a receipt by its public ID in a text-based format |

## Example Requests

### 1. **Register User**

**POST /api/auth/signup**

```bash
curl -X 'POST' \
  'http://127.0.0.1:8000/api/auth/signup' \
  -H 'Content-Type: application/json' \
  -d '{
    "name": "John Doe",
    "username": "johndoe",
    "password": "mysecurepassword",
    "password_confirm": "mysecurepassword"
}'
```

### 2. **Login User**

**POST /api/auth/signin**

```bash
curl -X 'POST' \
  'http://127.0.0.1:8000/api/auth/signin' \
  -H 'Content-Type: application/x-www-form-urlencoded' \
  -d 'username=johndoe&password=mysecurepassword'
```

**Response:**
```json
{
  "access_token": "jwt_token",
  "refresh_token": "refresh_jwt_token",
  "token_type": "bearer"
}
```

### 3. **Create Receipt**

**POST /receipts**

```bash
curl -X 'POST' \
  'http://127.0.0.1:8000/api/receipts' \
  -H 'Authorization: Bearer <your_token>' \
  -H 'Content-Type: application/json' \
  -d '{
    "products": [
      {
        "name": "Product 1",
        "price": 10.0,
        "quantity": 2
      },
      {
        "name": "Product 2",
        "price": 15.0,
        "quantity": 1
      }
    ],
    "payment": {
      "type": "cash",
      "amount": 35.0
    }
}'
```

**Response:**
```json
{
  "id": 1,
  "public_id": "uuid_value",
  "products": [
    {
      "name": "Product 1",
      "price": 10.0,
      "quantity": 2,
      "total": 20.0
    },
    {
      "name": "Product 2",
      "price": 15.0,
      "quantity": 1,
      "total": 15.0
    }
  ],
  "payment": {
    "type": "cash",
    "amount": 35.0
  },
  "total": 35.0,
  "rest": 0.0,
  "created_at": "2024-10-09T12:34:56.789"
}
```

### 4. **Get Receipts with Filters and Pagination**

**GET /receipts**

```bash
curl -X 'GET' \
  'http://127.0.0.1:8000/api/receipts?created_after=2024-10-01&minimum_total=10' \
  -H 'Authorization: Bearer <your_token>'
```

### 5. **Get Receipt by ID**

**GET /receipts/{receipt_id}**

```bash
curl -X 'GET' \
  'http://127.0.0.1:8000/api/receipts/1' \
  -H 'Authorization: Bearer <your_token>'
```

### 6. **View Receipt by Public ID**

**GET /receipts/{public_id}/view**

```bash
curl -X 'GET' \
  'http://127.0.0.1:8000/api/receipts/your-public-id/view?line_length=32'
```

**Response:**
```
      ФОП Джонсонюк Борис       
================================
3.00 x 298 870.00               
Mavic 3T              896 610.00
--------------------------------
20.00 x 31 000.00               
Дрон FPV з
акумулятором 6S
чорний                620 000.00
================================
СУМА                1 516 610.00
Готівка             1 516 610.00
Решта                       0.00
================================
        09.10.2024 14:11        
      Дякуємо за покупку!       
```

## Testing

To run the tests, you can use `pytest`:

```bash
pytest
```