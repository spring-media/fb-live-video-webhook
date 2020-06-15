from src.handler import *
from test import *


def test_wrong_request():
    """
    test where we pass a mocked api gateway event and None as context
    :return:
    """
    resp = webhook(api_gateway_event({}), None)
    assert resp == {"statusCode": 400, "body": "No POST or GET detected."}


def test_get_request():
    """
    Whenever your endpoint receives a verification request, it must:
    Respond with the hub.challenge value from the GET request including query string parameters, appended to the end of the URL
    :return:
    """
    get_request = {'method': 'GET', 'query': 'https://fb-live-video-webhook.com/webhooks?hub.mode=subscribe&hub.challenge=1158201444&hub.verify_token=>b1LdD1rD31Nw3bH00k§'}
    resp = webhook(get_request, None)
    hub_challenge = '1158201444'
    assert resp == {
        "statusCode": 200,
        "body": hub_challenge,
    }


def test_post_request():
    post_request = {'method': 'POST', 'body': {
        "object": "page",
        "entry": [
            {
                "id": "25604775729",
                "time": 1592224440,
                "changes": [
                    {
                        "value": {
                            "id": "10159659015335730",
                            "status": "vod"
                        },
                        "field": "live_videos"
                    }
                ]
            }
        ]
    }
                    }
    resp = webhook(post_request, None)
    assert resp == {"statusCode": 200, "body": "success", }


if __name__ == '__main__':
    test_get_request()
