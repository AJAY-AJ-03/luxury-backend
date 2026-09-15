# Django REST API Backend

[![Backend Framework](https://img.shields.io/badge/Backend-Django%20REST%20Framework-green.svg)](https://www.django-rest-framework.org/)
[![Language](https://img.shields.io/badge/Language-Python%203.10%2B-blue.svg)](https://www.python.org/)
[![Database](https://img.shields.io/badge/Database-SQLite%20%2F%20PostgreSQL-blue.svg)](https://www.postgresql.org/)
[![Auth](https://img.shields.io/badge/Security-JWT%20Authentication-purple.svg)](https://django-rest-framework-simplejwt.readthedocs.io/)

This directory houses the backend REST API engine for the e-commerce system. Built on **Django 6** and **Django REST Framework (DRF)**, it implements core services including JWT authentication (email and phone-based), catalog categorization, paginated and filtered product indices, and media/file upload handling.

---

## Table of Contents
1. [App Structure Directory](#app-structure-directory)
2. [Local Development Setup](#local-development-setup)
3. [Django Custom User Model](#django-custom-user-model)
4. [Custom Admin Configuration](#custom-admin-configuration)
5. [Complete API Endpoints Directory](#complete-api-endpoints-directory)
6. [Database Cart App Activation Status](#database-cart-app-activation-status)
7. [Testing and Linting](#testing-and-linting)

---

## App Structure Directory

The backend codebase is divided into focused apps:

*   **`backend/`**: Django configuration, global routing (`urls.py`), and project settings (`settings.py`).
*   **`user_auth/`**: Custom user model (`User`) supporting dual email/phone authentication. Provides endpoints for registration, login, and JWT token refresh.
*   **`categories/`**: Catalog category schemas. Supports admin control for activation, custom banners, and automated URL slug generation.
*   **`products/`**: Product inventory listings. Implements search filters, ordering parameters (by price, stock, creation date), and custom pricing validation.
*   **`cart/`**: Implemented models, serializers, views, and urls for storing customer shopping carts on the database level. **Fully registered and active in local setup.**
*   **`core/`**: Shared components including the `IsAdminOrReadOnly` routing permission block and `slug.py` generator.
*   **`api/`**: Global utility configurations and system health check views.

---

## Local Development Setup

### 1. Prerequisites
Ensure you have Python 3.10+ installed on your workspace.

### 2. Install and Initialize Virtual Environment
Run the following commands inside the `backend/` directory:

```bash
# Create virtual environment
python -m venv venv

# Activate Virtual Environment
# Windows PowerShell:
.\venv\Scripts\Activate.ps1
# Mac / Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 3. Setup Environment Variables
Create a `.env` file in the `backend/` folder (or copy values to system variables) containing:

```env
SECRET_KEY=django-insecure-development-secret-key-here
DEBUG=True
ALLOWED_HOSTS=127.0.0.1,localhost
```

### 4. Database Migrations
Create databases and apply migrations:

```bash
python manage.py migrate
```

### 5. Create Administrative Superuser
Create a staff user to access the administration panel:

```bash
python manage.py create_superuser
```
*You will be prompted for: Username, Email, Phone Number, and Password.*

### 6. Launch Server
Start the development server:

```bash
python manage.py runserver
```
The API is available at: [http://127.0.0.1:8000/](http://127.0.0.1:8000/)  
The Admin dashboard is available at: [http://127.0.0.1:8000/admin/](http://127.0.0.1:8000/admin/)

---

## Django Custom User Model

The system overrides the default Django authentication scheme (`user_auth.User`) to support modern email/phone lookups:

- **Primary Identifier**: Email (`USERNAME_FIELD = 'email'`).
- **Required fields**: `username` and `phone_number`.
- **Validation**: Enforces standard phone parameters using the regex pattern `^\+?1?\d{9,15}$`.
- **Login Customization**: The `LoginSerializer` checks user input for an `@` symbol. If present, it resolves user verification via the email column; otherwise, it queries the phone number column.

---

## Custom Admin Configuration

Administration options are declared in each app's `admin.py`:

- **`User` (user_auth)**: Customizes detail layout tabs. Adds support for searching by username, email, and phone number, with list filters for `is_staff`, `is_superuser`, and `is_active`.
- **`Category` (categories)**: Lists categories by status and provides automated search setups. Slugs are auto-populated from category names.
- **`Product` (products)**: Lists products in a grid detailing the SKU, category, price, discount price, current stock, and availability status. Features list filters for category and stock levels, and search bars for name, SKU, and description.

---

## Complete API Endpoints Directory

All request and response payloads must utilize the `application/json` format.

| Path | Method | Auth Required | Purpose |
| :--- | :--- | :---: | :--- |
| `/api/health/` | `GET` | No | System health check and server status. |
| `/auth/register/` | `POST` | No | Creates a new user profile; returns JWT pair. |
| `/auth/login/` | `POST` | No | Authenticates user via email/phone; returns JWT pair. |
| `/auth/token/refresh/` | `POST` | No | Receives refresh token; returns new access token. |
| `/api/categories/` | `GET` | No | Lists active product categories. |
| `/api/categories/{slug}/` | `GET` | No | Detailed catalog profile for specific category. |
| `/api/products/` | `GET` | No | Searchable, filterable, and paginated product lists. |
| `/api/products/{slug}/` | `GET` | No | Product specifications, stock status, and prices. |
| `/api/cart/` | `GET` | Yes | Retrieves user's active database cart. Creates one if missing. |
| `/api/cart/add/` | `POST` | Yes | Appends item to cart. Validates product stock. |
| `/api/cart/items/{product_id}/` | `PATCH` / `DELETE` | Yes | Updates item quantity or removes it from database cart. |
| `/api/cart/clear/` | `POST` | Yes | Flushes all items inside user's database cart. |

---

### API Payloads & Examples

#### 1. System Health Check
*   **Request**: `GET /api/health/`
*   **Response (200 OK)**:
    ```json
    {
      "status": "ok",
      "timestamp": "2026-05-26T11:20:48.123Z"
    }
    ```

#### 2. User Login
*   **Request**: `POST /auth/login/`
*   **Body**:
    ```json
    {
      "email_or_phone": "johndoe@example.com",
      "password": "SecretPassword123"
    }
    ```
*   **Response (200 OK)**:
    ```json
    {
      "message": "Login successful.",
      "user": {
        "id": 1,
        "username": "johndoe",
        "email": "johndoe@example.com",
        "phone_number": "+1234567890",
        "first_name": "John",
        "last_name": "Doe",
        "date_joined": "2026-05-26T05:50:52Z"
      },
      "tokens": {
        "refresh": "eyJhbGciOi...",
        "access": "eyJhbGciOi..."
      }
    }
    ```

#### 3. List Products (Filtered)
*   **Request**: `GET /api/products/?category__slug=electronics&search=headphones`
*   **Response (200 OK)**:
    ```json
    {
      "count": 1,
      "next": null,
      "previous": null,
      "results": [
        {
          "id": 14,
          "category": 3,
          "category_name": "Electronics",
          "name": "Wireless Bluetooth Headphones",
          "slug": "wireless-bluetooth-headphones",
          "price": "129.99",
          "discount_price": "99.99",
          "effective_price": "99.99",
          "stock": 18,
          "image": "http://localhost:8000/media/products/headphones.jpg",
          "is_available": true,
          "sku": "HEADPH-WRLS-01",
          "created_at": "2026-05-26T05:50:52Z"
        }
      ]
    }
    ```

---

## Database Cart App Activation Status

The database-backed `cart` app is **fully integrated, registered, and active** within the server's global settings:

- **Registration**: Added `'cart'` directly inside `INSTALLED_APPS` within `backend/settings.py`.
- **Global Router**: Mounted `cart.urls` inside `backend/urls.py`.
- **Database Tables**: Schema tables `Cart` and `CartItem` are successfully migrated in PostgreSQL/SQLite.

### Cart View Specs
1. **User Ownership**: Carts maintain a strict `OneToOneField` mapping with the `User` model, assuring isolated checkout lanes.
2. **Item Mappings**: `CartItem` holds a foreign key relationship with the `Product` model, enforcing inventory limits during validation checks.
3. **Active Serializers**:
   - `CartSerializer`: Calculates cart items lists, total counts, and aggregate prices.
   - `AddCartItemSerializer`: Enforces stock restrictions during insertions.
   - `UpdateCartItemSerializer`: Enforces stock boundaries during quantity updates.

---

## Testing and Linting

- **Run Django Unit Tests**:
  ```bash
  python manage.py test
  ```
- **Filter Backend Check**:
  Ensure Pyright or other type-check configurations align with Django settings. To check django type definitions:
  ```bash
  python manage.py check
  ```
