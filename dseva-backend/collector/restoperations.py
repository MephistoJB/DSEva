from typing import List
import requests # type: ignore
import os
from github import Repository # type: ignore
#from models import *
import json

api_url = os.environ.get("BACKEND")
def get_allrepositories():
    get_all_repositories_url = api_url + "repositories/"
    response = requests.get(get_all_repositories_url)
    return response.json()["data"]

def get_alldevelopers():
    get_all_developer_url = api_url + "developer/"
    response = requests.get(get_all_developer_url)
    return response.json()["data"]

def create_and_update_repository(repo: Repository):
    if(getattr(repo, 'full_name', None)):
        data = {"title":repo.full_name, "foreign_id":repo.id}
    else:
        data = {"title":repo['full_name'], "foreign_id":repo['id']}
        if(repo['parentGUID']):
            data["parent"] = repo['parentGUID']
    create_and_update_repository_url = api_url + "create_and_update_repository/"
    response = requests.post(create_and_update_repository_url, data = data)
    return response.json()

def create_developer(data: dict):
    create_developer_url = api_url + "developer/"
    response = requests.post(create_developer_url, data = data)
    return response.json()

def getNextElement():
    get_next_element_url = api_url + "nextelement/"
    response = requests.get(get_next_element_url)
    return response.json()["data"]

def getRepository(id: int):
    get_repositorydetails_url = api_url + str(id) + "/"
    response = requests.get(get_repositorydetails_url)
    if(response.status_code == 200):
        return response.json()
    return {}