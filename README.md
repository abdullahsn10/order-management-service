# Order Management Service

This is a microservice for managing orders in the coffee shop, along with the menu items. It is built using FastAPI and PostgreSQL.
## Features

- Manage orders, order items, and menu items.

- Handle order lifecycle, including assignment to users (chefs).

- Generate various reports related to orders, income, etc.
## Technology Stack

- **FastAPI**: Web framework for building APIs.
- **PostgreSQL**: Relational database management system.
- **SQLAlchemy**: ORM for database interactions.
- **Alembic**: Database migrations.
- **Docker**: Containerization for development and deployment.

## Installation

1. **Clone the repository:**

   ```bash
   git clone https://github.com/abdullahsn10/order-management-service
   cd order-management-service
   ```

2. **Set up a virtual environment:**

   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

4. **Configure the environment variables:**

   Create a `.env` file in the project root and define the necessary environment variables:

   ```bash
    SQLALCHEMY_DATABASE_URL=postgresql://user:password@localhost:5432/order_service_db
    PUBLIC_KEY_PATH='path/to/public.pem'
    ALGORITHM = "RS256"
    ACCESS_TOKEN_EXPIRE_MINUTES = 30
   ```

## Environment Variables

Make sure to define the following environment variables in your `.env` file:

- `SQLALCHEMY_DATABASE_URL`: The URL for connecting to your PostgreSQL database.
- `PUBLIC_KEY_PATH`: The public key used for JWT decryption.
## Running the Application

To run the application locally:

```bash
python server.py
```

This will start the FastAPI application and serve it at `http://127.0.0.1:8888`.

## API Endpoints

### Menu Items

- `GET /menu-items/`: Get all menu items.
- `POST /menu-items/`: Create a new menu item.
- `PUT /menu-items/{menu_item_id}`: Update a specific menu item.
- `DELETE /menu-items/{menu_item_id}`: Delete a specific menu item.

### Orders

- `POST /orders/`: Place an order, specifying the customer details and order items.
- `GET /orders/`: Get all orders with pagination and optional status filter.
- `GET /orders/{order_id}`:  Get a specific order.
- `PATCH /orders/{order_id}/status`: Update the status of a specific order.
- `PATCH /orders/{order_id}/assign/{user_id}`: Assign an order to a chef.

### Reports

- `GET /reports/top-selling-items/`: List top-selling items in a given period.
- `GET /reports/customers-orders/`:  List all customers with their order count and total amount paid in a given period.
- `GET /reports/chefs-orders/`:  List all chefs with their served orders in a given period.
- `GET /reports/issuers-orders/`: List all order issuers with their issued orders in a given period.
- `GET /reports/orders-income`: Get total income from orders along with order count in a given period.


## Database Migrations

This project uses Alembic for database migrations. Follow these steps to manage migrations:

1. **Initialize Alembic** (if not already done):
   ```bash
   cd src
   alembic init migrations
   ```

   This will create an `migrations` directory with configuration files. But it is already done.

2. **Configure Alembic**:

   Edit the `alembic.ini` file and update the `sqlalchemy.url` variable with your database URL:

   ```ini
   sqlalchemy.url = postgresql://user:password@localhost:5432/coffee_shop_db
   ```

   Alternatively, you can set it in your `.env` file and configure Alembic to use it.

3. **Create a New Migration**:

   Whenever you make changes to your SQLAlchemy models, generate a new migration script:

   ```bash
   alembic revision --autogenerate -m "describe your changes"
   ```

4. **Apply Migrations**:

   To apply migrations and update the database schema, run:

   ```bash
   alembic upgrade head
   ```

5. **Downgrade Migrations**:

   If you need to revert a migration, use:

   ```bash
   alembic downgrade -1
   ```

