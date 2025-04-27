from quart import Blueprint, request, jsonify, current_app, Response
import logging
import asyncio
import json

processing_bp = Blueprint('processing', __name__)

processing_enabled = False  # Global flag to control processing
processing_task = None


@processing_bp.route('/process', methods=['GET', 'POST'])
async def toggle_processing():
    global processing_enabled, processing_task
    if request.method == 'GET':
        return jsonify({"processing_enabled": processing_enabled}), 200
    try:
        data = await request.get_json()
        if 'enabled' not in data:
            return jsonify({"error": "Missing 'enabled' in request body"}), 400
        processing_enabled = bool(data['enabled'])
        current_app.config["RUNNING"] = processing_enabled 
        status = "enabled" if processing_enabled else "disabled"
        if processing_enabled and processing_task is None:
            processing_task = asyncio.create_task(processing_loop())
        return jsonify({"message": f"Processing {status}"}), 200
    except Exception as e:
        logging.error(f"Error in toggle_processing: {e}")
        return jsonify({"error": str(e)}), 500

async def receive_data():
    if not processing_enabled:
        return jsonify({"error": "Processing is currently disabled"}), 403

async def processing_loop():
    next_element_event = current_app.config["NEXT_ELEMENT_EVENT"]
    while processing_enabled:
        try:
            queue = current_app.config["REQUEST_QUEUE"]
            current_size = queue.qsize()
            if current_size < 3:
                for _ in range(3 - current_size):
                    queue_entry = await current_app.config["BACKEND"].getNextElement()
                    if queue_entry == None:
                        github_api = current_app.config["GITHUB_API"]
                        repo = github_api.getFallback()
                        if repo:
                            queue_entry = {"title": repo.name, "foreign_id": repo.id}
                        else:
                            logging.error("All repositories grabbed. Need a new fallback")
                    if queue_entry:
                        logging.info("Adding element to processing queue...")
                        await queue.put(queue_entry)
                        next_element_event.set()  # Trigger update for nextelements stream
            await asyncio.sleep(2)  # Kontrollintervall
        except Exception as e:
            logging.error(f"Error in processing_loop: {e}")
            await asyncio.sleep(5)
