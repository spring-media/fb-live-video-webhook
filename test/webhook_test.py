import unittest
from src import lambda_function
from moto import mock_apigateway
import os


class WebhookTest(unittest.TestCase):
    # Env variables
    DEST_BUCKET = 'spring-data-bi-dev'
    DEST_PATH = 'facebook/$STATE/video/webhook'
    STATE = 'dev'
    TOKEN = 't0k3N'

    def setUp(self):
        """
        executes before each test run
        :return:
        """
        os.environ['BUCKET'] = self.DEST_BUCKET
        os.environ['BUCKET_PATH'] = self.DEST_PATH
        os.environ['STATE'] = self.STATE
        os.environ['VERIFY_TOKEN'] = self.TOKEN

    def tearDown(self):
        """
        gets executed after each test run
        :return:
        """
        del os.environ['BUCKET']
        del os.environ['BUCKET_PATH']
        del os.environ['STATE']
        del os.environ['VERIFY_TOKEN']

    def test_new_live_video(self):
        event = {
            'httpMethod': 'POST',
            'body': {
                'object': 'page',
                'entry': [
                    {
                        'id': '25604775729',
                        'time': 1597649861,
                        'changes': [
                            {
                                'value': {
                                    'id': '10159868569485730',
                                    'status': 'live'
                                },
                                'field': 'live_videos'
                            }
                        ]
                    }
                ]
            }
        }
        context = None
        response = lambda_function.webhook(event=event, context=context)
        self.assertEqual(response['statusCode'], 200)


if __name__ == '__main__':
    unittest.main()
