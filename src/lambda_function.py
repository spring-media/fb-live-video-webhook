import boto3
import json
import os
import datetime as dt

KEY = "$STATE"
VERIFY_TOKEN = os.environ['VERIFY_TOKEN']
FB_BUCKET = os.environ['BUCKET']
FB_PATH = os.environ['BUCKET_PATH'].replace(KEY, os.environ['STATE'])


def write_json(event, json_key: str, bucket=FB_BUCKET, path=FB_PATH):
    s3 = boto3.resource('s3')
    fb_key = path + "/" + json_key
    print("File-->>{}".format(fb_key))
    data = event
    s3.Object(bucket, fb_key).put(Body=(bytes(data.encode('UTF-8'))))
    print("File-->>{}{}".format(fb_key, " file written"))


def webhook(event, context):
    response = {
        "statusCode": 200,
        "body": "BI-Team Facebook Webhook"
    }
    try:
        run_hour = dt.datetime.now().strftime("%H")
        run_date_ymd = dt.datetime.now().strftime("%Y%m%d")
        print("--> event{}".format(event))

        if event['httpMethod'] == 'GET':
            if event['queryStringParameters']['hub.verify_token'] == VERIFY_TOKEN:
                print("succefully verified")
                response['body'] = event['queryStringParameters']['hub.challenge']
                print("--> response{}".format(response))
                return response
            else:
                print("Wrong verification token!")
                response["statusCode"] = 400
                response["body"] = event
                return response

        elif event['httpMethod'] == 'POST':
            if 'entry' in event['body']:
                body = json.loads(event['body'])
                for b in body['entry']:
                    time_vid = b['time']
                    fb_site = b['id']
                    for l in b['changes']:
                        id = l['value']['id']
                        status = l['value']['status']
                        print("Status: " + str(status), "site: " + str(fb_site), "id:" + str(id))
                        # we only want to write a file to S3 if the video went live
                        if status == 'live':
                            filename = (
                                    "fb_webhook_lv-"
                                    + run_date_ymd
                                    + "-"
                                    + run_hour
                                    + "-"
                                    + fb_site
                                    + "-"
                                    + str(id)
                                    + "-"
                                    + str(time_vid)
                                    + ".json"
                            )
                            print("File-->>{}".format(filename))

                            write_json(event['body'], filename)
                        else:
                            print("Status is not live, but: " + str(status))
                response['body'] = event
            else:
                print("an error occured: event body has no entry. Event body: ")
                print(event['body'])
                response['body'] = event

            return response

        else:
            response["statusCode"] = 400
            response["body"] = event
            print("an error occured with the request!")
            return response

    except Exception as e:
        print("an exception occured! : " + str(e))

    return response
