from flask import Flask
from flask_sqlalchemy import SQLAlchemy
#from app import db
from models.user import User

app = Flask(__name__)

# Configure the database URI (for SQLite, this is a file)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///github_users.db'

db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    followers = db.Column(db.Integer)
    public_repos = db.Column(db.Integer)

# Sample user data with programming languages used in repositories (if needed)
# ...

# Endpoints
@app.route('/user/<username>/followers', methods=['GET'])
def get_followers(username):
    user = User.query.filter_by(username=username).first()
    if user:
        return f"Followers: {user.followers}"
    else:
        return "User not found", 404

@app.route('/user/<username>/repos', methods=['GET'])
def get_repos(username):
    user = User.query.filter_by(username=username).first()
    if user:
        return f"Public Repositories: {user.public_repos}"
    else:
        return "User not found", 404

@app.route('/user/<username>/languages', methods=['GET'])
def get_languages(username):
    # You can add language retrieval code here
    # This depends on how you store languages in your database
    return "Languages: Not implemented yet"

if __name__ == '__main__':
    app.run(debug=True)
