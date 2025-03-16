from restoperations import *
from githuboperations import *

def startcollector():
    try:
        authenticate()

    


        run = True
        while run:
            rl=getRateLimit()
            if(rl.remaining - getBuffer() <= 0):
                print("Github API limit is reaching. need to wait until " + str(rl.reset))
            else:
                ne = getNextElement()
                if(ne):
                    neGH = getRepo(ne["foreign_id"])
                    #print(ne)
                    #print(neGH)
                    parent = getParent(neGH)
                    if(parent):
                        create_and_update_repository(parent)
                    forks = getForkIDs(neGH)
                    for fork in forks:
                        fork["parentGUID"] = ne["id"]
                        create_and_update_repository(fork)
                else:
                    repo = getFallback()
                    if repo:
                        if not getRepository(repo.id):
                            create_and_update_repository(repo)
                    else:
                        print("Bereits alle Repositories überführt. Neuer Fallback benötigt.")
                        run = False


    except Exception as error:
        raise(error)
    finally:
        closeConnection()
        
startcollector()