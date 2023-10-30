from flask import Flask
from flask_migrate import Migrate
from app import app

# Create a Migrate instance
migrate = Migrate(app, db)

if __name__ == '__main__':
    app.run()
