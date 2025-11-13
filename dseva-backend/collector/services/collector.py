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
                logging.debug(f"handling Developer with id {element['foreign_id']}") 
                repos = github_api.getRepoIDs(neGH)
                for repo in repos:
                    repo["devGUID"] = element["id"]
                    logging.debug(f"handling repo {repo['name']} with id {repo['id']}") 
                    success = await backend_api.create_and_update_repository(repo)
                    if success:
                        logging.debug(f"repo {repo['name']} with id {repo['id']} handled successfully") 
                    else:
                        logging.error(f"repo {repo['name']} with id {repo['id']} not handled")
                success = await backend_api.create_and_update_developer(neGH)
                if success:
                    logging.debug(f"developer {element['name']} with id {element['foreign_id']} handled successfully") 
                else:
                    logging.error(f"developer {element['name']} with id {element['foreign_id']} not handled")
            else:
                logging.debug(f"handling Repo {element['title']} with id {element['foreign_id']}") 
                neGH = github_api.getRepo(element["foreign_id"])
                parent = github_api.getParent(neGH)
                if(parent):
                    logging.debug(f"handling Repo {element['title']} with id {element['foreign_id']}") 
                    success = await backend_api.create_and_update_repository(parent)
                    if success:
                        logging.debug(f"repo {parent['name']} with id {parent['id']} handled successfully") 
                    else:
                        logging.error(f"repo {parent['name']} with id {parent['id']} not handled")
                forks = github_api.getForkIDs(neGH)
                for fork in forks:
                    fork["parentGUID"] = element["id"]
                    logging.debug(f"handling Repo {fork['full_name']} with id {fork['id']}") 
                    success = await backend_api.create_and_update_repository(fork)
                    if success:
                        logging.debug(f"repo {fork['full_name']} with id {fork['id']} handled successfully") 
                    else:
                        logging.error(f"repo {fork['full_name']} with id {fork['id']} not handled")
                success = await backend_api.create_and_update_repository(neGH)
                if success:
                    logging.debug(f"repo {element['title']} with id {element['foreign_id']} handled successfully") 
                else:
                    logging.error(f"repo {element['title']} with id {element['foreign_id']} not handled")
        else:
            repo = github_api.getFallback()
            if repo:
                if not backend_api.getRepository(repo.id):
                    success = await backend_api.create_and_update_repository(repo)
            else:
                logging.error("All repositories grabbed. Need a new fallback")