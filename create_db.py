from app import db, app  # Import the app and db object

with app.app_context():
    db.create_all()
    print("Database tables created.")