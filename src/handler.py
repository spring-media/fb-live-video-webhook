'''
Your endpoint must be able to process two types of HTTPS requests:
Verification Requests and Event Notifications.
Since both requests use HTTPs, your server must have a valid TLS or SSL certificate correctly configured and installed. Self-signed certificates are not supported.
'''

import sys
import json
import logging
import boto3
import os
from dotenv import load_dotenv
from pathlib import Path

env_path = Path('..') / '.env'
load_dotenv(dotenv_path=env_path)
VERIFY_TOKEN = os.getenv('VERIFY_TOKEN')


def webhook(event, context):
    """
    The main handler for the FB webhook
    :param event: passed from Lambda function
    :param context: passed from Lambda function
    :return: reponse
    """
    try:
        response = {
            "statusCode": 200,
            "body": "success",
        }
        if event['method'] == 'GET':
            return handle_verif_req(event, response)
        elif  event['method'] == 'POST':
            return handle_ev_notifs(event, response)
        else:
            response = {
                    "statusCode": 400,
                    "body":  "No POST or GET detected."
            }
            return response
    except Exception as e:
        #logging.error("'method' was not provided, the application ends.")
        print(e)
        #logging.error(e)
        return e

def handle_verif_req(event, response):
    """
    :param event: the payload of the verification GET request
    :return: hub.challenge
    """

    if 'hub.verify_token' in event['query'] and  event['query']['hub.verify_token'] == VERIFY_TOKEN:
        #logging.info("succefully verified")
        print("succefully verified")
        response['body'] = event['query']['hub.challenge']
        return response
    else:
        print("Wrong verification token!")
        response = {
            "statusCode": 400,
            "body":  "Wrong validation token"
        }
        return response

def handle_ev_notifs(event, response):
    """
    - handle the POST request sent by Facebook regarding the change of a live video on a subscribed page
    - store the data received by Facebook on AWS S3
    :param event: the event from AWS Lambda function
    :param response: the http response
    :return: response
    """
    if 'entry' in event['body']:
        #logging.info(event['body']['entry'])
        print(event['body']['entry'])
    else:
        #logging.info(event['body'])  # Something we dont handle yet and we want to take a look ...
        print(event['body'])
    return response
