""" this is not 100% accurate result of language percentages
    use none lite versions for more accurate results
"""
import requests
from os import getenv
access_token = getenv("ACCESS_TOKEN")
headers = {
    'Authorization': f'token {access_token}',
    'Accept': 'application/vnd.github.v3+json',
}

def get_languages_lite(api_url):
    """ it returns lanugage usage percentage of repositories using main languages
    NOTE: does only one request and is not 100% accurate
    USAGE: get_languages_lite("https://api.github.com/users/{user_name}/repos") # repositories url

    """
    response = requests.get(api_url, headers=headers)
    if response.status_code == 200:
        repos = response.json()
        language_counts = {}
        language_percentages = {}
        for repo in repos:
            language = repo["language"]
            if language is not None:
                language_counts[language] = language_counts.get(language, 0) + 1
        total_repos = len(repos)

        for language, count in language_counts.items():
            percentage = round(count / total_repos * 100, 2)
            language_percentages[language] = percentage
        return language_percentages


def get_language_percentage_one_repo_lite(api_url):
    """ gets the langauges percentages of the given repo
        USAGE:  get_language_percentage_one_repo_lite("https://api.github.com/repos/{repository_name}/{user_name}/languages")
    """
    response = requests.get(api_url, headers=headers)

    if response.status_code == 200:
        languages = response.json()
        language_percentages = {}
        total_bytes = sum(languages.values())

        # Loop through each language and its bytes calculates their percentage
        for language, bytes in languages.items():
            percentage = round(bytes / total_bytes * 100, 2)
            language_percentages[language] = percentage
        return language_percentages
    else:
        return None
    
if __name__ == "__main__":
    print("--------------------------------------")
    print(get_language_percentage_one_repo_lite("https://api.github.com/repos/creytiv/re/languages"))
    print("--------------------------------------")
    print(get_languages_lite("https://api.github.com/users/krasimir/repos"))
