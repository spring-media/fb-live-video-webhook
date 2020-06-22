# fb-live-video-webhook
- **current stage**: TEST
- written in Node.js v12.x
## AWS
- uses the technical user `spring-data-bi`
- `index.js` specifies the webhook logic
### Lambda
- Webhook is deployed as a *AWS Lambda function* 
### API Gateway
- used to invoke the Lambda function
- [endpoint](https://1b50va2t51.execute-api.eu-central-1.amazonaws.com/test)
### S3
- files containing live data of videos are written to `spring-data-bi-test/facebook/test/video/live`
## Serverless framework
- [Serverless Documentation](https://www.serverless.com/framework/docs)
- Version: v1.72.0
## Deployment
### clone the repository
`git clone`
### install the apps and its modules
`npm install`
### add your credentials in `serverless.yml`
`TOKEN` can be found in the password tool `30 Evolution Welt/ Facebook PAGES`
### deploy using the *Serverless* framework
`serverless deploy`
#### deploy only updates to the function (faster)
`serverles deploy function --function app`
