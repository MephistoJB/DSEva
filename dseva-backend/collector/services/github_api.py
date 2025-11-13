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
                    try:
                        ratelimit = self.getConnection().get_rate_limit()
                        
                        # Handle different PyGithub API versions
                        if hasattr(ratelimit, 'core'):
                            # Old PyGithub API (v1.x)
                            core = ratelimit.core
                            current_app.config["RATELIMIT"] = {
                                "limit": core.limit,
                                "remaining": core.remaining,
                                "used": core.used,
                                "reset": core.reset
                            }
                        else:
                            # New PyGithub API (v2.x+) - RateLimitOverview structure
                            # The RateLimitOverview has different attributes
                            current_app.config["RATELIMIT"] = {
                                "limit": 5000,  # Default GitHub API limit
                                "remaining": 5000,  # Default remaining
                                "used": 0,  # Default used
                                "reset": 0  # Default reset time
                            }
                            
                            # Try to extract actual values if possible
                            # In newer versions, the structure might be different
                            # For now, we'll use the GitHub API directly to get rate limit info
                            import requests
                            headers = {"Authorization": f"Bearer {self._githubtoken}"}
                            response = requests.get("https://api.github.com/rate_limit", headers=headers)
                            if response.status_code == 200:
                                rate_data = response.json()
                                current_app.config["RATELIMIT"] = {
                                    "limit": rate_data["resources"]["core"]["limit"],
                                    "remaining": rate_data["resources"]["core"]["remaining"],
                                    "used": rate_data["resources"]["core"]["used"],
                                    "reset": rate_data["resources"]["core"]["reset"]
                                }
                        
                        remaining_event.set()  # Trigger update for nextelements stream
                    except Exception as e:
                        print(f"Error getting rate limit: {e}")
                        # Fallback to default values
                        current_app.config["RATELIMIT"] = {
                            "limit": 5000,
                            "remaining": 5000,
                            "used": 0,
                            "reset": 0
                        }

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
            for j in range (0,len(self._localrepolist)):
                if(repo.id == self._localrepolist[j]):
                    repo = None
                break
            if repo:
                self._localrepolist.append(repo.id)
                return repo
        return None

    def checkRateLimit(self):
        ratelimit = current_app.config["RATELIMIT"].get("remaining")
        buffer = current_app.config["BUFFER"]
        while(ratelimit<= buffer):
            # Wait for rate limit reset - 1 hour loop with 5-minute status updates
            import time
            wait_time = 3600  # 1 hour in seconds
            check_interval = 300  # 5 minutes in seconds
            start_time = time.time()
            
            logging.info(f"Rate limit exceeded. Starting 1-hour wait loop...")
            
            while time.time() - start_time < wait_time:
                elapsed = int(time.time() - start_time)
                remaining = wait_time - elapsed
                logging.info(f"Rate limit wait: {elapsed}s elapsed, {remaining}s remaining")
                time.sleep(check_interval)
                
            logging.info("Rate limit wait completed. Resuming operations...")
            self.getRateLimit(refresh=False, header=None)

    def getRepo(self, id):
        self.checkRateLimit()
        # Handle different ID formats that might come from the backend
        try:
            # If it's already an integer, use it directly
            if isinstance(id, int):
                repo_id = id
            else:
                # Handle string formats like "['236134905']" or "236134905"
                id_str = str(id).strip()
                # Remove brackets and quotes if present
                if id_str.startswith('[') and id_str.endswith(']'):
                    id_str = id_str[1:-1]  # Remove outer brackets
                if id_str.startswith("'") and id_str.endswith("'"):
                    id_str = id_str[1:-1]  # Remove outer quotes
                if id_str.startswith('"') and id_str.endswith('"'):
                    id_str = id_str[1:-1]  # Remove outer quotes
                repo_id = int(id_str)
            
            repo = self.getConnection().get_repo(repo_id)
            head = repo.raw_headers
            self.getRateLimit(refresh=False, header=head)
            return repo
        except (ValueError, TypeError) as e:
            logging.error(f"Error parsing repo ID '{id}': {e}")
            return None

    def getDev(self, id):
        self.checkRateLimit()
        # Handle different ID formats that might come from the backend
        try:
            # If it's already an integer, use it directly
            if isinstance(id, int):
                dev_id = id
            else:
                # Handle string formats like "['236134905']" or "236134905"
                id_str = str(id).strip()
                # Remove brackets and quotes if present
                if id_str.startswith('[') and id_str.endswith(']'):
                    id_str = id_str[1:-1]  # Remove outer brackets
                if id_str.startswith("'") and id_str.endswith("'"):
                    id_str = id_str[1:-1]  # Remove outer quotes
                if id_str.startswith('"') and id_str.endswith('"'):
                    id_str = id_str[1:-1]  # Remove outer quotes
                dev_id = int(id_str)
            
            dev = self.getConnection().get_user_by_id(dev_id)
            head = dev.raw_headers
            self.getRateLimit(refresh=False, header=head)
            return dev
        except (ValueError, TypeError) as e:
            logging.error(f"Error parsing dev ID '{id}': {e}")
            return None

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