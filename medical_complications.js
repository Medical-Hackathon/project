var fs = require('fs');

var getData = function(cb)
{
	fs.readFile("./data/complications_list.csv", function(err, data)
	{
		if(err){throw err};

		cb(data.toString())
	});
};

module.exports = getData;
