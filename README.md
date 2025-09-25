# Flask Todo App

A simple Todo application with user authentication (email/password + OAuth Google/GitHub/Facebook), admin panel, and SQLite storage.

## Features
- User registration & login
- OAuth login via Google, GitHub, Facebook (configure credentials)
- Admin panel (dashboard, stats, manage users & recent tasks)
- Task CRUD (Add, toggle complete, delete)
- Each task stores creation timestamp (UTC)
- SQLite + SQLAlchemy + Flask-Migrate
- Tailwind CSS via CDN

## Admin Login
Default admin credentials:
```
Email: admin@admin.com
Password: admin
```
(Automatically flagged as admin on registration or create via CLI command.)

## Setup
```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env  # fill in secrets if needed
flask --app run.py db init
flask --app run.py db migrate -m "Initial tables"
flask --app run.py db upgrade
flask --app run.py create-admin
flask --app run.py run
```

### OAuth Configuration
Register apps at Google, GitHub, Facebook developer portals. Add authorized redirect URIs:
```
http://localhost:5000/auth/callback/google
http://localhost:5000/auth/callback/github
http://localhost:5000/auth/callback/facebook
```
Fill corresponding environment variables in `.env`.

## Notes
- For production, set a strong SECRET_KEY and use a production-ready server (gunicorn, etc.)
- Consider adding CSRF protection for the JSON toggle endpoint or use `@csrf.exempt` selectively.
- Extend with pagination, due dates, file attachments, etc.

## License
MIT
