import json
import logging
import requests

logger = logging.getLogger()
logger.setLevel(logging.INFO)



def handler(event, context):
    logger.info(f"Received event: {event}")
    
    application_id = event['application_id']
    interaction_token = event['interaction_token']
    message = event['messages']
    embed = event['embeds']
    interaction_id = event['id']
    message_id = event['message_id']
    remove_all_buttons = event['remove_all_buttons']
    
    logger.info(f"Embed: {embed}")     
    if embed is not None:
        send_initial_embed(interaction_id, interaction_token, embed)
    
    if message is not None:
        send_initial_message(interaction_id, interaction_token, message)
    
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

    if response.status_code in [200, 204]:
        logger.info(f"Message sent successfully to url: {url}")
    else:
        logger.error(f"Failed ({response.status_code}) to send message: {response.text} to url: {url}")

def send_initial_embed(interaction_id, interaction_token, embed):
    url = f"https://discord.com/api/v10/interactions/{interaction_id}/{interaction_token}/callback"
        
    payload = {
        "type": 4,
        "data": {
            "embeds": [embed]
        }
    }
    
    response = requests.post(url, json=payload)
    logging.info(f"Embed post response: {response}")
    if response.status_code in [200, 204]:
        logger.info(f"Embed sent successfully ({response.status_code}) to url: {url}")
    else:
        logger.error(f"Failed ({response.status_code}) to send embed: {response.text} to url: {url}")

def send_followup_message(application_id, interaction_token, content):
    url = f"https://discord.com/api/v10/webhooks/{application_id}/{interaction_token}"
    
    payload = {
        "content": content
    }
    
    response = requests.post(url, json=payload)
    if response.status_code in [200, 204]:
        logger.info(f"Followup message sent successfully to url: {url}")
    else:
        logger.error(f"Failed ({response.status_code}) to send followup message: {response.text} to url: {url}")

def send_followup_embed(application_id, interaction_token, embed):
    url = f"https://discord.com/api/v10/webhooks/{application_id}/{interaction_token}"
    
    payload = {
        "embeds": embed
    }
    
    response = requests.post(url, json=payload)
    if response.status_code in [200, 204]:
        logger.info(f"Followup embed sent successfully to url: {url}")
    else:
        logger.error(f"Failed ({response.status_code}) to send followup embed: {response.text} to url: {url}")

def remove_buttons(application_id, interaction_token, message_id):
    url = f"https://discord.com/api/v10/webhooks/{application_id}/{interaction_token}/messages/{message_id}"
    
    payload = {
        "components": []  # Empty components array to remove buttons
    }

    response = requests.patch(url, json=payload)
    
    if response.status_code in [200, 204]:
        logger.info(f"Removed buttons successfully ({response.status_code}) to url: {url}")
    else:
        logger.error(f"Failed ({response.status_code}) to send remove buttons: {response.text} to url: {url}")