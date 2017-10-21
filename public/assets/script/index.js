var currentConditions = [0]

for (var key in diagnosis)
{
	$('#list-of-diagnosis').append('<tr><td class="diagnosis diagnosis-'+key+'">'+diagnosis[key]+'</td></tr>')
}

for (var key in PMH)
{
	$('#list-of-PMH').append('<tr><td class="PMH PMH-'+key+'">'+PMH[key]+'</td></tr>')
}

$('#diagnosis-table').DataTable(
	{
		"scrollY":        "300px",
        "scrollCollapse": true,
	});

$('#PMH-table').DataTable(
	{
		"scrollY":        "300px",
        "scrollCollapse": true,
	});

$(document).on("click", ".card-header", function(event)
{
	if (!$(this).hasClass("opened"))
	{
		$('.card-body').slideUp();
		$('#'+$(this).attr("class")[$(this).attr("class").length-1]).slideDown();
		$('.card-header').removeClass("opened");	
		$(this).addClass("opened");	
	}

	else
	{
		$(this).removeClass("opened");
		$('#'+$(this).attr("class")[$(this).attr("class").length-1]).slideUp();
	}
})

$(document).on('click', '.diagnosis', function(event)
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
		$('#diagnosis').append('<div class="hi" style="font-size:20px;">'+diagnosis[id]+'<span><button type="button" class="btn btn-danger delete pull-right" id="'+id+'">Delete</button></span></div>')
	}
})

$(document).on('click', '.PMH', function(event)
{
	var id = $(this).attr("class").slice(8);
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
		$('#PMH').append('<div class="hi" style="font-size:20px;">'+PMH[id]+'<span><button type="button" class="btn btn-danger delete pull-right" id="'+id+'">Delete</button></span></div>')
	}
})

$(document).on("click", ".delete", function(event)
{
	var id = $(this).attr("id");
	console.log($(this).parent().parent().remove())

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
})


$("#submit").on("click", function(event)
{

	var age = $('#age').val().trim();
	var sex = $('#sex').val();
	var race = $('#race').val();
	var edAd = $('#ed-ad').val();
	var bedSize = $('#bedsize').val();
	var location = $('#location').val();
	var volume = $('#volume').val();


	var otherinfo = []
	otherinfo.push(age)
	otherinfo.push(sex)
	otherinfo.push(race)
	otherinfo.push(edAd)
	otherinfo.push(bedSize)
	otherinfo.push(location)
	otherinfo.push(volume)

	console.log(otherinfo)

	$('.animationload').show()

	var predictData = 
	{
		conditions: currentConditions,
		otherData: otherinfo
	};

	$.ajax(
	{
		url: "/",
		type: "post",
		data: predictData
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