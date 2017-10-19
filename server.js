var express = require('express')
var bodyParser = require("body-parser");
var spawn = require('child_process').spawn;
var path = require("path");
var py = spawn('python', ['compute_input.py']);
var app = express()

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
	result = predict(function(result)
	{
		res.send(result)
	})
})

var predict = function(cb)
{
	data = []
	data.push(0)
	data.push(23)
	//Ceating fake data entry
	for (var i=0; i<263; i++)
	{
		data.push(0)
	}

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

	/*We have to stringify the data first otherwise our python process wont recognize it*/
	py.stdin.write(JSON.stringify(data));
	py.stdin.end();
}

app.listen(3000)

