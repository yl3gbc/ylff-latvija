from getpass import getpass

from werkzeug.security import generate_password_hash

from app import app
from extensions import db
from models import User


email = input("Admin email: ").strip()
password = getpass("Admin password: ").strip()

with app.app_context():
    existing_user = User.query.filter_by(email=email).first()

    if existing_user:
        print("Admin user already exists")
    else:
        admin = User(
            email=email,
            password_hash=generate_password_hash(password),
            is_admin=True,
            is_active=True,
        )

        db.session.add(admin)
        db.session.commit()

        print("Admin user created")
