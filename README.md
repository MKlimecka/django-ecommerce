# Django Commerce Project

This is a full-stack e-commerce application built with Django and Django REST Framework. It is based on the CodeWithMosh Ultimate Django Series (Parts 1–3) with additional custom backend and frontend features.

## Based on CodeWithMosh – Ultimate Django Series

**Part 1 – Django Fundamentals**
Introduction to data modeling in e-commerce systems.
- Building a modular and scalable e-commerce data model.
- Organizing models across Django apps.
- Using choice fields, one-to-one, one-to-many, and many-to-many relationships.
- Resolving circular and generic relationships.
- Creating and applying database migrations.
- Installing and connecting to MySQL.
- Running raw SQL and creating data.
- Understanding and using Django ORM: filtering, sorting, limiting, selecting fields, deferring fields, and querying generic relations.
- Query optimization using annotations, aggregations, F objects, and expressions.
- Using custom managers and understanding the queryset cache.
- Creating, updating, deleting objects.
- Executing raw SQL queries.
- Setting up and customizing Django Admin:

**Part 2 – REST APIs with Django REST Framework**
- Understanding REST principles: Resources, Representations, and HTTP Methods.
- Installing and configuring Django REST Framework (DRF).
- Creating models, serializers and API views.
- Validating and deserializing input.
- Class-based views, mixins, and generic views.
- Customizing generic views.
- Implementing filters, search, sort, and pagination.
- Authentication and Authorization:
  - Customizing the User model and extending user profiles.
  - Groups and permission system.
  - Token-based authentication using JSON Web Tokens (JWT).

**Part 3 – E-commerce Store Backend**
- Creating custom Django signals.
- Handling media:
  - Uploading and validating images via API.
  - Managing media via admin panel.
- Email sending:
  - Setting up fake SMTP.
  - Sending emails with attachments and templates.
- Asynchronous background tasks:
  - Installing Redis.
  - Setting up Celery.
  - Scheduling periodic tasks.
  - Monitoring and debugging tasks.
- Testing and optimization:
  - Writing and running unit tests.
  - Performance testing with Locust.
  - Profiling and optimizing slow endpoints.
- Caching:
  - Installing and configuring Redis cache backend.
  - Caching views and API responses.
  - Low-level caching with the cache API.

## Custom Features

### API Endpoints
- `favorites/` – All favorited products
- `favorites/me/` – Favorites of logged-in user
- `favorites/toggle/` – Add/remove favorite
- `carts/me/` – Cart of logged-in user
- `carts/items/` – Add to cart
- `carts/items/<id>/` – Edit/delete cart item

### Frontend
- Built with HTML, Bootstrap, and  JavaScript
- JWT tokens handled via `fetch()` and `localStorage`
- Fully functional UI: register, login/logout, product list, cart, favorites

### Signals
- On user creation:
  - Auto-create `Customer`
  - Auto-create empty `Favorites` and `Cart`

## Technologies

- Python 3
- Django 4
- Django REST Framework  
- Djoser + SimpleJWT  
- Bootstrap 5  
- JavaScript
- MySQL  


## Getting Started

```bash
git clone https://github.com/MKlimecka/django-ecommerce
pip install pipenv
pipenv shell
pipenv install
```

Create `settings/dev.py` (this file is .gitignored):

```python
SECRET_KEY = 'your-secret-key'
DEBUG = True

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',  
        'NAME': 'your-db-name',
        'USER': 'your-db-user',
        'PASSWORD': 'your-db-password',
        'HOST': 'localhost',
    }
}
```

Then:

```bash
python manage.py migrate
python manage.py runserver
```

App is available at: `http://localhost:8000/`

## Notes

- `settings.dev.py` is excluded via `.gitignore`
- `settings.dev.example.py` should be used for environment config reference
- Deployment setup is prepared in `settings.prod.py` (with env variables)

## License

Based on the [CodeWithMosh Django Course](https://codewithmosh.com/).  
Project extended for educational and portfolio purposes.