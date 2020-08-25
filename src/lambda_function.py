import boto3
import json
import os
import datetime as dt



def write_json(event, json_key: str, bucket, path):
    s3 = boto3.resource('s3')
    fb_key = path + "/" + json_key
    s3.Object(bucket, fb_key).put(Body=json.dumps(event))
    print("File-->>{}{}".format(fb_key, " file written"))


def webhook(event, context):
    KEY = "$STATE"
    VERIFY_TOKEN = os.environ['VERIFY_TOKEN']
    FB_BUCKET = os.environ['BUCKET']
    FB_PATH = os.environ['BUCKET_PATH'].replace(KEY, os.environ['STATE'])

    response = {
        "statusCode": 200,
        "body": "Spring Data BI Facebook Webhook"
    }

    run_hour = dt.datetime.now().strftime("%H")
    run_date_ymd = dt.datetime.now().strftime("%Y%m%d")

    if event['httpMethod'] == 'GET':
        if event['queryStringParameters']['hub.verify_token'] == VERIFY_TOKEN:
            print("succefully verified")
            response['body'] = event['queryStringParameters']['hub.challenge']
            print("--> response{}".format(response))
            return response
        else:
            print("Wrong verification token!")
            response["statusCode"] = 400
            response["body"] = "Wrong validation token"
            return response

    elif event['httpMethod'] == 'POST':
        if 'entry' in event['body']:
            body = event['body']
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

                        write_json(event=event['body'], json_key=filename, bucket=FB_BUCKET, path=FB_PATH)
                    else:
                        print("Status is not live, but: " + str(status))

        else:
            print("an error occured: event body has no entry. Event body: ")
            print(event['body'])
        return response

    else:
        response["statusCode"] = 400
        response["body"] = "No POST or GET detected sorry"
        print("an error occured with the request!")
        return response

    return response
