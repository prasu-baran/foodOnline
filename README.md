# FoodOnline — Multi-Vendor Food Ordering Platform

A full-stack food ordering marketplace built with **Django 5.1** and **PostgreSQL**. Customers can browse restaurants, add food to cart, place orders, and pay online. Vendors manage their menu, track orders, and view sales analytics.

---

## Features

### Customer
- Register / login with email verification
- Browse and search restaurants by name or food item
- Add food to cart, adjust quantities in real-time (AJAX)
- **Favourite restaurants** — heart-toggle, saved to a personal list
- **Coupon / promo codes** — apply at checkout for % or flat discounts
- **Multiple saved addresses** — save Home/Work addresses, click to fill at checkout
- Checkout with billing form auto-filled from profile
- Pay via **PayPal** or **RazorPay**
- View order history, order detail with tax breakdown
- **Reorder** — one click re-adds all items from a past order to cart
- **Rate & review** restaurants — star rating + comment from order detail or vendor page
- **Loyalty points** — earn 1 point per $1 spent (tracked on profile)
- Personal referral code auto-generated on registration

### Vendor / Restaurant
- Register with license upload; admin approval flow
- Full **menu builder** — add/edit/delete categories and food items
  - Food item tags: **Veg**, **Spicy**, **Allergen info**
- Set **opening hours** per day (AJAX add/remove rows)
- **Sales dashboard** with:
  - Total orders, current month revenue, total revenue cards
  - **Bar chart** — revenue for the last 6 months (Chart.js)
  - **Doughnut chart** — top 5 selling items by quantity
- View all orders and order details
- Receive email notifications on new orders

### Admin
- Approve/reject vendor registrations (email sent automatically)
- Manage **Tax** rates (applied dynamically at checkout)
- Manage **Coupons** — code, type (% / flat), min order, max uses, expiry
- View all Reviews, Favourites, User Addresses

---

## Tech Stack

| Layer | Technology |
|---|---|
| Backend | Django 5.1.4, Python 3.12 |
| Database | PostgreSQL (via psycopg2) |
| Frontend | Bootstrap 4, jQuery 3.4, SweetAlert2 |
| Charts | Chart.js 3.9 |
| Payments | PayPal SDK, RazorPay |
| Email | Gmail SMTP (via Django email backend) |
| Config | python-decouple (.env file) |

---

## Project Structure

```
foodOnline/
├── accounts/        # Custom User model, UserProfile, UserAddress, auth views
├── vendor/          # Vendor model, OpeningHour, menu builder views
├── menu/            # Category, FoodItem (with veg/spicy/allergen tags)
├── marketplace/     # Cart, Tax, Review, Coupon, Favourite — listing & checkout
├── orders/          # Payment, Order, OrderedFood — place order & payments
├── customers/       # Customer dashboard, profile, my orders, favourites, addresses
├── foodOnline_main/ # Project settings, main URLs, static JS/CSS
├── templates/       # All HTML templates
├── static/          # CSS, JS, images
├── media/           # User-uploaded files (profile pics, food images, licenses)
├── .env             # Secret keys — NOT committed to Git
└── .env-sample      # Template for .env — safe to commit
```

---

## Local Setup

### 1. Clone the repository

```bash
git clone https://github.com/your-username/foodOnline.git
cd foodOnline
```

### 2. Create and activate virtual environment

```bash
python -m venv env

# Windows
env\Scripts\activate

# macOS / Linux
source env/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

> If `requirements.txt` doesn't exist yet, generate it:
> ```bash
> pip freeze > requirements.txt
> ```

### 4. Set up environment variables

Copy the sample file and fill in your values:

```bash
cp .env-sample .env
```

Edit `.env`:

```env
SECRET_KEY=your-django-secret-key
DEBUG=True

# Database
DB_NAME=foodOnline_db
DB_USER=postgres
DB_PASSWORD=your_db_password
DB_HOST=localhost

# Email (Gmail SMTP)
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_HOST_USER=your@gmail.com
EMAIL_HOST_PASSWORD=your_gmail_app_password
DEFAULT_FROM_EMAIL=FoodOnline <your@gmail.com>

# Google Maps API Key
GOOGLE_API_KEY=your_google_maps_api_key

# PayPal
PAYPAL_CLIENT_ID=your_paypal_client_id
```

> **Gmail App Password**: Go to Google Account → Security → 2-Step Verification → App Passwords → generate one for "Mail".

### 5. Create the PostgreSQL database

```sql
CREATE DATABASE foodOnline_db;
```

### 6. Run migrations

```bash
python manage.py migrate
```

### 7. Create a superuser

```bash
python manage.py createsuperuser
```

### 8. Collect static files (optional for development)

```bash
python manage.py collectstatic
```

### 9. Start the development server

```bash
python manage.py runserver
```

Open **http://127.0.0.1:8000**

---

## Admin Panel Setup

Visit **http://127.0.0.1:8000/admin/** and:

1. **Approve vendors** — Vendor → select vendor → set `Is approved = True` → Save (triggers email)
2. **Add tax rates** — Marketplace → Tax → Add Tax (e.g. GST 5%)
3. **Create coupons** — Marketplace → Coupons → Add Coupon
   - Example: Code `WELCOME10`, Type `Percentage`, Value `10`, Min Order `0`, Active ✓
4. **Set food item tags** — Menu → Food Items → edit any item → set Veg/Spicy/Allergen

---

## Key URLs

| URL | Description |
|---|---|
| `/` | Home page — featured restaurants |
| `/marketplace/` | Browse all restaurants |
| `/marketplace/<slug>/` | Vendor detail — menu, reviews, opening hours |
| `/cart/` | Shopping cart |
| `/checkout/` | Checkout — address, coupon, payment method |
| `/orders/place_order/` | Place order |
| `/orders/order_complete/` | Order confirmation page |
| `/customer/my_orders/` | Customer order history |
| `/customer/my_favourites/` | Saved favourite restaurants |
| `/customer/my_addresses/` | Saved delivery addresses |
| `/vendordashboard/` | Vendor sales dashboard with charts |
| `/vendor/menu-builder/` | Vendor menu builder |
| `/admin/` | Django admin panel |

---

## Environment Variables Reference

| Variable | Required | Description |
|---|---|---|
| `SECRET_KEY` | Yes | Django secret key |
| `DEBUG` | No | `True` for dev, `False` for production |
| `DB_NAME` | Yes | PostgreSQL database name |
| `DB_USER` | Yes | PostgreSQL username |
| `DB_PASSWORD` | Yes | PostgreSQL password |
| `DB_HOST` | Yes | Database host (usually `localhost`) |
| `EMAIL_HOST` | No | SMTP host (default: `smtp.gmail.com`) |
| `EMAIL_PORT` | No | SMTP port (default: `587`) |
| `EMAIL_HOST_USER` | Yes | Gmail address |
| `EMAIL_HOST_PASSWORD` | Yes | Gmail App Password |
| `DEFAULT_FROM_EMAIL` | No | Sender name shown in emails |
| `GOOGLE_API_KEY` | No | Google Maps API key (for address autocomplete) |
| `PAYPAL_CLIENT_ID` | Yes | PayPal client ID for payment |

---

## Git & GitHub Safety

- `.env` is listed in `.gitignore` — your secrets are **never committed**
- `.env-sample` is committed as a template with empty values — safe to share
- `media/` uploads are gitignored — only code is pushed


