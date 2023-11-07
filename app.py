from flask import Flask, render_template, request, redirect, url_for
from utils import get_languages_lite as get_language
import requests
from os import getenv
import datetime

colors = {
        "Python": "#3776AB", # Blue
        "Java": "#B07219", # Brown
        "JavaScript": "#F7DF1E", # Yellow
        "C#": "#178600", # Green
        "C++": "#00599C", # Dark blue
        "PHP": "#777BB4", # Purple
        "R": "#198CE7", # Light blue
        "TypeScript": "#3178C6", # Cyan
        "Swift": "#FA7343", # Orange
        "C": "#438EFF", # Sky blue
        "Kotlin": "#F18E33", # Amber
        "Makefile": "#427B58", # Olive green
        "Others": "#666666" # gray 
    }

access_token = getenv("ACCESS_TOKEN")

headers = {
    'Authorization': f'token {access_token}',
    'Accept': 'application/vnd.github.v3+json',
}

app = Flask(__name__)

@app.route("/search")
def search_redirect():
  # Get the option parameter from the GET request
    search_for = request.args.get("search_for")
    q = request.args.get("q")
    language = request.args.get("language", "")
    location = request.args.get('location', "")
    sort_by = request.args.get('sort_by', "")
    # Redirect to the corresponding route based on the option value
    if search_for == "repos":
        return redirect(url_for("search_repos",search_for = search_for, q = q, language = language, location = location, sort_by = sort_by))
    elif search_for == "users":
        return redirect(url_for("search_users",search_for = search_for, q = q, language = language, location = location, sort_by = sort_by))
  
@app.route("/")
def home():
    """ home page used for searching"""
    return render_template("search.html")



@app.route('/users', methods=['GET'])
def search_users():
    """ searchs in users, repositories """
    username = request.args.get("q")
    lang = request.args.get("language", "")
    loc = request.args.get('location', "")
    sort_by = request.args.get('sort_by', "").split('_') if request.args.get('sort_by') else ['','']

    if not username:
        return render_template('user_results.html', users=[], colors=colors, results=-1)

    params = {
        'q': f'{username} location:"{loc}" language:"{lang}"',
        "sort": sort_by[0],
        "order": sort_by[1],
        "per_page": 3
    }

    req = requests.get(f"https://api.github.com/search/users", params=params, headers=headers)
    print("<<<<<", req.url)
    print(req.url)
    if req.status_code == 200:
        all_users = req.json()
        print(all_users)
        users = []
        results_count = all_users['total_count']

        print("====", all_users)
        # the result will have 'items' key set to the list of users that match the key word
        print(len(all_users['items']))

        # looping through all of the results to access each user
        for user in all_users['items']:
            temp =  {
                "username": user['login'],
                "avatar": user['avatar_url'],
                "html_url": user['html_url']
            }
            # DEBUGGING
            print("fetching for: ", user['login'])
            # inside a user result you will find 'url' that contains detailed information about the user, and store the info in users_info variable. e.g: https://api.github.com/repos/creytiv/re
            user_info = requests.get(user['url'], headers=headers).json()
            
            # inside the user_info the 'followers' key holds the number of followers the user has
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


        print(users)
        return render_template('user_results.html', users=users, colors= colors, results=results_count)
    else:
        return f"Error: status code - {req.status_code}"




@app.route('/trending')
def trending_repos():
    today = datetime.date.today()
    one_month_ago = today - datetime.timedelta(days=30)
    one_month_ago_str = one_month_ago.strftime("%Y-%m-%d")

    params = {
        "q": f"created:>{one_month_ago_str}",
        "sort": "stars",
        "order": "desc",
        "per_page": 3
    }
    colors = {
            "Python": "#3776AB", # Blue
            "Java": "#B07219", # Brown
            "JavaScript": "#F7DF1E", # Yellow
            "C#": "#178600", # Green
            "C++": "#00599C", # Dark blue
            "PHP": "#777BB4", # Purple
            "R": "#198CE7", # Light blue
            "TypeScript": "#3178C6", # Cyan
            "Swift": "#FA7343", # Orange
            "C": "#438EFF", # Sky blue
            "Kotlin": "#F18E33", # Amber
            "Makefile": "#427B58", # Olive green
            "Others": "#666666" # gray 
    }
    response = requests.get("https://api.github.com/search/repositories", params=params, headers=headers)

    if response.status_code == 200:
        data = response.json()
        items = data["items"]
        repos = []
        print(f"Found {len(items)} trending repositories:")
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
        return render_template('repo_results.html', repos=repos, colors=colors, results=1)

    else:
        return f"Error: status code - {response.status_code}"

   
@app.route('/repos', methods=['GET'])
def search_repos():
    """ search repos by the given key word """
    q = request.args.get("q")
    sort_by = request.args.get('sort_by').split('_') if request.args.get('sort_by') else ['','']
    lang = request.args.get("language", "")

    if not q:
        return render_template('repo_results.html', results=-1)
    params = {
        'q': f'{q} language:"{lang}"',
        "sort": sort_by[0],
        "order": sort_by[1],
        "per_page": 3
    }
    colors = {
            "Python": "#3776AB", # Blue
            "Java": "#B07219", # Brown
            "JavaScript": "#F7DF1E", # Yellow
            "C#": "#178600", # Green
            "C++": "#00599C", # Dark blue
            "PHP": "#777BB4", # Purple
            "R": "#198CE7", # Light blue
            "TypeScript": "#3178C6", # Cyan
            "Swift": "#FA7343", # Orange
            "C": "#438EFF", # Sky blue
            "Kotlin": "#F18E33", # Amber
            "Makefile": "#427B58", # Olive green
            "Others": "#666666" # gray 
    }

    response = requests.get("https://api.github.com/search/repositories", params=params, headers=headers)

    if response.status_code == 200:
        data = response.json()
        items = data["items"]
        results_count = data['total_count']

        repos = []
        print(f"Found {len(items)} trending repositories:")
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
        return render_template('repo_results.html', repos=repos, colors=colors, results=results_count)
    else:
        return f"Error: status code - {response.status_code}"
    

@app.route('/testing')
def testing():
    colors = {
            "Python": "#3776AB", # Blue
            "Java": "#B07219", # Brown
            "JavaScript": "#F7DF1E", # Yellow
            "C#": "#178600", # Green
            "C++": "#00599C", # Dark blue
            "PHP": "#777BB4", # Purple
            "R": "#198CE7", # Light blue
            "TypeScript": "#3178C6", # Cyan
            "Swift": "#FA7343", # Orange
            "C": "#438EFF", # Sky blue
            "Kotlin": "#F18E33", # Amber
            "Makefile": "#427B58", # Olive green
            "Others": "#666666" # gray
    }

    # default
    # return "testing"
    
    # test /users/re
    users = [{'username': 'adamwiggins', 'avatar': '', 'html_url': 'https://github.com/adamwiggins', 'followers': 970, 'following': 16, 'bio': 'Digital toolmaker', 'location': 'Berlin', 'public_repos': 99, 'languages': [('Ruby', 70.0), ('Python', 6.67), ('Elm', 6.67), ('Others', 16.659999999999997)]}, {'username': 'emmvs', 'avatar': '', 'html_url': 'https://github.com/emmvs', 'followers': 55, 'following': 51, 'bio': 'Hey there 🤟', 'location': 'Berlin', 'public_repos': 38, 'languages': [('Ruby', 83.33), ('HTML', 6.67), ('Shell', 3.33), ('Others', 6.670000000000002)]}, {'username': 'plutov', 'avatar': '', 'html_url': 'https://github.com/plutov', 'followers': 583, 'following': 96, 'bio': 'Gopher https://www.youtube.com/packagemain', 'location': 'Berlin, Germany', 'public_repos': 53, 'languages': [('Go', 56.67), ('JavaScript', 6.67), ('Shell', 6.67), ('Others', 29.989999999999995)]}]
    # users = [{'username': 'ReVanced', 'followers': 15937, 'following': 0, 'public_repos': 28, 'languages': [('Java', 21.43), ('Kotlin', 21.43), ('Python', 14.29), ('Others', 42.85)]}, {'username': 'rengwuxian', 'followers': 7913, 'following': 25, 'public_repos': 60, 'languages': [('Kotlin', 93.33), ('Java', 6.67), ('Others', 0.0)]}, {'username': 'remy', 'followers': 7511, 'following': 6, 'public_repos': 333, 'languages': [('JavaScript', 56.67), ('HTML', 10.0), ('PHP', 6.67), ('Others', 26.659999999999997)]}]
    # users = [{'username': 'mattn', 'avatar': 'https://avatars.githubusercontent.com/u/10111?v=4', 'html_url': 'https://github.com/mattn', 'followers': 11177, 'following': 1705, 'bio': 'Long-time Golang user&contributor, Google Dev Expert for Go, and author of many Go tools, Vim plugin author. Windows hacker C#/Java/C/C++, GitHubStars\r\n', 'location': 'Osaka, Japan', 'public_repos': 1922, 'languages': [('Go', 40.0), ('Perl', 13.33), ('C', 6.67), ('Others', 40.0)]}, {'username': 'PacktPublishing', 'avatar': 'https://avatars.githubusercontent.com/u/10974906?v=4', 'html_url': 'https://github.com/PacktPublishing', 'followers': 8861, 'following': 0, 'bio': 'Providing books, eBooks, video tutorials, and articles for IT developers, administrators, and users.', 'location': 'Birmingham, UK', 'public_repos': 8089, 'languages': [('Python', 10.0), ('Rich Text Format', 6.67), ('Java', 6.67), ('Others', 76.66)]}, {'username': 'ghost', 'avatar': 'https://avatars.githubusercontent.com/u/10137?v=4', 'html_url': 'https://github.com/ghost', 'followers': 8170, 'following': 0, 'bio': "Hi, I'm @ghost! I take the place of user accounts that have been deleted.\n:ghost:\n", 'location': 'Nothing to see here, move along.', 'public_repos': 0, 'languages': [('Others', 100)]}, {'username': 'microsoftopensource', 'avatar': 'https://avatars.githubusercontent.com/u/22527892?v=4', 'html_url': 'https://github.com/microsoftopensource', 'followers': 4364, 'following': 0, 'bio': 'This is the open source management service account used for performing key GitHub operations on behalf of Microsoft employees and users.', 'location': 'Redmond, WA', 'public_repos': 0, 'languages': [('Others', 100)]}, {'username': 'ireade', 'avatar': 'https://avatars.githubusercontent.com/u/8677283?v=4', 'html_url': 'https://github.com/ireade', 'followers': 2902, 'following': 29, 'bio': 'Frontend Developer and User Interface Designer', 'location': None, 'public_repos': 126, 'languages': [('HTML', 36.67), ('CSS', 20.0), ('JavaScript', 20.0), ('Others', 23.33)]}, {'username': 'storybookjs', 'avatar': 'https://avatars.githubusercontent.com/u/22632046?v=4', 'html_url': 'https://github.com/storybookjs', 'followers': 2830, 'following': 0, 'bio': 'Build bulletproof user interfaces', 'location': None, 'public_repos': 105, 'languages': [('TypeScript', 53.33), ('JavaScript', 40.0), ('Others', 6.670000000000002)]}]
    return render_template('user_results.html', users=users, colors=colors, results=20)


    # test /repos/abc
    # repos = [{'name': 'abcd', 'description': None, 'html_url': 'https://github.com/nlpxucan/abcd', 'owner': 'nlpxucan', 'stars': 7640, 'forks': 596, 'topics': []}, {'name': 'abcjs', 'description': 'javascript for rendering abc music notation', 'html_url': 'https://github.com/paulrosen/abcjs', 'owner': 'paulrosen', 'stars': 1704, 'forks': 261, 'topics': ['abc-notation', 'abcjs', 'javascript', 'midi', 'music', 'music-notation', 'music-player', 'sheet-music']}, {'name': 'bitcoin-abc', 'description': 'Bitcoin ABC develops node software and infrastructure for the eCash project. This a mirror of the official Bitcoin-ABC repository.  Please see README.md', 'html_url': 'https://github.com/Bitcoin-ABC/bitcoin-abc', 'owner': 'Bitcoin-ABC', 'stars': 1126, 'forks': 720, 'topics': ['bitcoin', 'bitcoin-abc', 'ecash', 'xec']}, {'name': 'FlutterBasicWidgets', 'description': 'ABC of Flutter widgets. Intended for super beginners at Flutter. Play with 35+ examples in DartPad directly and get familiar with various basic widgets in Flutter', 'html_url': 'https://github.com/PoojaB26/FlutterBasicWidgets', 'owner': 'PoojaB26', 'stars': 864, 'forks': 286, 'topics': ['basic', 'beginner', 'dart', 'examples', 'flutter', 'playground', 'widgets']}, {'name': 'abc', 'description': 'ABC: System for Sequential Logic Synthesis and Formal Verification', 'html_url': 'https://github.com/berkeley-abc/abc', 'owner': 'berkeley-abc', 'stars': 737, 'forks': 478, 'topics': []}, {'name': 'ABCalendarPicker', 'description': 'Fully configurable iOS calendar UI component with multiple layouts and smooth animations.', 'html_url': 'https://github.com/k06a/ABCalendarPicker', 'owner': 'k06a', 'stars': 711, 'forks': 125, 'topics': []}, {'name': 'abc', 'description': 'A better Deno framework to create web application.', 'html_url': 'https://github.com/zhmushan/abc', 'owner': 'zhmushan', 'stars': 598, 'forks': 48, 'topics': ['deno', 'framework', 'http', 'server']}, {'name': 'ABCustomUINavigationController', 'description': 'Custom UINavigationController. SquaresFlips and Cube effects', 'html_url': 'https://github.com/andresbrun/ABCustomUINavigationController', 'owner': 'andresbrun', 'stars': 499, 'forks': 74, 'topics': []}, {'name': 'abc', 'description': 'Power of appbase.io via CLI, with nifty imports from your favorite data sources', 'html_url': 'https://github.com/appbaseio/abc', 'owner': 'appbaseio', 'stars': 459, 'forks': 50, 'topics': ['appbase', 'cli', 'elasticsearch', 'etl']}, {'name': 'RABCDAsm', 'description': 'Robust ABC (ActionScript Bytecode) [Dis-]Assembler', 'html_url': 'https://github.com/CyberShadow/RABCDAsm', 'owner': 'CyberShadow', 'stars': 413, 'forks': 98, 'topics': []}]
    # return render_template('repo_results.html', repos=repos)


    # test /trending
    # trending = [{'name': 'Startup-CTO-Handbook', 'description': "The Startup CTO's Handbook, a book covering leadership, management and technical topics for leaders of software engineering teams", 'html_url': 'https://github.com/ZachGoldberg/Startup-CTO-Handbook', 'owner': 'ZachGoldberg', 'stars': 8684, 'forks': 378, 'topics': []}, {'name': 'MemGPT', 'description': 'Teaching LLMs memory management for unbounded context 📚🦙', 'html_url': 'https://github.com/cpacker/MemGPT', 'owner': 'cpacker', 'stars': 5409, 'forks': 532, 'topics': ['chat', 'chatbot', 'gpt', 'gpt-4', 'llm', 'llm-agent']}, {'name': 'XAgent', 'description': 'An Autonomous LLM Agent for Complex Task Solving', 'html_url': 'https://github.com/OpenBMB/XAgent', 'owner': 'OpenBMB', 'stars': 4246, 'forks': 349, 'topics': []}, {'name': 'ChatGLM3', 'description': 'ChatGLM3 series: Open Bilingual Chat LLMs | 开源双语对话语言模型', 'html_url': 'https://github.com/THUDM/ChatGLM3', 'owner': 'THUDM', 'stars': 3658, 'forks': 292, 'topics': []}, {'name': 'openapi-devtools', 'description': 'Effortlessly discover API behaviour with a Chrome extension that automatically generates OpenAPI specifications in real time for any app or website', 'html_url': 'https://github.com/AndrewWalsh/openapi-devtools', 'owner': 'AndrewWalsh', 'stars': 3283, 'forks': 48, 'topics': ['api', 'chrome', 'devtools', 'generator', 'openapi', 'openapi3', 'specification']}, {'name': 'RemoveAdblockThing', 'description': 'Removes The "Ad blocker are not allowed on Youtube"', 'html_url': 'https://github.com/TheRealJoelmatic/RemoveAdblockThing', 'owner': 'TheRealJoelmatic', 'stars': 3174, 'forks': 126, 'topics': ['adblock', 'remove-not-allowed', 'tampermonkey', 'tampermonkey-userscript', 'youtube']}, {'name': 'semana-javascript-expert08', 'description': 'JS Expert Week 8.0 - 🎥Pre processing videos before uploading in the browser 😏', 'html_url': 'https://github.com/ErickWendel/semana-javascript-expert08', 'owner': 'ErickWendel', 'stars': 2523, 'forks': 1778, 'topics': ['demuxer', 'javascript', 'mp4', 'mp4box', 'muxer', 'video-processing', 'video-streaming', 'webcodecs', 'webm', 'webstream', 'webworker', 'workers']}, {'name': 'Wonder3D', 'description': 'A cross-domain diffusion model for 3D reconstruction from a single image', 'html_url': 'https://github.com/xxlong0/Wonder3D', 'owner': 'xxlong0', 'stars': 2008, 'forks': 110, 'topics': ['3d-aigc', '3d-generation', 'single-image-to-3d']}, {'name': 'smallchat', 'description': 'A minimal programming example for a chat server', 'html_url': 'https://github.com/antirez/smallchat', 'owner': 'antirez', 'stars': 1990, 'forks': 159, 'topics': []}, {'name': 'go-ethereum', 'description': 'Forked Golang execution layer implementation of the Ethereum protocol.', 'html_url': 'https://github.com/SidraChain/go-ethereum', 'owner': 'SidraChain', 'stars': 1759, 'forks': 491, 'topics': []}, {'name': 'sidra-contracts', 'description': 'Genesis Smart Contracts for Sidra Chain', 'html_url': 'https://github.com/SidraChain/sidra-contracts', 'owner': 'SidraChain', 'stars': 1640, 'forks': 517, 'topics': []}, {'name': 'fadblock', 'description': 'Friendly Adblock for YouTube: A fast, lightweight, and undetectable YouTube Ads Blocker for Chrome, Opera and Firefox.', 'html_url': 'https://github.com/0x48piraj/fadblock', 'owner': '0x48piraj', 'stars': 1601, 'forks': 49, 'topics': ['adblock', 'adguard', 'blocker', 'chrome', 'extension', 'firefox', 'javascript', 'opera', 'privacy', 'youtube']}, {'name': 'flexoki', 'description': 'An inky color scheme for prose and code.', 'html_url': 'https://github.com/kepano/flexoki', 'owner': 'kepano', 'stars': 1233, 'forks': 38, 'topics': ['alacritty', 'color', 'color-scheme', 'colors', 'iterm2', 'iterm2-color-scheme', 'kitty', 'neovim', 'neovim-colorscheme', 'terminal-colors', 'theme', 'vscode', 'vscode-theme', 'wezterm', 'wezterm-colorscheme', 'xresources']}, {'name': 'text-embeddings-inference', 'description': 'A blazing fast inference solution for text embeddings models', 'html_url': 'https://github.com/huggingface/text-embeddings-inference', 'owner': 'huggingface', 'stars': 1175, 'forks': 37, 'topics': ['ai', 'embeddings', 'huggingface', 'llm', 'ml']}, {'name': 'DreamCraft3D', 'description': 'Official implementation of DreamCraft3D: Hierarchical 3D Generation with Bootstrapped Diffusion Prior', 'html_url': 'https://github.com/deepseek-ai/DreamCraft3D', 'owner': 'deepseek-ai', 'stars': 1081, 'forks': 31, 'topics': ['3d-creation', '3d-generation', 'aigc', 'diffusion-models', 'generative-model', 'image-to-3d']}, {'name': '4K4D', 'description': '4K4D: Real-Time 4D View Synthesis at 4K Resolution', 'html_url': 'https://github.com/zju3dv/4K4D', 'owner': 'zju3dv', 'stars': 1080, 'forks': 23, 'topics': []}, {'name': 'Sistema-Anti-Fraude-Electoral', 'description': 'Sistema Open Source para Identificar potenciales fraudes electorales, minimizar su ocurrencia e impacto.', 'html_url': 'https://github.com/Las-Fuerzas-Del-Cielo/Sistema-Anti-Fraude-Electoral', 'owner': 'Las-Fuerzas-Del-Cielo', 'stars': 1076, 'forks': 185, 'topics': []}, {'name': 'geist-font', 'description': None, 'html_url': 'https://github.com/vercel/geist-font', 'owner': 'vercel', 'stars': 1045, 'forks': 24, 'topics': ['font', 'variable-fonts']}, {'name': 'distil-whisper', 'description': None, 'html_url': 'https://github.com/huggingface/distil-whisper', 'owner': 'huggingface', 'stars': 962, 'forks': 20, 'topics': ['audio', 'speech-recognition', 'whisper']}, {'name': 'zero123plus', 'description': 'Code repository for Zero123++: a Single Image to Consistent Multi-view Diffusion Base Model.', 'html_url': 'https://github.com/SUDO-AI-3D/zero123plus', 'owner': 'SUDO-AI-3D', 'stars': 921, 'forks': 59, 'topics': ['3d', '3d-graphics', 'aigc', 'diffusers', 'diffusion-models', 'image-to-3d', 'research-project', 'text-to-3d']}]
    # return render_template('trending_repos.html', repos=trending)



if __name__ == '__main__':
    app.run(debug=True)