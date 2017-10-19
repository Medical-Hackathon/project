$("#submit").on("click", function(event)
{
	var data = 
	{
		clicked: true
	}

	$.ajax(
	{
		url: "/",
		type: "post",
		data: data
	}).done(function(result)
	{
		result = result.trim()
		var prediction = result.substr(1);
		prediction = prediction.slice(0, prediction.length-1);
		prediction = prediction.split(",");
		var result = prediction.map(function (x) 
		{ 
		    return parseFloat(x, 10); 
		});
		console.log(result[1])
		$('#complication_stat').html(result[0])
	})
})