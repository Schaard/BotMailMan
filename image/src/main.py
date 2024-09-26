import json
import logging
import requests

logger = logging.getLogger()
logger.setLevel(logging.INFO)

def handler(event, context):
    logger.info(f"Received event: {event}")
    
    application_id = event['application_id']
    interaction_token = event['interaction_token']
    messages = event['messages']
    interaction_id = event['id']
    message_id = event['message_id']
    remove_all_buttons = event['remove_all_buttons']

    for message in messages:
        send_initial_message(interaction_id, interaction_token, message)
        #send_followup_message(application_id, interaction_token, message)
        
    if remove_all_buttons:
        remove_buttons(application_id, interaction_token, message_id)

    return {
        "statusCode": 200,
        "body": json.dumps("Mailman activity complete")
    }

def send_initial_message(interaction_id, interaction_token, content):
    url = f"https://discord.com/api/v10/interactions/{interaction_id}/{interaction_token}/callback"
        
    payload = {
        "type": 4,
        "data": {
            "content": content
        }
    }
    
    response = requests.post(url, json=payload)

    if response.status_code != 200:
        logger.error(f"Failed ({response}) to send message: {response.text} to url: {url}")
    else:
        logger.info("Message sent successfully")

def send_followup_message(application_id, interaction_token, content):
    url = f"https://discord.com/api/v10/webhooks/{application_id}/{interaction_token}"
    
    payload = {
        "content": content
    }
    
    response = requests.post(url, json=payload)
    if response.status_code != 200:
        logger.error(f"Failed (response: {response.text}) to send follow-up message {payload} to {url}")
    else:
        logger.info("Follow-up message sent successfully")

        # Function to remove the button from the original message by editing it
def remove_buttons(application_id, interaction_token, message_id):
    url = f"https://discord.com/api/v10/webhooks/{application_id}/{interaction_token}/messages/{message_id}"
    
    # Payload to remove components (i.e., buttons)
    payload = {
        "components": []  # Empty components array to remove buttons
    }

    response = requests.patch(url, json=payload)
    
    if response.status_code != 200:
        logger.error(f"Failed to remove button: {response.text}")
    else:
        logger.info("Button removed successfully")