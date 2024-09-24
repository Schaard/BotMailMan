import json
import logging
import requests

logger = logging.getLogger()
logger.setLevel(logging.INFO)

def handler(event, context):
    logger.info(f"Received event: {event}")
    
    application_id = event['application_id']
    interaction_token = event['interaction_token']
    follow_up_messages = event['follow_up_messages']
    
    for message in follow_up_messages:
        send_followup_message(application_id, interaction_token, message)
    
    return {
        "statusCode": 200,
        "body": json.dumps("Follow-up messages sent successfully")
    }

def send_followup_message(application_id, interaction_token, content):
    url = f"https://discord.com/api/v10/webhooks/{application_id}/{interaction_token}"
    
    payload = {
        "content": content
    }
    
    response = requests.post(url, json=payload)
    if response.status_code != 200:
        logger.error(f"Failed to send follow-up message: {response.text}")
    else:
        logger.info("Follow-up message sent successfully")