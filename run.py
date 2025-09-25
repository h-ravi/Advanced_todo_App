from app import create_app, db
from app.models import User

app = create_app()

@app.cli.command('create-admin')
def create_admin():
    """Create the default admin user if not exists."""
    email = 'admin@admin.com'
    password = 'admin'
    user = User.query.filter_by(email=email).first()
    if user:
        print('Admin user already exists')
    else:
        user = User(email=email, is_admin=True)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        print('Admin user created')

@app.shell_context_processor
def _shell_context():
    return {'db': db, 'User': User}

if __name__ == '__main__':
    # For production consider: gunicorn 'run:app'
    app.run(debug=True)
