'''
Your endpoint must be able to process two types of HTTPS requests:
Verification Requests and Event Notifications.
Since both requests use HTTPs, your server must have a valid TLS or SSL certificate correctly configured and installed. Self-signed certificates are not supported.
'''

import json
import logging
import boto3
from utils.facebookhandler import FacebookHandler

VERIFY_TOKEN = os.environ['VERIFY_TOKEN'] #reemplace
response = {
    "statusCode": 200,
    "body": "",
}

def webhook(event, context):

    try:
        if event['method'] == 'GET':
            handle_verif_req(event)
        elif  event['method'] == 'POST':
            handle_ev_notifs(event)
        else:
            response = {
                    "statusCode": 400,
                    "body":  "No POST or GET detected sorry"
            }
            return response
    except Exception as e:
        print(e)
        return e

def handle_verif_req(event):
    """
    :param event: the payload of the verification GET request
    :return: hub.challenge
    """

    if 'hub.verify_token' in event['query'] and  event['query']['hub.verify_token'] == VERIFY_TOKEN:
        logging.info("succefully verified")
        response['body'] = event['query']['hub.challenge']
        return  response
    else:
        print("Wrong verification token!")
        response = {
            "statusCode": 400,
            "body":  "Wrong validation token"
        }
        return response

def handle_ev_notifs(request):
    """
    handle the POST request sent by Facebook regarding the change of a live video on a subscribed page
    store the data received by Facebook on AWS S3
    :return: HTTP status code 200 OK HTTPS
    """
    if 'entry' in event['body']:
        FacebookHandler.entries(event['body']['entry'])
    else:
        print(event['body'])  # Something we dont handle yet and we want to take a look ...
    return response

def hello(event, context):
    body = {
        "message": "Go Serverless v1.0! Your function executed successfully!",
        "input": event
    }

    response = {
        "statusCode": 200,
        "body": json.dumps(body)
    }

    return response

    # Use this code if you don't use the http event with the LAMBDA-PROXY
    # integration
    """
    return {
        "message": "Go Serverless v1.0! Your function executed successfully!",
        "event": event
    }
    """
