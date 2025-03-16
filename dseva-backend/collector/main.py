#!/usr/bin/env python
import os, logging, time, sys
from flask import Flask
from threading import Thread
from restoperations import *
from githuboperations import *
#from collector import *


class Collector(Flask):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.worker_thread = None

    def run(self, host=None, port=None, debug=None, extra_files=None, on_load=None, use_reloader=True, use_debugger=None, use_evalex=None, passthrough_errors=False, ssl_context=None, threaded=False, processes=None, ssl_keyfile=None, ssl_certfile=None):
        super().run(host=host, port=port, debug=debug, extra_files=extra_files, on_load=on_load, use_reloader=use_reloader, use_debugger=use_debugger, use_evalex=use_evalex, passthrough_errors=passthrough_errors, ssl_context=ssl_context, threaded=threaded, processes=processes, ssl_keyfile=ssl_keyfile, ssl_certfile=ssl_certfile)
        self.start_worker()

    def start_worker(self):
        if not self.worker_thread:
            self.worker_thread = Thread(target=self.additional_method)
            self.worker_thread.daemon = True
            self.worker_thread.start()

    def startcollector(self):
        try:
            authenticate()

            run = True
            while run:
                rl=getRateLimit()
                if(rl.remaining - getBuffer() <= 0):
                    logging.info("Github API limit is reaching. need to wait until " + str(rl.reset))
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

# Flask-App-Instanz erstellen
app = Flask(__name__)

LOG_LEVEL = os.getenv('LOG_LEVEL', None)
DEBUG = os.environ.get("DEBUG", "0")

# Create Logger
logger = logging.getLogger(__name__)

if LOG_LEVEL:
    if LOG_LEVEL == "ERROR":
        logger.setLevel(logging.ERROR)
    elif LOG_LEVEL == "WARNING":
        logger.setLevel(logging.WARNING)
    elif LOG_LEVEL == "INFO":
        logger.setLevel(logging.INFO)
    elif LOG_LEVEL == "DEBUG":
        logger.setLevel(logging.DEBUG)
    else:
        logging.basicConfig(
            level=logging.DEBUG,
            format="%(asctime)s [%(levelname)s] %(message)s",
            handlers=[
                logging.StreamHandler(sys.stdout)
            ]
        )
        logging.error("Log Level not set correctly. Please choose from ERROR, WARNING, INFO or DEBUG")
else:
    logger.setLevel(logging.INFO)

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)
if LOG_LEVEL:
    logging.info(f"LogLevel is set to {LOG_LEVEL}")
else:
    logging.info(f"LogLevel is set to INFO")

logging.info(f"Checking Config")

#TODO ConfigCheck

if(DEBUG and DEBUG=="1"):
    logging.info(f"DEBUG Mode activated.")

app.config['DEBUG'] = DEBUG

def main():

    # start Python Debugger
    debug = os.environ.get("DEBUG")
    print(debug)
    if debug=="1":
        print(debug=="1")
        import debugpy
        debugpy.listen(("0.0.0.0", 3001))
        print('Attached!')
    # end Python Debugger

    #startcollector()
while 1 != 2:
    time.sleep(2)

if __name__ == '__main__':
    main()
    #if app.config['DEBUG'] and app.config['DEBUG']=="1":
    #    import debugpy
    #    debugpy.listen(("0.0.0.0", 3002))
    #    logging.info('DebugPy attached!')
    #    app.run(host='0.0.0.0', port=5000)
    #else:
    #    app.run(host='0.0.0.0', port=5000)
