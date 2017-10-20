var fs = require('fs');

var getData = function(cb)
{
	fs.readFile("./data/test.csv", function(err, data)
	{
		if(err){throw err};

		cb(data.toString())
	});
};

module.exports = getData;
