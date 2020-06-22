import boto3
import json
import os
from base64 import b64decode
import datetime as dt
import uuid

# from utils.facebookhandler import FacebookHandler 
VERIFY_TOKEN = os.environ['VERIFY_TOKEN']
FB_BUCKET = os.environ['BUCKET'] 
FB_PATH = os.environ['BUCKET_PATH'] 


def write_json(event,json_key: str,bucket=FB_BUCKET,path=FB_PATH):
    s3 = boto3.resource('s3')
    fb_key= path + "/" + json_key
    data = json.loads(json.dumps(event['headers']))    
    s3.Object(bucket, fb_key).put(Body=(bytes(json.dumps(data).encode('UTF-8'))))

def respond(err, res=None):
    return {
        'statusCode': '400' if err else '200',
        'body': err.message if err else json.dumps(res),
        'headers': {
            'Content-Type': 'application/json',
        },
    }


def webhook(event, context):

    try:
        print("--> entry{}".format(event))
        uuid_4 = str(uuid.uuid4())
        run_hour = dt.datetime.now().strftime("%H")
        run_date_min = dt.datetime.now().strftime("%M")
        run_date_ymd = dt.datetime.now().strftime("%Y%m%d")
    
        filename = (
                    "fb-webhook-video-live-"
                    + run_date_ymd
                    + "-"
                    + run_hour
                    + "-"
                    + run_date_min
                    + "-"
                    + uuid_4
                    + ".hook"
                    #+ str(object_id)
                    )
                
        response = {
            "statusCode": 200,
            "body":"",
        }
        
        operation = event['httpMethod']
        print("operation:{}".format(operation)) 
        if operation== 'GET':
            if 'hub.verify_token' in event['query'] and  event['query']['hub.verify_token'] == VERIFY_TOKEN:     
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
        # hier kommt die Verarbeitung hin.
        # body in file auf s3 schreiben.
        elif  operation == 'POST':
            if 'entry' in event['body']:
                write_json(event,filename)  
                # FacebookHandler.entries(event['body']['entry'])
            else:
                print("--> no entry")
                #for r in event:
                #    print(r)
                #print(event['body'])
                # hier testwweise headers wegschreiben
                write_json(event,filename)                
            return response
        else:
            response = {
                    "statusCode": 400,
                    "body":  "No POST or GET detected sorry"
            }
            return response
    except Exception as e:
        print(e)
        return e