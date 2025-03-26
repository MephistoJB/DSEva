from typing import List
import logging, requests, os, json
from github import Repository # type: ignore

class Backend_API:
    def __init__(self, backend_url, logger: logging.Logger):
        self._logger = logger
        self._backend_url = backend_url

    async def get_allrepositories(self):
        get_all_repositories_url = self._backend_url + "repositories/"
        response = requests.get(get_all_repositories_url)
        return response.json()["data"]

    async def get_alldevelopers(self):
        get_all_developer_url = self._backend_url + "developer/"
        response = requests.get(get_all_developer_url)
        return response.json()["data"]

    async def create_and_update_repository(self, repo: Repository):
        if(getattr(repo, 'full_name', None)):
            data = {"title":repo.full_name, "foreign_id":repo.id, "ownerD":repo.owner.id}
        else:
            data = {"title":repo['full_name'], "foreign_id":repo['id'], "ownerD":repo['owner']['id']}
            if repo.get('parentGUID'):
                data["parent"] = repo['parentGUID']
        create_and_update_repository_url = self._backend_url + "create_and_update_repository/"
        response = requests.post(create_and_update_repository_url, data = data)
        return response.json()

    async def create_developer(self, data: dict):
        create_developer_url = self._backend_url + "developer/"
        response = requests.post(create_developer_url, data = data)
        return response.json()

    async def getNextElement(self):
        get_next_element_url = self._backend_url + "nextelement/"
        response = requests.get(get_next_element_url)
        return response.json()["data"]

    async def getRepository(self, id: int):
        get_repositorydetails_url = self._backend_url + str(id) + "/"
        response = requests.get(get_repositorydetails_url)
        if(response.status_code == 200):
            return response.json()
        return {}