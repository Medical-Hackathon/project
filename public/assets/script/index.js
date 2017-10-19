

$("#submit").on("click", function(event)
{

	$('.animationload').show()

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
		prediction = prediction.map(function (x) 
		{ 
		    return parseFloat(x, 10); 
		});

		$('.animationload').hide()

		if (prediction[0] === 0)
		{
			$('.alert').attr("class", "alert alert-success")
			$('#complication_stat').html("No Complication Predicted <br>")
			$('#confidence').html("Confidence: "+prediction[1]+"%")
		}

		else
		{
			$('.alert').attr("class", "alert alert-danger")
			$('#complication_stat').html("Complication Predicted <br>")
			$('#confidence').html("Confidence: "+prediction[2]+"%")			
		}
	})
})