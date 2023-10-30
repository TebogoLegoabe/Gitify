from .database import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    followers = db.Column(db.Integer, nullable=False)
    public_repos = db.Column(db.Integer, nullable=False)

    def __init__(self, username, followers, public_repos):
        self.username = username
        self.followers = followers
        self.public_repos = public_repos
