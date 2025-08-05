# CoreZen Solutions - Inventory Management API

This project is a solution for the CoreZen Solutions Backend Developer Internship assignment.

## The Problem

Any business that manages physical goods, from a small shop to a large warehouse, faces critical challenges: How to accurately track product information? How to prevent overselling by maintaining a real-time stock count? How to log every stock movement for auditing and analysis? A manual or unreliable system leads to lost sales, incorrect data, and operational inefficiency.

The objective of this project was to solve this by building a centralized, reliable, and fast API to serve as the single source of truth for all inventory operations.

## The Solution: An Inventory Management API

This API provides the backend foundation to solve the problems above. It allows different applications (like a warehouse management app, an e-commerce website, or a sales dashboard) to interact with a consistent and accurate inventory database.

The implementation uses FastAPI, SQLAlchemy, and Alembic to build a high-performance, asynchronous, and maintainable system with the following features:

- **Product Management**: Full CRUD functionality for products.
- **Stock Tracking**: Record stock movements which atomically update product quantities.
- **Async Operations**: Built with `async` and `await` for high performance.
- **Data Validation**: Uses Pydantic for strict request/response data validation.
- **Pagination**: List endpoints support pagination for handling large datasets.
- **Database Migrations**: Alembic handles database schema versioning safely.
- **Interactive Docs**: Automatic, interactive API documentation provided by FastAPI.

## Tech Stack

- **Framework**: FastAPI
- **ORM**: SQLAlchemy 2.0 (with `asyncio` support)
- **Database**: SQLite (via `aiosqlite`)
- **Migrations**: Alembic
- **Validation**: Pydantic
- **Server**: Uvicorn

## Setup and Installation

### Prerequisites

- Python 3.8+
- A virtual environment tool (like `venv`)

### 1. Clone the Repository

```bash
git clone [https://github.com/Gaurang2737/corezen-inventory-api.git](https://github.com/Gaurang2737/corezen-inventory-api.git)
cd corezen-inventory-api

2. Create and Activate a Virtual Environment
For macOS/Linux:

python3 -m venv venv
source venv/bin/activate

For Windows:

python -m venv venv
.\venv\Scripts\activate

3. Install Dependencies
pip install -r requirements.txt

4. Set up the Database
alembic upgrade head

Running the Application
To start the API server, run the following command from the project root:

uvicorn app.main:app --reload

The API will be available at http://127.0.0.1:8000.

API Documentation
Once the server is running, you can access the interactive API documentation at:

Swagger UI: http://127.0.0.1:8000/docs

ReDoc: http://127.0.0.1:8000/redoc

Sample API Requests (cURL)
Create a new product
curl -X 'POST' \
  '[http://127.0.0.1:8000/products/](http://127.0.0.1:8000/products/)' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "name": "Laptop Pro",
  "description": "A powerful new laptop",
  "price": 1299.99,
  "available_quantity": 50
}'

Get all products
curl -X 'GET' \
  '[http://127.0.0.1:8000/products/](http://127.0.0.1:8000/products/)' \
  -H 'accept: application/json'

Record a stock transaction
curl -X 'POST' \
  '[http://127.0.0.1:8000/stock/](http://127.0.0.1:8000/stock/)' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "product_id": 1,
  "quantity": 10,
  "transaction_type": "IN"
}'
