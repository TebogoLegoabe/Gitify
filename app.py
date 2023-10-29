from flask import Flask, request, jsonify

app = Flask(__name__)

# Sample user data with programming languages used in repositories
users = {
    "user1": {
        "username": "user1",
        "followers": 100,
        "public_repos": 20,
        "languages": [
            {"name": "Python", "usage": 70},
            {"name": "JavaScript", "usage": 30}
            ]
    },
    "user2": {
        "username": "user2",
        "followers": 50,
        "public_repos": 10,
        "languages": [
            {"name": "C++", "usage": 60},
            {"name": "Java", "usage": 40}
            ]
    }
}

# Endpoints
@app.route('/user/<username>/followers', methods=['GET'])
def get_followers(username):
    if username in users:
        user_info = users[username]
        return f"Followers: {user_info['followers']}"
    else:
        return "User not found", 404

@app.route('/user/<username>/repos', methods=['GET'])
def get_repos(username):
    if username in users:
        user_info = users[username]
        return f"Public Repositories: {user_info['public_repos']}"
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
