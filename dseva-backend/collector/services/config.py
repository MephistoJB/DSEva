import logging, os, re, asyncio
from services.github_api import Github_API
from services.collector import Collector
from services.backend_api import Backend_API

# Load environment variables for configuration
DEBUG = os.getenv('DEBUG', 'False')
BUFFER = int(os.getenv('BUFFER', 200))
GITHUB_TOKEN = os.environ.get("GITHUB_TOKEN", None)
BACKEND_URL = os.environ.get("BACKEND")

# Define application version
def get_current_version_from_releasenotes(filepath: str) -> str:
    with open(filepath, "r") as file:
        first_line = file.readline().strip()
        version = first_line.split(" -")[0]  # Trennt am ersten " -"
        return version
    
VERSION = get_current_version_from_releasenotes("releasenotes")

"""
Configures the Quart application with necessary settings.

Parameters:
- app (Quart): The Quart application instance.

Sets:
- Various configuration values such as AI settings, API endpoints, and debugging options.
"""
def setConfig(app):
    app.config["VERSION"] = VERSION
    app.config["BUFFER"] = BUFFER
    app.config["RUNNING"] = os.environ.get("IMMIDIATESTART", False)
    app.config["RATELIMIT"] = None
    app.config["NEXT_ELEMENT_EVENT"] =  asyncio.Event()
    app.config["REMAINING_EVENT"] =  asyncio.Event()
    app.config["RUNNING_EVENT"] =  asyncio.Event()

    if GITHUB_TOKEN:
        app.config["GITHUB_TOKEN"] = GITHUB_TOKEN
        app.config["GITHUB_API"] = Github_API(GITHUB_TOKEN, logging)
        app.config["COLLECTOR"] = Collector(logging)
    else:
        logging.error("No Github Token found. Please define Github Token in the ENV. No Github Operations possible")
    
    if BACKEND_URL:
        app.config["BACKEND"] = Backend_API(BACKEND_URL, logging)