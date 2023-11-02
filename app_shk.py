from flask import Flask, render_template
from utils import get_languages_lite as get_language
import requests
from os import getenv


access_token = getenv("ACCESS_TOKEN")

headers = {
    'Authorization': f'token {access_token}',
    'Accept': 'application/vnd.github.v3+json',
}
app = Flask(__name__)

@app.route("/")
def home():
    return "hello world"

@app.route('/users/<key_word>', methods=['GET'])
def search_users(key_word):
    """ searchs in users, repositories """
    # search for the key_word in the users -> e.g : https://api.github.com/search/users?q=re
    req = requests.get(f"https://api.github.com/search/users?q={key_word}", headers=headers)
    all_users = req.json()
    users = []
    print("====", all_users)
    # the result will have 'items' key set to the list of users that match the key word
    print(len(all_users['items']))

    # looping through all of the results to access each user
    for user in all_users['items']:
        temp =  {
            "username": user['login'],
            "followers": '',
            "public_repos": 0,
            "languages": {}
        }
        # DEBUGGING
        print("fetching for: ", user['login'])
        # inside a user result you will find 'url' that contains detailed information about the user, and store the info in users_info variable. e.g: https://api.github.com/repos/creytiv/re
        user_info = requests.get(user['url'], headers=headers).json()
        
        # inside the user_info the 'followers' key holds the number of followers the user has
        temp['followers'] = user_info['followers']
        # inside the user_info the 'public_repos' key holds the number of public repositories the user owns
        temp['public_repos'] = user_info['public_repos']
        # inside the 'repos_url the 'repos_url' key holds a link to all the repositories the user owns. e.g : https://api.github.com/users/Qihoo360
        # what the get_language function does is: it accepts a repos_url, adds all the language usages of that user in each repository, calculates their usage percentage,returns a dictionary of languages, when you use the .itmes() the result will be as follows. eg: [('Java', 21.43), ('Kotlin', 21.43), ('Python', 14.29), ('Others', 42.85)]
        unfiltered_lang = get_language(user_info['repos_url']).items()

        # the code bellow is a filtering mechanism: it selects top 3 languages used, sum the other languages and adds them as a forth language
        sorted_lang = sorted(unfiltered_lang,key=lambda ln: ln[1], reverse=True)
        temp['languages'] = sorted_lang[0:3]
        remained = 0
        for t in temp['languages']:
            remained += t[1]
        temp['languages'].append(('Others', 100 - remained))
        # adds the user's info to the list of users
        users.append(temp)
    
    # DEBUGGING: for visualising
    # users = [{'username': 're', 'followers': 6, 'public_repos': 0, 'languages': [('Others', 100)]} , {'username': 'ReVanced', 'followers': 15925, 'public_repos': 28, 'languages': [('Java', 21.43), ('Kotlin', 21.43), ('Python', 14.29), ('Others', 42.85)]} , {'username': 're-ovo', 'followers': 413, 'public_repos': 136, 'languages': [('Java', 46.67), ('Kotlin', 26.67), ('JavaScript', 3.33), ('Others', 23.33)]} , {'username': 'vbty', 'followers': 210, 'public_repos': 151, 'languages': [('C++', 16.67), ('HTML', 10.0), ('Python', 10.0), ('Others', 63.33)]} , {'username': 'kanreisa', 'followers': 162, 'public_repos': 37, 'languages': [('JavaScript', 63.33), ('TypeScript', 16.67), ('C', 6.67), ('Others', 13.329999999999998)]} , {'username': 'lloc', 'followers': 90, 'public_repos': 96, 'languages': [('PHP', 43.33), ('JavaScript', 23.33), ('Python', 6.67), ('Others', 26.67)]} , {'username': 'citizenfx', 'followers': 386, 'public_repos': 66, 'languages': [('C++', 33.33), ('C#', 13.33), ('Go', 10.0), ('Others', 43.34)]} , {'username': 'rwfpl', 'followers': 648, 'public_repos': 18, 'languages': [('C++', 61.11), ('Python', 22.22), ('C', 5.56), ('Others', 11.11)]} , {'username': 'rescript-lang', 'followers': 260, 'public_repos': 19, 'languages': [('OCaml', 31.58), ('JavaScript', 21.05), ('ReScript', 15.79), ('Others', 31.580000000000013)]} , {'username': 'ReAbout', 'followers': 340, 'public_repos': 17, 'languages': [('Python', 17.65), ('C', 11.76), ('Java', 5.88), ('Others', 64.71000000000001)]} , {'username': 'krasimir', 'followers': 1958, 'public_repos': 210, 'languages': [('JavaScript', 76.67), ('HTML', 3.33), ('Dart', 3.33), ('Others', 16.67)]} , {'username': 'reZach', 'followers': 86, 'public_repos': 77, 'languages': [('JavaScript', 40.0), ('C#', 20.0), ('HTML', 13.33), ('Others', 26.67)]} , {'username': 'joe-re', 'followers': 64, 'public_repos': 99, 'languages': [('JavaScript', 33.33), ('TypeScript', 20.0), ('Ruby', 10.0), ('Others', 36.67)]} , {'username': 'akiross', 'followers': 68, 'public_repos': 75, 'languages': [('Go', 23.33), ('Rust', 13.33), ('Dockerfile', 13.33), ('Others', 50.010000000000005)]} , {'username': 'v-kolesnikov', 'followers': 134, 'public_repos': 176, 'languages': [('Ruby', 23.33), ('Clojure', 10.0), ('Elixir', 6.67), ('Others', 60.0)]} , {'username': 'ReCoded-Org', 'followers': 64, 'public_repos': 73, 'languages': [('JavaScript', 46.67), ('HTML', 16.67), ('CSS', 10.0), ('Others', 26.659999999999997)]} , {'username': 'remy', 'followers': 7511, 'public_repos': 333, 'languages': [('JavaScript', 56.67), ('HTML', 10.0), ('PHP', 6.67), ('Others', 26.659999999999997)]} , {'username': 'Crauzer', 'followers': 234, 'public_repos': 64, 'languages': [('C#', 40.0), ('C++', 6.67), ('Rust', 3.33), ('Others', 50.0)]} , {'username': 'redrgnl', 'followers': 27, 'public_repos': 20, 'languages': [('HTML', 25.0), ('JavaScript', 20.0), ('PHP', 15.0), ('Others', 40.0)]} , {'username': 'reMarkable', 'followers': 185, 'public_repos': 95, 'languages': [('C++', 20.0), ('C', 16.67), ('Go', 13.33), ('Others', 50.0)]} , {'username': 'Re4son', 'followers': 586, 'public_repos': 132, 'languages': [('C', 40.0), ('Java', 10.0), ('Others', 50.0)]} , {'username': 'scorelab', 'followers': 170, 'public_repos': 109, 'languages': [('JavaScript', 33.33), ('HTML', 16.67), ('CSS', 6.67), ('Others', 43.33)]} , {'username': 'hanxiao', 'followers': 3706, 'public_repos': 105, 'languages': [('Python', 30.0), ('JavaScript', 13.33), ('CSS', 3.33), ('Others', 53.34)]} , {'username': 'renovate-bot', 'followers': 1234, 'public_repos': 8824, 'languages': [('Go', 6.67), ('C++', 3.33), ('Blade', 3.33), ('Others', 86.67)]} , {'username': 'renatogroffe', 'followers': 2671, 'public_repos': 1313, 'languages': [('C#', 66.67), ('HTML', 13.33), ('PowerShell', 6.67), ('Others', 13.329999999999998)]} , {'username': 'neoremind', 'followers': 674, 'public_repos': 49, 'languages': [('Java', 66.67), ('C++', 6.67), ('Shell', 6.67), ('Others', 19.989999999999995)]} , {'username': 'rac14', 'followers': 28, 'public_repos': 161, 'languages': [('PHP', 33.33), ('Java', 6.67), ('C++', 3.33), ('Others', 56.67)]} , {'username': 'gpakosz', 'followers': 382, 'public_repos': 35, 'languages': [('C', 20.0), ('Ruby', 16.67), ('C++', 16.67), ('Others', 46.66)]} , {'username': 'Guss-droid', 'followers': 51, 'public_repos': 43, 'languages': [('TypeScript', 70.0), ('JavaScript', 16.67), ('Ruby', 6.67), ('Others', 6.659999999999997)]} , {'username': 'mreferre', 'followers': 155, 'public_repos': 47, 'languages': [('Shell', 20.0), ('JavaScript', 6.67), ('Go', 6.67), ('Others', 66.66)]}]
    
    # print(users)
    # ^^^ NOTE: print it for if you need DEBUGGING

    return render_template('user_results.html', users=users)

if __name__ == '__main__':
    app.run(debug=True)