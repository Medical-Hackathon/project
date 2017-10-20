var currentConditions = []

for (var key in getData)
{
	$('#list-of-conditions').append('<tr><td class="condition condition-'+key+'">'+getData[key]+'</td></tr>')
}

$('#example').DataTable();

$(document).on('click', '.condition', function(event)
{
	var id = $(this).attr("class").slice(20);
	id = id.substring(0, id.length-10)
	seen = false;

	for (var i=0; i<currentConditions.length; i++)
	{
		if (id === currentConditions[i])
		{
			seen = true;
			break;
		}
	}

	if (seen)
	{
		alert("You have already selected this condition.");
	}

	else
	{
		currentConditions.push(id)
		console.log(currentConditions)
		$('#patient-conditions').append('<li class="list-group-item d-flex justify-content-between align-items-center">'+getData[id]+'<span><button type="button" class="btn btn-danger delete" id="'+id+'">Delete</button></span></li>')
	}
})

$(document).on("click", ".delete", function(event)
{
	var id = $(this).attr("id");
	console.log(id)

	for (var i=0; i<currentConditions.length; i++)
	{
		if (id === currentConditions[i])
		{
			console.log("EQUAL! "+id+" and "+currentConditions[i])
			currentConditions.splice(i, 1);
			break;
		}
	}

	console.log(currentConditions)

	$('.conition-'+id).parent().remove();


})


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