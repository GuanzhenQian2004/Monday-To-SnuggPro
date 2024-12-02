import logging
from flask import Flask, request, jsonify
from . import config
from .mondayItem import MondayItem
from .snuggproJob import SnuggProJob

# Initialize the Flask app
app = Flask(__name__)

@app.route('/')
def homepage():
    return """
    <html>
        <head>
            <title>My Webhook App</title>
        </head>
        <body>
            <h1>Welcome to My Webhook App</h1>
            <p>Check out the source code for this project on GitHub:</p>
            <a href="https://github.com/GuanzhenQian2004/Monday-To-SnuggPro" target="_blank">GitHub Repository</a>
        </body>
    </html>
    """

# Webhook Page Route
@app.route('/webhook', methods=['POST'])
def handle_webhook():
    
    # Fetch data
    data = request.get_json()
    logging.debug("Received Data From Webhook: %s", data)

    # Initial webhook verification setup
    if 'challenge' in data:
        challenge = data['challenge']
        logging.info("Connected with a new Monday.com webhook endpoint")
        return jsonify({'challenge': challenge}), 200

    # Parse event type and origin board id
    try:
        event_type = data.get('event').get('type', '')
        board_id = data.get('event').get('boardId', '')
        logging.debug("Recieved Event from Monday.com, Event Type: %s, Board ID: %s", event_type, board_id)
    except Exception as e:
        logging.error("An error occurred while extracting event_type or board_id: %s", e)
        return jsonify({"status": "Error occurred while processing the webhook"}), 500

    # Handling event
    if event_type == 'update_column_value' and board_id == config.BOARD_ID: # Note: Verification can be removed, it's kept just to prevent unexpected situations
        
        # Parse item name and item id
        try:
            item_name = data.get('event').get('pulseName', 'Unknown Item')
            item_id = data.get('event').get('pulseId')
            logging.info("Monday.com Item Changed: %s (ID: %s)", item_name, item_id)
        except Exception as e:
            logging.error("An error occurred while extracting item_name or item_id: %s", e)
            return jsonify({"status": "Error occurred while processing item data"}), 500
        
        # Parse Data from item
        changed_item = MondayItem(config.MONDAY_API_TOKEN, item_id, item_name, pulseID=True)
        snuggpro_job_data = changed_item.get_snuggpro_job_creation_data()
        logging.info("Parsed Data from changed Item: %s", snuggpro_job_data)

        # Create new Snuggpro Job
        new_job = SnuggProJob(
            snuggpro_job_data['firstName'],
            snuggpro_job_data['lastName'],
            snuggpro_job_data['email'],
            snuggpro_job_data['homePhone'],
            snuggpro_job_data['address1'],
            snuggpro_job_data['city'],
            snuggpro_job_data['state'],
            snuggpro_job_data['zip']
        )
        try:
            new_job.create_job()
            logging.info("Snuggpro Job created successfully.")
        except Exception as e:
            logging.error("An error occurred while creating Snuggpro job: %s", e)
            return jsonify({"status": "Error occurred while creating the job"}), 500

    else:
        logging.warning("%s was not handled", event_type)

    # Respond to acknowledge
    return jsonify({"status": "Webhook received"}), 200

# Run the Flask apps
if __name__ == '__main__':
    # Configure logging
    logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s')

    # Run Application
    app.run(host='0.0.0.0', port=8080, debug=True)

