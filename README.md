# fb-live-video-webhook
## Facebook
[Facebook Documentation](https://developers.facebook.com/docs/graph-api/webhooks/getting-started/webhooks-for-pages/)
## Python 

## AWS
- uses the technical user `spring-data-bi`
- `handler.py` specifies the webhook logic
-  will be deployed as an *AWS Lambda function* 
## Serverless framework
- [Serverless Documentation](https://www.serverless.com/framework/docs)
- Version: v1.72.0
## Initialization
### Dependencies
`pip install -r requirements.txt`
### Credentials
for the `VERIFY_TOKEN`, check the password tool (Evolution Welt/Facebook PAGES)

`touch .env`

`vim .env`

```
ACCESS_KEY_ID=YOUR_KEY_ID
SECRET_ACCESS_KEY=YOUR_ACCESS_KEY
VERIFY_TOKEN=YOUR_TOKEN
```
## Deployment
### clone the repository
`git clone`
### run all tests using pyenv
`cd test`
`pytest -v -s handlerTest.py`
### deploy using the 'Serverless' framework
`serverless deploy -- stage {dev/test/prod} --region eu-central-1`
