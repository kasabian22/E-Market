# EMarket REST API

[![Django Version](https://img.shields.io/badge/Django-6.0-0C4B33?logo=django&logoColor=white)](https://www.djangoproject.com/)
[![DRF Version](https://img.shields.io/badge/DRF-3.17-red?logo=django&logoColor=white)](https://www.django-rest-framework.org/)
[![JWT Auth](https://img.shields.io/badge/Auth-SimpleJWT-orange)](https://django-rest-framework-simplejwt.readthedocs.io/)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg?logo=python&logoColor=white)](https://www.python.org/)

A modular, scalable eCommerce backend REST API built with Django and Django REST Framework. EMarket provides a complete foundation for online retail applications, including custom email-based authentication, token-based security, product catalog with advanced search/filtering, automated rating calculations, and inventory-aware order processing.

---

## Table of Contents

- [Overview](#overview)
- [Key Features](#key-features)
- [Tech Stack](#tech-stack)
- [Project Architecture](#project-architecture)
- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
  - [Environment Configuration](#environment-configuration)
  - [Database Setup & Migrations](#database-setup--migrations)
  - [Running the Server](#running-the-server)
- [API Overview & Quick Usage](#api-overview--quick-usage)
  - [Authentication](#authentication)
  - [Product Catalog & Reviews](#product-catalog--reviews)
  - [Order Processing](#order-processing)
- [Running Tests](#running-tests)
- [Documentation & Support](#documentation--support)
- [Contributing](#contributing)
- [Maintainers](#maintainers)
- [License](#license)

---

## Overview

EMarket REST API serves as the backend engine for modern e-commerce platforms. Designed following RESTful principles, clean architecture, and Django best practices, it simplifies user account onboarding, catalog browsing, shopping cart checkout, and review management while keeping responses fast, standardized, and secure.

---

## Key Features

- **Email-Based Custom Authentication**: Uses email as the primary login credential with `rest_framework_simplejwt` for secure stateless JWT authentication.
- **Account & Password Management**: Includes user registration, profile management, and secure token-based password reset via automated email links.
- **Product Catalog & Categorization**: Products structured across categories (`Computers`, `Food`, `Kids`, `Home`) with stock tracking and pagination (12 items per page).
- **Dynamic Search & Filtering**: Multi-parameter search using `django-filter` supporting keyword search, category, brand, and custom price ranges (`minPrice`, `maxPrice`).
- **Review & Rating Aggregation**: Users can rate and review products; overall product ratings are automatically recalculated and updated dynamically on review creation, edit, or deletion.
- **Order Lifecycle & Inventory Management**: Handles order placement with multiple payment methods (`COD`, `CARD`) and statuses (`Processing`, `Shipped`, `Delivered`). Placing an order automatically deducts stock from inventory in real-time.
- **Uniform Error Handling**: Custom JSON 404 and 500 error handlers for consistent JSON API responses across all endpoints.

---

## Tech Stack

- **Backend Framework**: [Django 6.0](https://www.djangoproject.com/)
- **API Toolkit**: [Django REST Framework 3.17](https://www.django-rest-framework.org/)
- **Authentication**: `djangorestframework-simplejwt` (JSON Web Tokens)
- **Query Filtering**: `django-filter`
- **Database**: SQLite (default for development; easily swappable with PostgreSQL or MySQL)
- **Email Service**: SMTP integration (configured for Mailtrap in development)

---

## Project Architecture

```text
REST_API_Project/
├── emarket/                  # Core Django project root
│   ├── account/              # Authentication, custom user model, and profiles
│   ├── project/              # Product catalog, categories, filters, and reviews
│   ├── order/                # Shopping orders, order items, and stock tracking
│   ├── utils/                # Custom JSON exception and error handlers
│   ├── emarket/              # Project settings, routing, and WSGI/ASGI entrypoints
│   ├── postman/              # Postman API workspace definitions
│   ├── db.sqlite3            # SQLite development database
│   └── manage.py             # Django CLI management script
├── .env.example              # Sample environment configuration template
├── .gitignore                # Git ignore patterns
├── CONTRIBUTING.md           # Contribution guidelines
├── LICENSE                   # MIT License
└── requirements.txt          # Production and development dependencies
```

---

## Getting Started

Follow these steps to set up and run the project locally.

### Prerequisites

- **Python 3.10+** installed on your system.
- **pip** (Python package manager).
- **Git** version control.

### Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/<your-username>/REST_API_Project.git
   cd REST_API_Project
   ```

2. **Create and activate a virtual environment**:
   - On Windows (PowerShell):
     ```powershell
     python -m venv venv
     .\venv\Scripts\Activate.ps1
     ```
   - On macOS/Linux:
     ```bash
     python3 -m venv venv
     source venv/bin/activate
     ```

3. **Install project dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

### Environment Configuration

Copy the example environment file and customize your settings if needed:

```bash
# Windows
copy .env.example .env

# macOS / Linux
cp .env.example .env
```

Ensure your email credentials in `emarket/emarket/settings.py` or `.env` match your SMTP provider (e.g., [Mailtrap](https://mailtrap.io/) for development password resets).

### Database Setup & Migrations

Apply database migrations to set up the database schema:

```bash
python emarket/manage.py migrate
```

Create a superuser account for administration access:

```bash
python emarket/manage.py createsuperuser
```

### Running the Server

Start the Django development server:

```bash
python emarket/manage.py runserver
```

The API will be accessible at: `http://127.0.0.1:8000/`  
The Django Admin interface is at: `http://127.0.0.1:8000/admin/`

---

## API Overview & Quick Usage

All API endpoints are prefixed with `/api/`. Below is a high-level overview of core routes and sample requests.

### Authentication

| Method | Endpoint | Description | Access |
|---|---|---|---|
| `POST` | `/api/register/` | Register a new user | Public |
| `POST` | `/api/token/` | Obtain JWT access & refresh tokens | Public |
| `GET` | `/api/userinfo/` | Get current user profile | Authenticated |
| `PUT` | `/api/userinfo/update/` | Update profile information | Authenticated |
| `POST` | `/api/forgot_password/` | Send password reset email | Public |
| `POST` | `/api/reset_password/<token>/` | Reset password using token | Public |

#### Example: Obtain JWT Token

```bash
curl -X POST http://127.0.0.1:8000/api/token/ \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "password": "yourpassword"
  }'
```

Response:
```json
{
  "refresh": "<refresh_token>",
  "access": "<access_token>"
}
```

> **Note**: For protected endpoints, pass the access token in the `Authorization` header:  
> `Authorization: Bearer <access_token>`

---

### Product Catalog & Reviews

| Method | Endpoint | Description | Access |
|---|---|---|---|
| `GET` | `/api/products/` | List products with pagination & filters | Public |
| `GET` | `/api/products/<id>` | Retrieve product details by ID | Public |
| `POST` | `/api/products/new/` | Create a new product | Admin |
| `PUT` | `/api/products/update/<id>` | Update product details | Admin / Creator |
| `DELETE` | `/api/products/delete/<id>` | Remove a product | Admin / Creator |
| `POST` | `/api/products/review/<id>` | Add or update a product review | Authenticated |
| `DELETE` | `/api/products/review/delete/<id>` | Delete your product review | Authenticated |

#### Example: Filter Products

Filter by keyword, price range, and category:

```bash
curl -X GET "http://127.0.0.1:8000/api/products/?keyword=laptop&minPrice=300&maxPrice=1500&category=Computers"
```

---

### Order Processing

| Method | Endpoint | Description | Access |
|---|---|---|---|
| `POST` | `/api/orders/new/` | Place a new order (auto updates stock) | Authenticated |
| `GET` | `/api/orders/` | List orders | Authenticated |
| `GET` | `/api/order/<id>/` | Get order details | Authenticated |
| `PUT` | `/api/order/<id>/edit/` | Update order status | Admin |
| `DELETE` | `/api/order/<id>/delete/` | Cancel / delete an order | Authenticated |

#### Example: Create an Order

```bash
curl -X POST http://127.0.0.1:8000/api/orders/new/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <access_token>" \
  -d '{
    "city": "Metropolis",
    "zip_code": "10001",
    "street": "123 Main St",
    "state": "NY",
    "country": "USA",
    "phone_number": "+1234567890",
    "order_Items": [
      {
        "product": 1,
        "quantity": 2,
        "price": 29.99
      }
    ]
  }'
```

---

## Running Tests

EMarket includes automated tests to verify routing, API responses, and custom error handlers.

Run all tests using `manage.py`:

```bash
python emarket/manage.py test
```

To run tests for an individual app:

```bash
python emarket/manage.py test project
python emarket/manage.py test account
python emarket/manage.py test order
```

---

## Documentation & Support

- **API Testing Workspace**: Postman resources and configuration can be found in the [emarket/postman](emarket/postman) directory.
- **Reporting Issues**: Found a bug or have a feature suggestion? Open an issue on GitHub Issues.
- **Framework Documentation**:
  - [Django Documentation](https://docs.djangoproject.com/)
  - [Django REST Framework Documentation](https://www.django-rest-framework.org/)
  - [Simple JWT Documentation](https://django-rest-framework-simplejwt.readthedocs.io/)

---

## Contributing

We welcome community contributions to EMarket! For detailed instructions on branching, coding conventions, testing, and submitting pull requests, please read [CONTRIBUTING.md](CONTRIBUTING.md).

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## Maintainers

EMarket is maintained by:

- **Project Lead**: [@ProjectMaintainer](https://github.com/)
- Built and maintained with contributions from the open source community.

---

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

