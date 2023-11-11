# Gitify 

Gitify is a GitHub Stats API that allows users to retrieve comprehensive statistics and insights for any GitHub user. This API provides a user-friendly interface to access a wide range of data related to GitHub users, repositories, commits, followers, etc. It also allows users to sort the search by number of stars, most forks,updates etc.

![GitHub Image](https://crowdbotics.ghost.io/content/images/2019/07/github.jpg)

## Table of Contents
- [Project Overview](#Project Overview)
- [key Functionality](#Key Functionality)
- [Environment](#environment)
- [Usage](#usage)
- [Examples of Use](#examples-of-use)
- [Issues](#issues)
- [ATHORS](#Authors)
- [Deployment](Deployment)

## Project Overview

The objective of this project is to create a user-friendly API that simplifies the process of retrieving and presenting GitHub user statistics. It retrieves information such as repository details, follower and following counts, trending repositories, and more. Whether you're a developer assessing your GitHub activity or an organization looking to analyzing contribution of your employees,looking to hire new developer in the companies. Gitify allows you to easily access their stats. Users can search for trending repositories, Gitify offers these features and more.

## Key Functionalities

- **User Stats:** Retrieve detailed statistics about a GitHub user, including their repositories, commits,languages, followers, and following.

- **Repository Insights:** Get in-depth information about a specific GitHub repository, including contributors, commit history, and open issues.

- **User Search:** Search for GitHub users based on various criteria, such as programming language expertise or location.

- **Recent Activity:** Monitor a user's recent GitHub activity, including push events, issue creation, and pull request activity.

- **Collaboration Metrics:** Assess user collaboration by analyzing contributions to other repositories and pull request reviews.

## Environment

The Gitify is developed using python and flask. It interacts with the GitHub API and requires the use of OAuth tokens for authentication.
dependencies - python, flask, requests.
## Usage

clone the repo.
add github access token. for ubuntu `export ACCESS_TOKEN="place_your_token_here"`
run `python app.py` # it will open the app with the debuggin on
navigate to home page http://127.0.0.1:5000

## Examples of Use
to look for trending repositories - `http://127.0.0.1:5000/trending`
to search for users by user name - `http://127.0.0.1:5000/users`- type key words in the search bar to get results
to search for repositories - `http://127.0.0.1:5000/repos`type key words in the search bar to get results


See practical examples of how to use the GitHub Stats API in the [Examples of Use](#examples-of-use) section. These examples help you understand how to leverage the API's capabilities.

## Issues

If you encounter any issues or bugs while using the GitHub Stats API, please report them in the [Issues](#issues) section. We appreciate your feedback and will work to resolve any problems promptly.

## Authors

Tebogo Legoabe - [Github](https://github.com/TebogoLegoabe) / [LinkedIn](https://www.linkedin.com/in/tebogo-legoabe)
Shakir Muhammedsaid - [Github](https://github.com/Shakir-ahmed1) / [LinkedIn](https://www.linkedin.com/in/shakir-ahmedsalih10)

## Link to Deployed site

Gitify - [Gitify](http://web-02.shakir.tech/gitify)
