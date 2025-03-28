#!/usr/bin/env python
import os, sys, logging, asyncio, hypercorn.asyncio, debugpy, time  # Core libraries and async server
from quart import Quart, current_app, request, jsonify, Blueprint, Response  # Quart framework imports
from threading import Thread
from routes.frontend import frontend_bp
from routes.processing import processing_bp
from services import config
from watchgod import run_process


# Create a Quart application instance
app = Quart(__name__)

# Global request queue for handling asynchronous processing
request_queue = asyncio.Queue()

# Register application blueprints for different API functionalities
#app.register_blueprint(documents_bp)  
#app.register_blueprint(status_bp)  
app.register_blueprint(frontend_bp)  
app.register_blueprint(processing_bp)  

# Event for handling server shutdown gracefully
shutdown_event = asyncio.Event()

""" 
Gracefully shuts down the Quart server.
Logs the shutdown event, sets the shutdown flag, 
waits briefly for cleanup, and exits the process.
"""
async def stopServer():
    logging.info("Server is shutting down...")
    shutdown_event.set()  # Set shutdown event flag
    await asyncio.sleep(1)  # Small delay to allow cleanup
    sys.exit(0)  # Terminate the process

""" 
Background worker that continuously processes queued requests.
- Waits for new tasks in `request_queue`
- Processes each task asynchronously
- Logs any errors that occur during processing
"""
async def background_task():
    logging.info("Starting background queue processor...")

    while True:
        queue_entry = await request_queue.get()  # Wait until a new request is available
        try:
            async with app.app_context():  # Ensure Quart app context is available
                logging.info(f"Processing queue entry: {queue_entry}") 
                await app.config["COLLECTOR"].process_queue(queue_entry)  # Call the processing function
        except Exception as e:
            logging.error(f"Error processing queue entry: {e}")  # Log any errors
        finally:
            request_queue.task_done()  # Mark task as completed

""" 
Initializes configurations and services before the server starts.
- Validates application configuration
- Initializes the PAPERLESS API connection
- Sets up the global request queue
- Starts the background queue processor
"""
@app.before_serving
async def init_before_serving():
    logging.info("Starting pre-server initialization...")

    app.config["REQUEST_QUEUE"] = request_queue  # Store the request queue in app config
    # Start the background queue processing task
    app.config["BACKGROUND_TASK"] = asyncio.create_task(background_task())
    
    # Apply configuration settings from the `config` module
    config.setConfig(app)
   
    logging.info("Pre-server initialization complete.")

""" 
Main entry point for starting the Quart application.
- Configures logging
- Enables remote debugging if `DEBUG=True`
- Initializes the application
- Starts the Hypercorn server
"""
async def main(debug):
    logLevel = "DEBUG" if debug == 'True' else "INFO"  # Set log level accordingly

    # Config the Root-Logger
    logging.basicConfig(
        level=getattr(logging, logLevel, logging.INFO),
        format="%(asctime)s [%(levelname)s] %(message)s",
        handlers=[logging.StreamHandler(sys.stdout)]
    )

    # Set the LogLevel for the frameworks
    logging.getLogger("quart").setLevel(getattr(logging, logLevel, logging.INFO))
    logging.getLogger("hypercorn").setLevel(getattr(logging, logLevel, logging.INFO))
    logging.getLogger("asyncio").setLevel(getattr(logging, logLevel, logging.INFO))

    logging.info(f"LogLevel is set to {logLevel}")

    # Enable remote debugging if debug mode is active
    if debug == 'True':
        logging.info("Starting Debugpy...")
        debugpy.listen(("0.0.0.0", 3001))  # Open debugging port 5679
        logging.info("Waiting for debugger connection...")
        debugpy.wait_for_client()  # Pause execution until debugger is attached

    logging.info("Starting application initialization...")

    await init_before_serving()  # Run pre-start initialization tasks

    logging.info("Initialization complete, starting server...")

    # Configure and start the Hypercorn web server
    conf = hypercorn.Config()
    conf.bind = ["0.0.0.0:5000"]  # Set the server to listen on port 5000
    conf.accesslog = "-"  # Enable access logging
    conf.errorlog = "-"  # Enable error logging

    await hypercorn.asyncio.serve(app, conf)  # Start Quart application with Hypercorn

def debugStart():
    asyncio.run(main("True"))

# Ensure the application runs when executed as a script
if __name__ == '__main__':
    debug = os.getenv('DEBUG', 'False')  # Fetch debug mode from environment variables
    if debug == "True":
        run_process(".", debugStart)
    else:
        asyncio.run(main(debug))
