import logging
from quart import current_app

class Collector:
    def __init__(self, logger: logging.Logger):
        self._logger = logger


    async def process_queue(self, data: dict) -> None:
        try:
            github_api = current_app.config["GITHUB_API"]
            buffer = current_app.config["BUFFER"]
            if not github_api:
                return
            if not data:
                return  # Skip processing if data is empty
            logging.info(f"Processing request: {data}")
            ratelimit = github_api.getRateLimit()
            if(ratelimit.get("remaining") - buffer <= 0):
                logging.info("Github API limit is reaching. need to wait until " + str(ratelimit.reset))
                ####### TODO warteschleife muss hier noch rein #########

            success = await self.collect(github_api, data)
            return True
        except Exception as e:
            logging.error(f"Error in queue processing: {e}")

    async def collect(self, github_api, element):
        backend_api = current_app.config["BACKEND"]
        if(element):
            if element.get("type","")=='Developer':
                neGH = github_api.getDev(element["foreign_id"])
                repos = github_api.getRepoIDs(neGH)
                for repo in repos:
                    repo["devGUID"] = element["id"]
                    success = await backend_api.create_and_update_repository(repo)
            else:
                neGH = github_api.getRepo(element["foreign_id"])
                parent = github_api.getParent(neGH)
                if(parent):
                    success = await backend_api.create_and_update_repository(parent)
                forks = github_api.getForkIDs(neGH)
                for fork in forks:
                    fork["parentGUID"] = element["id"]
                    success = await backend_api.create_and_update_repository(fork)
                success = await backend_api.create_and_update_repository(neGH)
        else:
            repo = github_api.getFallback()
            if repo:
                if not backend_api.getRepository(repo.id):
                    success = await backend_api.create_and_update_repository(repo)
            else:
                logging.error("All repositories grabbed. Need a new fallback")