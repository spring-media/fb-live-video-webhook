import boto3
import json
import os
from base64 import b64decode
import datetime as dt
import uuid

# from utils.facebookhandler import FacebookHandler
KEY = "$STATE"
VERIFY_TOKEN = os.environ['VERIFY_TOKEN']
FB_BUCKET = os.environ['BUCKET']
FB_PATH = os.environ['BUCKET_PATH'].replace(KEY, os.environ['STATE'])
FB_SITE = "25604775729"


def write_json(event, json_key: str, bucket=FB_BUCKET, path=FB_PATH):
    s3 = boto3.resource('s3')
    fb_key = path + "/" + json_key
    data = event  # json.loads(json.dumps(event))
    s3.Object(bucket, fb_key).put(Body=(bytes(data.encode('UTF-8'))))

    response = {
        "statusCode": 200,
        "body": "",
    }


def webhook(event, context):
    try:
        # print(event)
        # for ev in event:
        #    print (ev)
        # uuid_4 = str(uuid.uuid4())
        run_hour = dt.datetime.now().strftime("%H")
        run_date_min = dt.datetime.now().strftime("%M")
        run_date_ymd = dt.datetime.now().strftime("%Y%m%d")

        if event['httpMethod'] == 'GET':
            if event['queryStringParameters']['hub.verify_token'] == VERIFY_TOKEN:
                print("succefully verified")
                response['body'] = event['queryStringParameters']['hub.challenge']
                print("--> response{}".format(response))
                return response
            else:
                print("Wrong verification token!")
                response = {
                    "statusCode": 400,
                    "body": "Wrong validation token"
                }
                return response
        elif event['httpMethod'] == 'POST':
            if 'entry' in event['body']:
                body = json.loads(event['body'])
                for b in body['entry']:
                    time_vid = b['time']
                    for l in b['changes']:
                        id = l['value']['id']
                        filename = (
                                "fb-webhook-lv-"
                                + run_date_ymd
                                + "-"
                                + run_hour
                                + "-"
                                + FB_SITE
                                + "-"
                                + str(id)
                                + "-"
                                + str(time_vid)
                                + ".json"
                        )
                        print("File-->>{}".format(filename))

                        write_json(event['body'], filename)

            else:
                print(event['body'])
                # write_json(event, filename)
            return response
        else:
            response = {
                "statusCode": 400,
                "body": "No POST or GET detected sorry"
            }
            return response

    except Exception as e:
        response = {
            "statusCode": 200,
            "body": "Ok."
        }
    return response