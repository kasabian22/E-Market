# ElectroStore — Django E-Commerce Project Plan

> **Purpose:** Build a simple, single-vendor electronics e-commerce website as a learning project using Django, Django REST Framework (DRF), HTML, CSS, and vanilla JavaScript.
>
> **Important working rule for Antigravity:** Act as a patient programming tutor and project mentor—not an automatic code generator. The developer is a junior developer and must learn by doing. Do not write the entire application, an entire feature, or complete files on the developer's behalf. Guide the developer through small steps, explain concepts, ask them to think and try, and review their work.

---

## 1. Project Goal and Scope

Build **ElectroStore**, a basic online store that sells electronics. It is a **single-vendor** store with two roles:

- **Customer:** Browse products, register, log in, manage a cart, place orders, and view their own orders.
- **Administrator:** Manage categories, products, stock, and orders through Django Admin.

### MVP features

1. Product catalog with categories, product details, images, and specifications.
2. Product search, category filtering, sorting, and pagination.
3. Customer registration, login, logout, and account information.
4. Shopping cart: add items, update quantities, remove items, and view totals.
5. Checkout with customer and delivery details.
6. Cash on Delivery (COD) as the initial payment method.
7. Order confirmation, order history, and order details.
8. Admin management of categories, products, inventory, and order statuses.

### Explicitly postpone

Do not add these to the first version unless the developer later requests them:

- Online payment gateways and payment processing.
- Coupons, discounts, reviews, ratings, wishlist, and product comparison.
- Multiple sellers, warehouses, or advanced inventory systems.
- Product recommendation systems and real-time notifications.
- Anonymous shopping carts.
- React, microservices, Docker/Kubernetes, Redis, Celery, or other infrastructure not required by the MVP.

Keep the project intentionally small. Prefer the simplest design that correctly supports the requirements.

---

## 2. Recommended Architecture

Use one Django project and serve the frontend from Django templates/static files. The frontend calls the DRF API with JavaScript `fetch()`.

**Request flow:**

`HTML/CSS/Vanilla JS → HTTP request (JSON) → Django REST Framework → Django models/business logic → Database`

### Technology choices

- **Backend:** Django.
- **API:** Django REST Framework.
- **Frontend:** Django templates, HTML, CSS, and vanilla JavaScript.
- **Database:** SQLite during early development; PostgreSQL for production.
- **Authentication:** Django's built-in authentication with session-based authentication for the same-origin frontend/API setup.
- **Admin interface:** Django Admin; do not build a separate custom admin dashboard for the MVP.
- **API testing:** DRF browsable API and/or Postman/Insomnia.
- **Version control:** Git and GitHub throughout development.

Because the frontend and API share the same origin, session authentication is a simple starting point. Protect unsafe requests (POST, PATCH, PUT, DELETE) with CSRF tokens. Do not introduce token/JWT authentication unless there is a real requirement, such as a separate frontend domain or mobile client.

---

## 3. Database Design

Design and understand the relationships before implementing serializers or API endpoints.

Use Django's built-in `User` model initially. Do not create a custom user model unless there is a clear requirement. If a custom user model is needed, decide before the first migrations.

### Models

#### 3.1 Category

Suggested fields:

- `id` — primary key.
- `name` — category name.
- `slug` — URL-friendly unique value.
- `description` — optional description.

Relationship: one Category has many Products.

#### 3.2 Product

Suggested fields:

- `id`.
- `category` — foreign key to Category.
- `name`.
- `slug` — unique URL-friendly value.
- `brand`.
- `description`.
- `price` — use `DecimalField`, never float for money.
- `stock_quantity` — available inventory; must not become negative.
- `image` — main product image (`ImageField`).
- `is_active` — whether the product is available for sale.
- `created_at` and `updated_at`.

Do not hard-delete products that are referenced by historical orders. Prefer deactivation, or use a suitable protected relationship.

#### 3.3 ProductSpecification

Use this optional-but-recommended model because electronics have different specifications.

Suggested fields:

- `product` — foreign key to Product.
- `name` — e.g. RAM, Storage, Processor, Screen Size.
- `value` — e.g. 16 GB, 512 GB SSD, Ryzen 7.

A product can have many specifications. Avoid adding a separate database field for every possible specification.

#### 3.4 Cart

Suggested fields:

- `id`.
- `user` — one-to-one relationship with User.
- `created_at` and `updated_at`.

For the MVP, each registered customer has one cart.

#### 3.5 CartItem

Suggested fields:

- `id`.
- `cart` — foreign key to Cart.
- `product` — foreign key to Product.
- `quantity` — positive integer.

Add a database uniqueness constraint on `(cart, product)` so the same product appears only once in a cart. Adding the same product again should update its quantity.

#### 3.6 Order

Suggested fields:

- `id`.
- `order_number` — unique customer-facing reference.
- `user` — foreign key to User.
- `status` — choices such as Pending, Confirmed, Processing, Shipped, Delivered, Cancelled.
- `subtotal`.
- `shipping_fee`.
- `total_amount`.
- `customer_name`.
- `phone_number`.
- `city`.
- `address`.
- `notes` — optional delivery instructions.
- `created_at`.

Copy the shipping details into the Order when it is created. Do not rely on a customer's current profile/address for historical orders, because the customer may change their information later.

No separate Payment model is needed for the initial COD-only version.

#### 3.7 OrderItem

Suggested fields:

- `id`.
- `order` — foreign key to Order.
- `product` — reference to Product, with deletion behavior that protects order history.
- `product_name` — snapshot of the product name at purchase time.
- `unit_price` — snapshot of the price at purchase time.
- `quantity`.

Store product name and unit price snapshots. Historical orders must not change when the current product name or price changes.

### Main relationships

- Category **1 → many** Product.
- Product **1 → many** ProductSpecification.
- User **1 → 1** Cart.
- Cart **1 → many** CartItem.
- Product **1 → many** CartItem.
- User **1 → many** Order.
- Order **1 → many** OrderItem.
- Product **1 → many** OrderItem.

### Database concepts to learn

Primary keys, foreign keys, one-to-one and one-to-many relationships, unique constraints, `DecimalField`, `ImageField`, `choices`, `on_delete`, migrations, QuerySets, model validation, and database transactions.

### Core data rules

- Use `DecimalField` for every money value.
- Quantities must be positive.
- Stock must never become negative.
- Validate prices and stock on the backend.
- Do not trust prices or totals submitted by JavaScript.
- Keep each user's cart and orders private to that user.

---

## 4. Django Project and App Structure

Create one Django project and these focused apps:

- `catalog` — Category, Product, ProductSpecification, catalog API.
- `accounts` — registration and account-related endpoints; use Django's built-in authentication.
- `cart` — Cart, CartItem, cart API.
- `orders` — Order, OrderItem, checkout, order API.

A possible high-level layout:

```text
ElectroStore/
├── config/
│   ├── settings.py
│   ├── urls.py
│   └── ...
├── catalog/
│   ├── models.py
│   ├── serializers.py
│   ├── views.py
│   ├── urls.py
│   └── admin.py
├── accounts/
│   ├── serializers.py
│   ├── views.py
│   ├── urls.py
│   └── ...
├── cart/
│   ├── models.py
│   ├── serializers.py
│   ├── views.py
│   ├── urls.py
│   └── admin.py
├── orders/
│   ├── models.py
│   ├── serializers.py
│   ├── views.py
│   ├── urls.py
│   └── admin.py
├── templates/
├── static/
│   ├── css/
│   ├── js/
│   └── images/
├── media/
├── manage.py
├── requirements.txt
└── README.md
```

This is a suggestion, not a rigid rule. Keep files and responsibilities understandable; do not create extra layers or folders without a reason.

### Initial dependencies

Start with only:

- Django.
- Django REST Framework.
- Pillow (for image handling).

Add packages only when a feature requires them.

Configure installed apps, database, static files, media files, timezone/language, and DRF settings. Start with SQLite and move to PostgreSQL before production deployment.

---

## 5. Build Phases and Required Order

Follow these milestones in order. Finish and test a milestone before moving on.

### Milestone 1 — Requirements and database design

1. Confirm the MVP scope.
2. Write basic customer/admin user stories.
3. Draw an ERD for the models and relationships.
4. Decide model fields, constraints, and deletion behavior.

**Deliverable:** Requirements list and database diagram.

### Milestone 2 — Project setup and models

1. Create the Django project and four apps.
2. Install and configure Django REST Framework.
3. Configure the database and media/static settings.
4. Implement models in dependency order: Category → Product → ProductSpecification → Cart → CartItem → Order → OrderItem.
5. Create and apply migrations.
6. Add sample data and inspect relationships in Django shell/Admin.

**Deliverable:** Working database and understandable model relationships.

### Milestone 3 — Django Admin

Configure admin pages to:

- Manage categories.
- Add/edit/deactivate products and upload images.
- Search and filter products by category/availability.
- View stock quantities.
- View orders, customers, dates, totals, statuses, and order items.
- Update order status.

Create a superuser and test the admin workflow.

**Deliverable:** Store data can be managed without a custom admin frontend.

### Milestone 4 — Product catalog API

First understand the DRF request flow:

`Model → Serializer → View → URL → HTTP response`

Learn serializers, validation, APIView, generic views, ModelViewSet, routers, permissions, filtering, and pagination. Use generic views for straightforward endpoints; use ViewSets where they genuinely simplify CRUD.

Suggested endpoints:

| Method | Endpoint | Purpose |
|---|---|---|
| GET | `/api/categories/` | List categories |
| GET | `/api/categories/<id>/` | Category details |
| GET | `/api/products/` | List active products |
| GET | `/api/products/<slug>/` | Product details |

The product listing should support:

- Search by product name and brand (description optionally).
- Filtering by category and availability.
- Ordering by price ascending/descending and newest.
- Pagination, e.g. 12 products per page.

Product list responses should contain only card data: ID, name, slug, price, image, brand, category, and availability. Product detail responses can additionally contain full description and specifications. Do not expose every model field by default.

**Deliverable:** Tested read-only catalog API returning JSON.

### Milestone 5 — Authentication and permissions

Implement:

- Registration.
- Login.
- Logout.
- Current-user/account endpoint.

Use Django's authentication functions/system. Learn `authenticate()`, `login()`, `logout()`, `request.user`, DRF authentication classes, permission classes, and CSRF protection.

Permission rules:

| Resource/action | Access |
|---|---|
| Catalog and categories | Public read access |
| Registration and login | Public |
| Cart | Authenticated owner only |
| Checkout | Authenticated customer only |
| Orders | Authenticated owner only |
| Admin operations | Staff/admin only |

Ensure a customer cannot access another customer's cart or order by changing an ID in the URL. Enforce this on the backend through permissions and user-filtered querysets, not by hiding frontend links.

**Deliverable:** Working customer accounts and tested access restrictions.

### Milestone 6 — Shopping cart API

Suggested endpoints:

| Method | Endpoint | Purpose |
|---|---|---|
| GET | `/api/cart/` | Retrieve current user's cart |
| POST | `/api/cart/items/` | Add a product |
| PATCH | `/api/cart/items/<id>/` | Change quantity |
| DELETE | `/api/cart/items/<id>/` | Remove an item |

When adding an item:

1. Identify the authenticated user.
2. Retrieve or create their cart.
3. Validate that the product exists and is active.
4. Check availability and requested quantity.
5. Update the existing CartItem or create one.
6. Return the updated cart.

When updating/removing, ensure the item belongs to the current user's cart. Quantity must be at least one and must not exceed available stock.

Calculate item subtotals and cart subtotal on the backend. The frontend may display the values, but it must not be trusted to determine purchase totals.

**Deliverable:** Customers can manage their own cart through the API.

### Milestone 7 — Checkout and orders API

Suggested endpoints:

| Method | Endpoint | Purpose |
|---|---|---|
| POST | `/api/orders/` | Create an order from current cart |
| GET | `/api/orders/` | List current user's orders |
| GET | `/api/orders/<id>/` | Retrieve an owned order |

The checkout request should contain delivery/contact information, not a trusted item list, unit prices, or total. The backend must read the customer's cart and retrieve current product prices itself.

Order creation workflow:

1. Validate shipping/contact information.
2. Retrieve the current user's cart.
3. Reject an empty cart.
4. Check that every product is active and has enough stock.
5. Calculate subtotal, shipping fee, and total on the backend.
6. Create the Order with a snapshot of delivery information.
7. Create OrderItems with product-name and unit-price snapshots.
8. Decrease stock.
9. Clear the cart.
10. Return order confirmation.

Use `transaction.atomic()` so an error does not leave a partial order, partially updated stock, or partially cleared cart. Learn about `select_for_update()` for safer handling of simultaneous purchases of limited stock. Keep the first implementation understandable; add concurrency handling with guidance when the developer reaches this phase.

Order statuses: Pending, Confirmed, Processing, Shipped, Delivered, Cancelled.

For cancellation, define and implement a clear stock-restoration rule. Ensure stock is restored only once; repeated cancellation/status updates must not restore stock multiple times. Do not allow customers to set their own order status.

**Deliverable:** Complete COD purchase workflow and order history.

### Milestone 8 — Frontend

Use Django templates, HTML, CSS, and vanilla JavaScript. Keep the frontend same-origin with the API for the initial version. Use `fetch()` for API communication.

Suggested pages:

1. Home — navigation, hero, categories, featured/latest products, footer.
2. Product listing — product grid, search, filters, sorting, pagination.
3. Product detail — image, name, price, description, specifications, stock, quantity, add-to-cart.
4. Cart — line items, quantity controls, remove actions, subtotal, checkout link.
5. Checkout — customer/contact/address form, order summary, COD, place-order action.
6. Registration and login.
7. Account/order history.
8. Order detail/confirmation.

Suggested frontend structure:

```text
templates/
    base.html
    home.html
    products.html
    product_detail.html
    cart.html
    checkout.html
    login.html
    register.html
    orders.html
    order_detail.html

static/
    css/style.css
    js/api.js
    js/products.js
    js/product_detail.js
    js/cart.js
    js/checkout.js
    js/auth.js
    js/orders.js
    images/
```

Build in this order:

1. Base template, navigation, footer, and shared layout.
2. Homepage.
3. Product listing connected to API.
4. Search/filter/sort/pagination.
5. Product details.
6. Registration/login.
7. Cart.
8. Checkout and order creation.
9. Order history and details.
10. Loading, empty, error, and success states.
11. Responsive/mobile styling.

Learn Fetch API, promises, async/await, JSON, HTTP methods/status codes, DOM manipulation, event listeners, form handling, and error handling. Send CSRF tokens with unsafe session-authenticated requests.

**Deliverable:** A responsive customer-facing store connected to the API.

### Milestone 9 — Testing and security

Write tests as each feature is developed; do not wait until the entire application is complete. Use Django TestCase and DRF APIClient/APITestCase as appropriate. Test both successful and failing cases.

Minimum test coverage checklist:

- Categories/products can be retrieved.
- Product filtering, search, ordering, and pagination work.
- Invalid prices and negative stock are rejected.
- Registration/login/logout work.
- Unauthenticated users cannot access private endpoints.
- One customer cannot access another customer's cart or orders.
- Adding the same product updates its cart quantity rather than creating duplicates.
- Cart quantities cannot exceed stock.
- Empty-cart checkout is rejected.
- Inactive/out-of-stock products cannot be purchased.
- Backend-calculated prices/totals are used.
- Historical order snapshots remain unchanged after product edits.
- Checkout updates stock and clears the cart atomically.
- Cancellation restores stock only once.
- Frontend handles loading, empty, validation-error, and success responses.
- Responsive layouts work on mobile and desktop.

Security essentials:

- Keep Django password hashing/authentication.
- Protect unsafe requests with CSRF.
- Enforce ownership and staff permissions on the backend.
- Validate all input server-side.
- Never trust frontend prices, totals, quantities, or order status.
- Validate image file types and sizes.
- Keep secret keys and credentials out of Git.
- Use HTTPS in production.

**Deliverable:** An application with tested core workflows and permissions.

### Milestone 10 — Deployment and documentation

Before deployment:

- Switch to PostgreSQL.
- Use environment variables for secrets and configuration.
- Set `DEBUG=False` and configure `ALLOWED_HOSTS`.
- Configure production static/media file handling.
- Configure HTTPS.
- Apply migrations and create an admin account.
- Test production authentication, permissions, images, and checkout.
- Plan database backups.

Learn the purpose of WSGI/ASGI, production application servers, static vs media files, environment variables, migrations, and database backups. Do not add Docker or orchestration tools unless there is a real reason.

README should include project overview, features, stack, database diagram, API endpoints, setup instructions, screenshots, and deployment URL.

**Deliverable:** A deployed and documented E-Commerce application.

---

## 6. AI Tutor Rules — MUST FOLLOW

The developer is using this project to learn. Your role is to teach, guide, review, and help debug—not to take over implementation.

### 6.1 Never do the whole project for the developer

- **Do not write the entire project code.**
- **Do not generate a complete application or complete feature in one response.**
- Do not create or replace multiple files with a finished implementation unless the developer explicitly asks for a narrowly scoped code change after attempting it.
- Do not automatically implement every milestone. Work only on the current small step the developer is tackling.
- Do not provide a large copy-paste solution as the default answer.

### 6.2 Teach before showing solutions

When the developer asks how to implement something:

1. Briefly explain the underlying concept and why it is needed.
2. Break the task into small, ordered steps.
3. Ask the developer to attempt the next step when practical.
4. Give a hint or point to the relevant Django/DRF concept or documentation.
5. Review the developer's attempt and explain what is correct, what is wrong, and why.

Prefer Socratic questions and progressive hints. Ask one focused question at a time; do not overwhelm the developer with a questionnaire.

### 6.3 Do not give the direct answer immediately

When the developer is stuck:

- Start with a conceptual hint, not the finished code.
- If that is insufficient, give a more specific hint or pseudocode.
- Only provide a small illustrative code snippet when necessary, and explain each relevant line.
- Do not reveal the complete solution unless the developer explicitly asks for it after trying, and even then keep the answer scoped to the exact issue.

The goal is for the developer to write and understand the code themselves.

### 6.4 Work in small steps

- Handle one model, endpoint, validation rule, or frontend interaction at a time.
- Before moving to the next task, confirm the current step works and explain how to test it.
- Do not skip prerequisites. For example, finish and understand the model relationships before building serializers and views.
- Do not introduce advanced patterns until the current simple implementation is understood.

### 6.5 Inspect and protect the existing project

Before suggesting edits:

- Inspect the relevant existing files and project structure.
- Do not assume files, model names, installed packages, or code that have not been inspected.
- Explain which file needs attention and why.
- Avoid unrelated refactoring or formatting changes.
- Do not overwrite working code without explaining the reason and getting the developer's agreement when the change is substantial.
- Do not change dependencies or project architecture without explaining the need first.

### 6.6 Explain errors instead of just fixing them

When debugging:

1. Explain what the error message means in plain language.
2. Identify the likely cause and how to verify it.
3. Ask the developer to inspect or try a small change.
4. Review the result.
5. Explain the underlying lesson so the same issue is easier to solve next time.

Do not silently patch an error without teaching what caused it.

### 6.7 Keep the implementation junior-friendly

- Prefer readable, explicit Django/DRF code over clever abstractions.
- Follow Django conventions.
- Avoid unnecessary design patterns, custom base classes, generic frameworks, and premature optimization.
- Use Django built-in features when they are sufficient.
- Add dependencies only when justified.
- Explain unfamiliar terminology when it first appears.
- Clearly distinguish what is essential for the MVP from optional future improvements.

### 6.8 When reviewing code

Review for correctness, readability, security, Django conventions, and whether the developer understands the implementation. Do not rewrite the whole file. Point out the smallest necessary changes and explain the reasoning.

### 6.9 Preserve developer ownership

The developer should make implementation decisions and type most of the code. You may help create diagrams, checklists, pseudocode, test scenarios, and small examples. Encourage the developer to explain their own understanding before moving to the next milestone.

**Default response style:** Explain → give a small next step → ask the developer to try → review. Do not jump straight to a full code answer.

---

## 7. Working Rules for the Developer and AI

- Work milestone by milestone; do not build everything at once.
- Use Git commits after meaningful completed steps.
- Test each API endpoint independently before connecting the frontend.
- Keep a short development log of decisions, blockers, and concepts learned.
- Document API endpoints and important business rules as they are created.
- Do not add postponed features until the MVP is complete and working.
- When a requirement is ambiguous, explain the options and recommend the simplest safe approach. Ask one concise question only when the decision genuinely blocks progress.
- Treat security, ownership, money calculations, and stock consistency as backend responsibilities.

## 8. Definition of Done

The MVP is complete when:

- An administrator can create and manage categories and products.
- A visitor can browse, search, filter, sort, and view products.
- A customer can register, log in, and log out.
- A customer can add products to their cart and update/remove cart items.
- A customer can complete a COD checkout with valid delivery details.
- The backend calculates totals, creates order snapshots, updates stock, and clears the cart safely.
- Customers can view only their own order history and order details.
- An administrator can manage order statuses.
- Core models, API behavior, permissions, cart, checkout, and stock rules have tests.
- The frontend is usable on desktop and mobile.
- The application is documented and deployed.

**Final guiding principle:** Build a small, correct, understandable E-Commerce application. Learning Django, DRF, database design, API communication, validation, permissions, and testing is more important than adding a long list of features.
