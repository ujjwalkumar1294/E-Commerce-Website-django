# E-Commerce-Website-django
A fully functional e-commerce website built using Django. Features include user authentication, product listings, cart management, order processing, and an admin dashboard for managing products and orders

🚀 Features

User registration & login

Product listing and product detail pages

Shopping cart functionality

Checkout and order confirmation

User order history

Responsive UI using HTML & CSS

🛠️ Tech Stack

Backend: Django (Python)

Database: SQLite (db.sqlite3)

Frontend: HTML, CSS

Version Control: Git & GitHub

📂 Project Structure
django-ecommerce/
├── ecommerce_project/   # Django project settings
├── store/               # Core e-commerce app (models, views, templates)
├── static/              # CSS and static files
├── media/               # Uploaded product images (gitignored)
└── manage.py

🚀 How to Run

Install Django:

pip install django


Apply migrations:

python manage.py migrate


Run the development server:

python manage.py runserver

🔐 Admin Access

Create a superuser to access the Django admin panel:

python manage.py createsuperuser


Access the admin panel at:

http://127.0.0.1:8000/admin/
