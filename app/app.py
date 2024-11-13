from flask import Flask, request, jsonify
import config
from mondayItem import MondayItem
from snuggproJob import SnuggProJob

# Initialize the Flask app
app = Flask(__name__)

# Define the route to handle incoming webhooks from Monday.com
@app.route('/webhook', methods=['POST'])
def handle_webhook():
    
    data = request.get_json()
    # Debug: Print received data from webhook
    print("\nRecieved Data From Webhook:\n", data, "\n")

    # Initial webhook verification setup
    if 'challenge' in data:
        challenge = data['challenge']
        return jsonify({'challenge': challenge}), 200


    event_type = data.get('event', {}).get('type', '')
    board_id = data.get('event', {}).get('boardId', '')

    print(data)

    # Need to change
    if event_type == 'update_column_value' and board_id == config.BOARD_ID:
        item_name = data.get('event', {}).get('pulseName', 'Unknown Item')
        item_id = data.get('event', {}).get('pulseId')
        print(f"///// Item Changed Status: {item_name} (ID: {item_id}) /////")
        
        changed_item = MondayItem(config.MONDAY_API_TOKEN, item_id, item_name, pulseID=True)
        snuggpro_job_data = changed_item.get_snuggpro_job_creation_data()
        print("\nParsed Data:\n", snuggpro_job_data, "\n")

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

        new_job.create_job()

    # Respond to acknowledge
    return jsonify({"status": "Webhook received"}), 200

# Run the Flask app on a specified port
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)

