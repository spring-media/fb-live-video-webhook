# fb-live-video-webhook
- **current stage**: PROD
- written in Python 3.7
## FB
- `API_VERSION`: `9.0`
- Account details to be found in the password tool `30 Evolution Welt/ Facebook User`
- uses the App `NMT BI`
- needs to be subscribed to the `Page` Webhook in Facebook for Developers
- App needs to be set to `Live`
## AWS
- uses the technical user `spring-data-bi`
- `lambda_function.py` specifies the webhook logic
### Lambda
- Webhook is deployed as a *AWS Lambda function* 
### API Gateway
- Gets called by Facebook using HTTP `GET` or `POST` request
- used to invoke the Lambda function
- [endpoint test](https://9u3wjmdx1g.execute-api.eu-central-1.amazonaws.com/test/webhook)
### S3
- files contain the live status of videos, the time of the event and the ID of the page
 - files are written to `spring-data-bi/facebook/{env}/video/webhook`
## Serverless framework
- Lambda function is deployed using the serverless framework
- [Serverless Documentation](https://www.serverless.com/framework/docs)
- Version: v1.72.0
## Tests
* Unit Tests should be written for each new functionality
* Tests are executed as part of the deployment
* run tests before deployment: `python -m unittest`
## Deployment
### clone the repository
`git clone`
### add your credentials in `serverless.yml`
* `TOKEN`: can be found in the password tool `30 Evolution Welt/ Facebook PAGES`
* `STAGE`: the state of the service
### deploy using the *Serverless* framework
`serverless deploy`
#### deploy only updates to the function (faster)
`serverless deploy function --function src.lambda_function`
