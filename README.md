# Mini E-Commerce API

## Setup Instructions
1. Clone the repository.
2. Install dependencies: `pip install -r requirements.txt`
3. Run migrations: `python manage.py migrate`
4. Create superuser: `python manage.py createsuperuser`
5. Start server: `python manage.py runserver`

## Tech Stack
- Python / Django
- Django REST Framework (DRF)
- SimpleJWT (Authentication)
- SQLite/PostgreSQL (Database)

## Features
- **JWT Auth:** Secure registration and login.
- **RBAC:** Separate permissions for Admins and Customers.
- **Order Logic:** Atomic transactions to ensure stock consistency.
- **Fraud Control:** Prevents stock misuse by limiting repeated cancellations.

## Assumptions
- A user can have only one active cart at a time.
- Orders can only be cancelled while in 'Pending' status.
- Once an order is cancelled, stock is automatically returned to the inventory.

## API_Information
Admin:
1. View - GET - https://ecommercebackend-apyfydev.up.railway.app/shop/products/
2. Add - POST- https://ecommercebackend-apyfydev.up.railway.app/shop/products/
3. Update - PUT- https://ecommercebackend-apyfydev.up.railway.app/shop/products/1/
4. Delete- DELETE - https://ecommercebackend-apyfydev.up.railway.app/shop/products/1/

Customer:
1. View - GET - https://ecommercebackend-apyfydev.up.railway.app/shop/products/
2. Add product to cart - POST - https://ecommercebackend-apyfydev.up.railway.app/shop/cart/add/
3. Remove product from cart - DELETE - https://ecommercebackend-apyfydev.up.railway.app/shop/cart/add/1/
4. Place order - POST - https://ecommercebackend-apyfydev.up.railway.app/shop/order/place/
5. Cancel order - https://ecommercebackend-apyfydev.up.railway.app/shop/order/<int:pk>/cancel/
6. Order status - https://ecommercebackend-apyfydev.up.railway.app/shop/order/<int:pk>/status/
