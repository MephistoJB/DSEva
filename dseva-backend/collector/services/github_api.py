import os, logging, random, requests
from quart import current_app
from github import Github # type: ignore
from github import Auth # type: ignore
from github import Repository # type: ignore

class Github_API:
    def __init__(self, githubtoken, logger: logging.Logger):
        self._logger = logger
        self._connection = None
        if githubtoken:
            self._githubtoken = githubtoken
            self._connection = self.getConnection()
        self._localrepolist = []

    def getConnection(self):
        if not self._githubtoken:
            logging.info("Github connection could not be established. No Github Token passed.")
            return None
        if not self._connection:
            auth = Auth.Token(self._githubtoken)
            self._connection = Github(auth=auth)
            logging.info("Github connection established ")
        return self._connection

    def getRateLimit(self, refresh=True, header=None):
        remaining_event = current_app.config["REMAINING_EVENT"]
        if not header:
            if refresh:
                if(self.getConnection()):
                    ratelimit = self.getConnection().get_rate_limit()
                    core = ratelimit.core
                    current_app.config["RATELIMIT"] = {
                        "limit": core.limit,
                        "remaining": core.remaining,
                        "used": core.used,
                        "reset": core.reset
                    }
                    remaining_event.set()  # Trigger update for nextelements stream

        else:
            ratelimit = current_app.config["RATELIMIT"]
            if ratelimit['limit'] != header.get("x-ratelimit-limit"):
                ratelimit['limit'] = header.get("x-ratelimit-limit")
                remaining_event.set()
            if ratelimit['remaining'] != header.get("x-ratelimit-remaining"):
                ratelimit['remaining'] = header.get("x-ratelimit-remaining")
                remaining_event.set()
            if ratelimit['used'] != header.get("x-ratelimit-used"):
                ratelimit['used'] = header.get("x-ratelimit-used")
                remaining_event.set()
            if ratelimit['used'] != header.get("x-ratelimit-used"):
                ratelimit['reset'] = header.get("x-ratelimit-reset")
                remaining_event.set()
        return current_app.config["RATELIMIT"]

    def closeConnection(self, ):
        try:
            self.getConnection().close()
            print("Github connection closed ")
        except Exception as error:
            # handle the exception
            print("An exception occurred:", error)

    def getFallback(self):
        list = self.getConnection().get_user().get_repos()
        repo = None
        for i in range(0, list.totalCount-1):
            repo = list[i]
            for j in range (0,len(localrepolist)):
                if(repo.id == self._localrepolist[j]):
                    repo = None
                break
            if repo:
                self._localrepolist.append(repo.id)
                return repo
        return None

    def getRepo(self, id: int):
        id = int(id)
        repo = self.getConnection().get_repo(id)
        head = repo.raw_headers
        self.getRateLimit(refresh=False, header=head)
        return repo

    def getDev(self, id: int):
        id = int(id)
        dev = self.getConnection().get_user_by_id(id)
        head = dev.raw_headers
        self.getRateLimit(refresh=False, header=head)
        return dev

    def repoToJSON(self, repo: Repository):
        return None

    def getForkIDs(self, repo):
        headers = {"Authorization": f"Bearer {self._githubtoken}"}
        if(repo.forks_count>0):
            response = requests.get(repo.forks_url, headers=headers)
            if response and response.status_code==200 and response.text !="[]":
                head = response.headers.get('_store')
                self.getRateLimit(refresh=False, header=head)
                return response.json()
        else:
            return []
    def convertHeaderFromPlainResponse(self, response):
        store = response.headers._store
        head = {
                "x-ratelimit-limit": store['x-ratelimit-limit'][1],
                "x-ratelimit-remaining": store['x-ratelimit-remaining'][1],
                "x-ratelimit-used": store['x-ratelimit-used'][1],
                "x-ratelimit-reset": store['x-ratelimit-reset'][1]
            }
        return head
        ratelimit['remaining'] = header.get("x-ratelimit-remaining")
        ratelimit['used'] = header.get("x-ratelimit-used")
        ratelimit['reset'] = header.get("x-ratelimit-reset")
    def getRepoIDs(self, dev):
        headers = {"Authorization": f"Bearer {self._githubtoken}"}
        if(dev.public_repos>0):
            response = requests.get(dev.repos_url, headers=headers)
            if response and response.status_code==200 and response.text !="[]":
                head = self.convertHeaderFromPlainResponse(response)
                self.getRateLimit(refresh=False, header=head)
                return response.json()
        else:
            return []

    def getParent(self, repo):
        return repo.parent