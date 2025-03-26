from quart import Blueprint, jsonify, render_template, current_app, Response  # Import necessary modules
import asyncio
import json

# Blueprint for handling frontend routes
frontend_bp = Blueprint("frontend", __name__)

"""
Handles the root route and renders the main frontend page.

Returns:
- HTML page (index.html) with injected version number and button tags.
"""
@frontend_bp.route('/')
async def index():
    current_app.config["GITHUB_API"].getRateLimit()
    return await render_template(
        "index.html",
        version=current_app.config["VERSION"],
        running=current_app.config["RUNNING"],
    )

@frontend_bp.route('/infos/ratelimit')
async def ratelimit_stream():
    app = current_app._get_current_object()
    remaining_event = app.config["REMAINING_EVENT"]
    async def event_stream():
        last_data = None

        while True and app.config.get("RATELIMIT"):
            await remaining_event.wait()
            remaining_event.clear()
            data = {
                "remaining": app.config.get("RATELIMIT").get("remaining"),
                "buffer": app.config.get("BUFFER")
            }

            if data != last_data:
                yield f"data: {json.dumps(data)}\n\n"
                last_data = data

            await asyncio.sleep(1)

    return Response(event_stream(), content_type='text/event-stream')

@frontend_bp.route('/infos/running')
async def running_stream():
    app = current_app._get_current_object()
    running_event = app.config["RUNNING_EVENT"]

    async def event_stream():
        last_data = None

        while True and app.config["RUNNING"]:
            await running_event.wait()
            running_event.clear()
            data = {
                "running": app.config["RUNNING"],
            }

            if data != last_data:
                yield f"data: {json.dumps(data)}\n\n"
                last_data = data

            await asyncio.sleep(1)

    return Response(event_stream(), content_type='text/event-stream')


@frontend_bp.route('/infos/nextelements')
async def nextelements_stream():
    app = current_app._get_current_object()
    next_element_event = app.config["NEXT_ELEMENT_EVENT"]

    async def event_stream():
        last_snapshot = None
        while True:
            await next_element_event.wait()
            next_element_event.clear()

            queue = app.config.get("REQUEST_QUEUE")
            if queue:
                items = list(queue._queue)
                if items != last_snapshot:
                    yield f"data: {json.dumps([str(i) for i in items])}\n\n"
                    last_snapshot = items

    return Response(event_stream(), content_type='text/event-stream')