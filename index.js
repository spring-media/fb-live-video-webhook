const serverless = require('serverless-http');
const express = require('express')
const bodyParser = require('body-parser')
const xhub = require('express-x-hub')
const aws = require('aws-sdk')

// Set the Region 
aws.config.update({ region: 'eu-central-1' });
const s3 = new aws.S3({
    accessKeyId: process.env.ACCESS_KEY_ID,
    secretAccessKey: process.env.SECRET_ACCESS_KEY
});
const app = express()

app.use(xhub({ algorithm: "sha1", secret: process.env.APP_SECRET }));
app.use(bodyParser.json());

var token = process.env.TOKEN || "token";
var received_updates = [];

app.get("/", function (req, res) {
    console.log(req);
    res.send("<pre>" + JSON.stringify(received_updates, null, 2) + "</pre>");
});

app.get(["/facebook", "/instagram"], function (req, res) {

    if (
        req.query["hub.mode"] == "subscribe" &&
        req.query["hub.verify_token"] == token
    ) {
        res.send(req.query["hub.challenge"]);
        console.log(req);
    } else {
        res.sendStatus(400);
    }
});

app.post("/facebook", function (req, res) {

    if (!req.isXHubValid()) {
        console.log(
            "Warning - request header X-Hub-Signature not present or invalid"
        );
        res.sendStatus(401);
        return;
    }

    console.log("request header X-Hub-Signature validated");
    // Process the Facebook updates here
    received_updates.unshift(req.body);

    var data = {
        "video_id": req.body.entry[0].changes[0].value.id,
        "event_time": req.body.entry[0].time,
        "status": req.body.entry[0].changes[0].value.status,
    };

    var filename = process.env.PATH_TEST + '/' + data["video_id"] + '_' + data["event_time"] + '.json'

    try {
        var base64data = new Buffer(JSON.stringify(data), 'binary');
        s3.putObject({
            Bucket: process.env.BUCKET_TEST,
            Key: filename,
            Body: base64data,
        }, function (resp) {
            received_updates.push("Data was saved to S3!")
        });
    } catch (e) {
        received_updates.push("Error while saving to S3: " + e)
    }


    res.sendStatus(200);
});



module.exports.handler = serverless(app);