# Django Market Data Platform

A Django web application for viewing and filtering market data from Supabase, with authentication, pagination, and a modern UI.

## Features

- Custom user model with authentication (login/signup/logout)
- Market data integration from Supabase
- REST API endpoints (Django REST Framework)
- Pagination, filtering, and detail views
- Responsive UI with base template and navbar
- CORS support for frontend integration
- Environment-based configuration using `.env`
- Production-ready security settings

## Setup

1. **Clone the repository:**
   ```bash
   git clone https://github.com/xStFtx/quick-django-app.git
   cd quick-django-app
   ```

2. **Create and activate a virtual environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment variables:**
   - Copy `.env.example` to `.env` and fill in your secrets:
     ```
     DJANGO_SECRET_KEY=your-production-secret-key
     DEBUG=True
     ALLOWED_HOSTS=127.0.0.1,localhost
     SUPABASE_URL=https://your-project.supabase.co
     SUPABASE_KEY=your-supabase-key
     ```

5. **Run migrations:**
   ```bash
   python manage.py migrate
   ```

6. **Create a superuser (optional, for admin access):**
   ```bash
   python manage.py createsuperuser
   ```

7. **Run the development server:**
   ```bash
   python manage.py runserver
   ```

8. **Access the app:**
   - Visit [http://127.0.0.1:8000/](http://127.0.0.1:8000/) in your browser.

## Environment Variables

- `DJANGO_SECRET_KEY` — Django secret key (keep this secret!)
- `DEBUG` — Set to `False` in production
- `ALLOWED_HOSTS` — Comma-separated list of allowed hosts
- `SUPABASE_URL` — Your Supabase project URL
- `SUPABASE_KEY` — Your Supabase API key

## Security

- Do **not** commit your `.env` file or secret keys to public repositories.
- Set `DEBUG=False` and configure `ALLOWED_HOSTS` for production.
- Use HTTPS and review Django's [deployment checklist](https://docs.djangoproject.com/en/stable/howto/deployment/checklist/).

## License

MIT

## Author

[xStFtx](https://github.com/xStFtx)
