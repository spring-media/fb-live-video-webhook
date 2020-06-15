import json


def api_gateway_event(payload: dict) -> dict:
    return {
        'resource': '',
        'path': '',
        'method': '',
        'headers': {},
        'requestContext': {
            'resourcePath': '',
            'httpMethod': ''
        },
        'body': json.dumps(payload)
    }
