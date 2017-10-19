var express = require('express')
var spawn = require('child_process').spawn;
var py = spawn('python', ['compute_input.py']);
var app = express()

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
});

/*We have to stringify the data first otherwise our python process wont recognize it*/
py.stdin.write(JSON.stringify(data));
py.stdin.end();

app.listen(3000)

