# Mini E-Commerce API

A Django REST Framework based backend for a simple e-commerce platform.

## Features
- **JWT Auth:** Secure registration and login.
- **RBAC:** Separate permissions for Admins and Customers.
- **Order Logic:** Atomic transactions to ensure stock consistency.
- **Fraud Control:** Prevents stock misuse by limiting repeated cancellations.

## Tech Stack
- Python / Django
- Django REST Framework (DRF)
- SimpleJWT (Authentication)
- SQLite/PostgreSQL (Database)

## Setup Instructions
1. Clone the repository.
2. Install dependencies: `pip install -r requirements.txt`
3. Run migrations: `python manage.py migrate`
4. Create superuser: `python manage.py createsuperuser`
5. Start server: `python manage.py runserver`

## Assumptions
- A user can have only one active cart at a time.
- Orders can only be cancelled while in 'Pending' status.
- Once an order is cancelled, stock is automatically returned to the inventory.
