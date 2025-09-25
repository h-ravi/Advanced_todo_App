# Flask Todo App

This Flask Todo App is a simple yet powerful web application designed to help users manage their daily tasks with ease. It is built using the Flask framework and integrates modern features such as user authentication, OAuth logins, an admin panel, and a task management system. The application is lightweight, beginner-friendly, and highly extendable, making it a perfect starting point for learning Flask or for building your own task management tool.

This document serves as a detailed guide to understand the project, its features, setup process, configuration details, and potential extensions.

---

## SECTION 1: INTRODUCTION

The Flask Todo App is a task management system where users can create, update, and delete their to-do tasks. Unlike basic examples, this app also supports:

1. User authentication via email and password.
2. Third-party authentication via OAuth (Google, GitHub, Facebook).
3. An admin dashboard where administrators can manage users, view task statistics, and oversee recent activity.
4. A clean user interface powered by Tailwind CSS.
5. A robust backend built with Flask, SQLite, SQLAlchemy, and Flask-Migrate.

This combination of features makes the project practical for real-world use while still being simple enough for educational purposes.

---

## SECTION 2: FEATURES

1. User Authentication

   * New users can register using an email and password.
   * Existing users can log in securely.
   * OAuth authentication is supported for Google, GitHub, and Facebook.
   * Passwords are hashed and stored securely.

2. Admin Panel

   * A special dashboard accessible only by admin users.
   * Admins can manage registered users.
   * Recent tasks are displayed for quick overview.
   * Task statistics and activity metrics can be monitored.

3. Task Management (CRUD Functionality)

   * Add a new task with a simple form.
   * Mark tasks as complete or incomplete by toggling their status.
   * Delete tasks when no longer needed.
   * Each task automatically stores a creation timestamp in UTC format.

4. Database and Migrations

   * SQLite is used for data storage, making setup very easy.
   * SQLAlchemy ORM provides clean database interaction.
   * Flask-Migrate handles database migrations, so schema changes are manageable.

5. User Interface

   * Tailwind CSS is included via CDN.
   * Provides a modern, responsive, and clean UI without requiring a heavy frontend framework.

6. Developer Friendly

   * Environment configuration through `.env` file.
   * Ready-to-use setup commands for database initialization and admin creation.
   * Clear separation of features and extendable codebase.

---

## SECTION 3: DEFAULT ADMIN LOGIN

By default, the application comes with a pre-configured admin user.

Email: [admin@admin.com](mailto:admin@admin.com)
Password: admin

This user automatically has admin privileges. You can also create additional admin accounts by registering new users and manually assigning them admin rights or by using the CLI command `flask --app run.py create-admin`.

---

## SECTION 4: SETUP AND INSTALLATION

To run this application locally, follow these steps:

Step 1: Clone the repository

* Download the project or clone it using Git.

Step 2: Create and activate a virtual environment

* Run: `python -m venv venv`
* On Linux or macOS: `source venv/bin/activate`
* On Windows: `venv\Scripts\activate`

Step 3: Install dependencies

* `Run: pip install -r requirements.txt`

Step 4: Configure environment variables

* Copy the example environment file: cp .env.example .env
* Open `.env.example` and add necessary secrets (for example, secret key, OAuth credentials).

Step 5: Initialize the database

* Run: `flask --app run.py db init`
* Run: `flask --app run.py db migrate -m "Initial tables"`
* Run: `flask --app run.py db upgrade`

Step 6: Create an admin user

* Run: `flask --app run.py create-admin`

Step 7: Start the server

* Run: `flask --app run.py run`
* The application will be available at: [http://localhost:5000](http://localhost:5000)

---

## SECTION 5: OAUTH CONFIGURATION

To enable login via Google, GitHub, and Facebook, you need to register applications with these providers.

1. Register your app in the respective developer portals (Google Cloud Console, GitHub Developer, Facebook Developers).
2. Add the following authorized redirect URIs for each provider:

   * [http://localhost:5000/auth/callback/google](http://localhost:5000/auth/callback/google)
   * [http://localhost:5000/auth/callback/github](http://localhost:5000/auth/callback/github)
   * [http://localhost:5000/auth/callback/facebook](http://localhost:5000/auth/callback/facebook)
3. Obtain Client ID and Client Secret from each provider.
4. Add these credentials in your `.env` file under appropriate variable names.

---

## SECTION 6: PROJECT STRUCTURE

A general outline of the project structure is as follows:

* run.py              : Entry point to run the Flask application.
* app/                : Contains the main application code.

  * models/          : Database models (User, Task, etc.).
  * routes/          : Application routes and view functions.
  * templates/       : HTML templates rendered by Flask.
  * static/          : Static files such as CSS and JS.
  * admin/           : Admin panel logic and views.
* migrations/         : Database migration files created by Flask-Migrate.
* requirements.txt    : List of Python dependencies.
* .env.example        : Example environment configuration file.

---

## SECTION 7: DEPLOYMENT NOTES

1. Secret Key

   * Always set a strong and unique SECRET\_KEY in your `.env.example` file for production.

2. Production Server

   * Use a production-ready WSGI server like Gunicorn or uWSGI instead of Flask’s development server.

3. Security Considerations

   * Add CSRF protection for APIs, especially if exposing JSON endpoints.
   * Always validate OAuth credentials and redirect URIs.

4. Scaling

   * You may replace SQLite with PostgreSQL or MySQL for larger deployments.
   * Add caching layers such as Redis if performance is critical.

5. Extensions

   * Implement pagination for large lists of tasks.
   * Add due dates, reminders, or file attachments to tasks.
   * Consider adding notifications (email or push) for deadlines.

---

## SECTION 8: FUTURE IMPROVEMENTS

* Advanced analytics for admins (task completion rates, user activity).
* Role-based access control beyond just admin and normal users.
* Mobile-friendly interface improvements.
* API endpoints for integration with external apps.
* Automated test coverage to ensure code reliability.

---

## SECTION 9: CONTRIBUTING

Contributions are welcome!
To contribute:

1. Fork the repository.
2. Create a feature branch for your changes.
3. Commit and push your changes.
4. Submit a pull request with a clear description.

Please follow standard coding conventions and provide test cases where possible.

---

## SECTION 10: LICENSE

This project is licensed under the MIT License.
This means you are free to use, modify, and distribute the project, provided you include the original license.

---

## SECTION 11: SUPPORT

If you find this project helpful, please consider giving it a star on GitHub.
Your support motivates further development and improvements.

For questions, issues, or feature requests, please open an issue in the repository.

---

## END OF README

---

Would you like me to also create a **shorter "Quick Start Guide" version** of this README (something concise that users can read in 1 minute), alongside this detailed one, so you can include both in the repository?
