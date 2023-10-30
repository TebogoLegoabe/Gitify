from flask import Flask
from models.database import db
from models.user import User
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Configure the database URI (for SQLite, this is a file)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///github_users.db'
db.init_app(app)

# Create the database tables
with app.app_context():
    db.create_all()

# Sample user data with programming languages used in repositories
users = {
    "user1": User(username="user1", followers=100, public_repos=20),
    "user2": User(username="user2", followers=50, public_repos=10)
}

# Endpoints
@app.route('/user/<username>/followers', methods=['GET'])
def get_followers(username):
    # Assuming you have a dictionary 'users' with user data, similar to your previous code
    if username in users:
        user_info = users[username]
        return f"Followers: {user_info['followers']}"
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
    if username in users:
        user_info = users[username]
        languages = user_info.get('languages', [])
        language_data = "\n".join([f"{lang['name']} ({lang['usage']}%)" for lang in languages])
        return f"Languages:\n{language_data}"
    else:
        return "User not found", 404

if __name__ == '__main__':
    app.run(debug=True)
