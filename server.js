var express = require('express');
var bodyParser = require("body-parser");
var spawn = require('child_process').spawn;
var path = require("path");
var app = express();


app.use(bodyParser.json());
app.use(bodyParser.urlencoded({ extended: true }));
app.use(bodyParser.text());
app.use(bodyParser.json({ type: "application/vnd.api+json" }));
app.use(express.static(path.join(__dirname, "public")));

app.get("/", function(req, res)
{
	res.sendFile(path.join(__dirname, "public", "index.html"));
})

app.post("/", function(req, res)
{
	var conditions = req.body.conditions
	var otherinfo = req.body.otherData
	var data = []
	data.push(otherinfo)
	data.push(conditions)

	result = predict(data, function(result)
	{
		res.send(result)
	})
})

var predict = function(data, cb)
{
	var py = spawn('python', ['compute_input.py']);

	py.stdin.write(JSON.stringify(data));
	py.stdin.end();

	dataString = '';
	/*Here we are saying that every time our node application receives data from the python process output stream(on 'data'), we want to convert that received data into a string and append it to the overall dataString.*/
	py.stdout.on('data', function(data)
	{
	  dataString += data.toString();
	});

	/*Once the stream is done (on 'end') we want to simply log the received data to the console.*/
	py.stdout.on('end', function()
	{
	  console.log('Repeated Random Balanced Sub-Sampling Prediction: '+dataString);
	  cb(dataString)
	});
}

app.listen(3000)

