import os
import random
from github import Github # type: ignore
from github import Auth # type: ignore
from github import Repository # type: ignore
import requests # type: ignore

githubtoken = os.environ.get("GITHUB_TOKEN")
con = None
buffer = int(os.environ.get("GITHUB_BUFFER") if os.environ.get("GITHUB_BUFFER") else 200)
localrepolist = []

if not githubtoken:
    print("No Github Token found. Please define Github Token in the ENV. Exiting")
    exit()

def authenticate():
    auth = Auth.Token(githubtoken)
    global con
    con = Github(auth=auth)
    print("Github connection established ")

def getRateLimit():
    if(con):
        temp = con.get_rate_limit()
        return temp.core

def closeConnection():
    try:
        con.close()
        print("Github connection closed ")
    except Exception as error:
        # handle the exception
        print("An exception occurred:", error)

def getBuffer():
    return buffer

def getFallback():
    list = con.get_user().get_repos()
    repo = None
    for i in range(0, list.totalCount-1):
        repo = list[i]
        for j in range (0,len(localrepolist)):
            if(repo.id == localrepolist[j]):
               repo = None
               break
        if repo:
            localrepolist.append(repo.id)
            return repo
    return None

def getRepo(id: int):
    id = int(id)
    repo = con.get_repo(id)
    return repo

def repoToJSON(repo: Repository):
    return None

def getForkIDs(repo):
    if(repo.forks_count>0):
        response = requests.get(repo.forks_url)
        if response and response.status_code==200 and response.text !="[]":
            return response.json()
    else:
        return []

def getParent(repo):
    return repo.parent