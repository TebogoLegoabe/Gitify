""" gitify's main module that handles most of the backend code """
from flask import Flask, render_template, request, redirect, url_for, abort
from utils import get_languages_lite as get_language
from utils import options
import requests
from os import getenv
import datetime

# global variables used to limit how many results are displayed per page
REPOS_PER_PAGE = 5
USERS_PER_PAGE = 5

# github access token fetched from github
access_token = getenv("ACCESS_TOKEN")
# headers that define OAuth requirements for github api
if not access_token:
    print('please set the enviromental variable "ACCESS_TOKEN" to your github access token')
headers = {
    'Authorization': f'token {access_token}',
    'Accept': 'application/vnd.github.v3+json',
}


# frequently used common data that is passed to the urls

app = Flask(__name__)


@app.errorhandler(404)
def page_not_found(e):
    """ error handler for pages that doesn't exist"""
    return render_template("404.html"), 404


@app.errorhandler(422)
def unprocessable_entity(e):
    """ 
    error handler for out of reach results
    NOTE: github api only allows the fetch of top 1000 results of the key_word
    and gives the following massage
    {
        "message": "Only the first 1000 search results are available",
        "documentation_url": "https://docs.github.com/v3/search/"
    }
    """
    return render_template("422.html"), 422

@app.errorhandler(401)
def page_not_found(e):
    """ error handler for pages that unauthorized"""
    return render_template("401.html"), 401


@app.route("/search")
def search_redirect():
    """ redirects to /repos or /users uri's according to the filled form"""
  # Get the option parameter from the GET request
    search_for = request.args.get("search_for")
    q = request.args.get("q")
    language = request.args.get("language", "")
    location = request.args.get('location', "")
    sort_by = request.args.get('sort_by', "")
    # Redirect to the corresponding route based on the option value
    if search_for == "repos":
        return redirect(url_for("search_repos", search_for=search_for, q=q, language=language, location=location, sort_by=sort_by))
    elif search_for == "users":
        return redirect(url_for("search_users", search_for=search_for, q=q, language=language, location=location, sort_by=sort_by))


@app.route("/")
def home():
    """ home page used for searching"""
    return render_template("search.html")


@app.route('/users', methods=['GET'])
def search_users():
    """ searchs for users in github using github api """
    # getting all parameters of the /users uri
    username = request.args.get("q")
    lang = request.args.get("language", "")
    loc = request.args.get('location', "")
    sort_by = request.args.get('sort_by', "").split(
        '_') if request.args.get('sort_by') else ['', '']

    # paramaters used by gitify
    params_g = {
        'q': username,
        "sort_by": sort_by,
        "location": loc,
        "language": lang,
        "per_page": USERS_PER_PAGE,
        "page": int(request.args.get('page', 1))
    }
    # if a no parameters passed display empty page
    if not username:
        return render_template('user_results.html', users=[], options=options, results=-1, p=params_g, language=lang, q=username)
    # parameters used in github api
    params = {
        'q': f'{username} location:"{loc}" language:"{lang}"',
        "sort": sort_by[0],
        "order": sort_by[1],
        "per_page": USERS_PER_PAGE,
        "page": int(request.args.get('page', 1))
    }
    # search for the user
    req = requests.get(f"https://api.github.com/search/users",
                       params=params, headers=headers)
    if req.status_code == 200:
        all_users = req.json()
        users = []
        results_count = all_users['total_count']

        # loops over all users and retrive necessary information about the user
        for user in all_users['items']:
            temp = {
                "username": user['login'],
                "avatar": user['avatar_url'],
                "html_url": user['html_url']
            }
            # inside a user result you will find 'url' that contains detailed information about the user, and store the info in users_info variable. e.g: https://api.github.com/repos/creytiv/re
            user_info = requests.get(user['url'], headers=headers).json()

            # fetching user's information
            temp['followers'] = user_info['followers']
            temp['following'] = user_info['following']
            temp['bio'] = user_info['bio']
            temp['location'] = user_info.get('location', 'Unknown')
            # inside the user_info the 'public_repos' key holds the number of public repositories the user owns
            temp['public_repos'] = user_info['public_repos']
            # inside the 'repos_url the 'repos_url' key holds a link to all the repositories the user owns. e.g : https://api.github.com/users/Qihoo360
            # what the get_language function does is: it accepts a repos_url, adds all the language usages of that user in each repository, calculates their usage percentage,returns a dictionary of languages, when you use the .itmes() the result will be as follows. eg: [('Java', 21.43), ('Kotlin', 21.43), ('Python', 14.29), ('Others', 42.85)]
            unfiltered_lang = get_language(user_info['repos_url']).items()

            # the code bellow is a filtering mechanism: it selects top 3 languages used, sum the other languages and adds them as a forth language
            sorted_lang = sorted(
                unfiltered_lang, key=lambda ln: ln[1], reverse=True)
            temp['languages'] = sorted_lang[0:3]
            remained = 0
            for t in temp['languages']:
                remained += t[1]
            temp['languages'].append(('Others', 100 - remained))
            # adds the user's info to the list of users
            users.append(temp)

        return render_template('user_results.html', users=users, options=options, results=results_count, p=params_g, language=lang, q=username)
    elif req.status_code == 422:
        abort(422)
    elif req.status_code == 401:
        abort(401)
    elif req.status_code == 404:
        abort(404)
    else:
        render_template('wrong.html')


@app.route('/repos', methods=['GET'])
def search_repos():
    """ search repos by the given key word """
    # getting all parameters of the /users uri
    q = request.args.get("q")
    sort_by = request.args.get('sort_by').split(
        '_') if request.args.get('sort_by') else ['', '']
    lang = request.args.get("language", "")
    # paramaters used by gitify
    params_g = {
        'q': q,
        "sort_by": request.args.get('sort_by', ""),
        "language": lang,
        "per_page": REPOS_PER_PAGE,
        "page": int(request.args.get('page', 1))
    }
    # if a no parameters passed display empty page
    if not q:
        return render_template('repo_results.html', results=-1, page=0, options=options, p=params_g)
    # prametres needed by for github requests
    params = {
        'q': f'{q} language:"{lang}"' if lang else q,
        "sort": sort_by[0],
        "order": sort_by[1],
        "per_page": REPOS_PER_PAGE,
        "page": int(request.args.get('page', 1))
    }
    # search in github api for repositories
    response = requests.get(
        "https://api.github.com/search/repositories", params=params, headers=headers)

    # if the response is successfull
    if response.status_code == 200:
        data = response.json()
        items = data["items"]
        results_count = data['total_count']

        repos = []
        # get required infos about the repostories by looping over them
        for item in items:
            temp = {}
            temp['name'] = item['name']
            temp['description'] = item['description']
            temp['html_url'] = item['html_url']
            temp['owner'] = item['owner']['login']
            temp['avatar'] = item['owner']['avatar_url']
            temp['language'] = item['language']
            temp['stars'] = item['stargazers_count']
            temp['forks'] = item['forks_count']
            temp['topics'] = item['topics']
            repos.append(temp)
        return render_template('repo_results.html', repos=repos, options=options, results=results_count, p=params_g)
    # handling errors if the response has an issue
    elif response.status_code == 422:
        abort(422)
    elif response.status_code == 404:
        abort(401)
    elif response.status_code == 422:
        abort(404)
    else:
        render_template('wrong.html')



@app.route('/trending')
def trending_repos():
    """ it fetches trending repositories in the current month """
    # calculating 30 days from today and format it as requeired by github api
    today = datetime.date.today()
    one_month_ago = today - datetime.timedelta(days=30)
    one_month_ago_str = one_month_ago.strftime("%Y-%m-%d")
    # pramaters needed by github api
    params = {
        "q": f"created:>{one_month_ago_str}",
        "sort": "stars",
        "order": "desc",
        "per_page": 20,
    }
    # send get requests to github api to fetch trending repositories
    response = requests.get(
        "https://api.github.com/search/repositories", params=params, headers=headers)
    print("status code <<", response.status_code)
    if response.status_code == 200:
        data = response.json()
        items = data["items"]
        repos = []
        # get all required information of each repositories
        for item in items:
            temp = {}
            temp['name'] = item['name']
            temp['description'] = item['description']
            temp['html_url'] = item['html_url']
            temp['owner'] = item['owner']['login']
            temp['avatar'] = item['owner']['avatar_url']
            temp['language'] = item['language']
            temp['stars'] = item['stargazers_count']
            temp['forks'] = item['forks_count']
            temp['topics'] = item['topics']
            repos.append(temp)
        return render_template('trending.html', repos=repos, options=options, results=1, p=params)
    else:
        # if something went wrong
        abort(404)


if __name__ == '__main__':
    app.run()