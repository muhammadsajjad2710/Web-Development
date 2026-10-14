// Previously executed datasets (i.e. radiological images) are written into a table paired with their dates, to be inserted into a div container.


var executedmodels = new Array(10);
var executiontime = new Array(10);

function getrevenue(memberid, apikey) {



    var apiurl = 'https://api.chief.ai/api/v1.0/suppliers/commission';

    var form_data = new FormData();
    form_data.append("member_id", memberid);


    /* TEST CODE: Variable & data type check: */
    console.log("api key: " + apikey + " " + memberid);



    $.ajax({
        type: 'POST',
        url: apiurl,
        beforeSend: function(request) {
            request.setRequestHeader("x-api-key", apikey);
        },
        contentType: false,
        processData: false,
        timeout: 600000,
        data: form_data,
        success: function(response) {


            $(".revenue").html("Revenue " + data.Current_Balance_Commission);

        }
    });



}

function writeDatasets() {
    datasets_history = "<table>";
    $.post('http://172.83.9.18:5001/api/v1.0/datasets/retrieve', {
            customer_id: 46
        },
        function(data) {
            $.each(data.allDatasets, function(key, value) {
                var filename = value.datasetsfilepath;
                var date = value.created_on;

                filename = filename.split('/data/')[1];
                date = date.split('.')[0];
                time = date.split('T')[1];
                date = date.split('T')[0];
                datasets_history = datasets_history + "<tr><td style=\"width:100px;\">" + filename + "</td><td style=\"width:25px;\">-</td><td>" + time + ",  " + date + "</td></tr>";
            });
            datasets_history = datasets_history + "</table>";
            $(".datasets").html("Your Last Model Executions:<br /><br />" + datasets_history);
        });
}

// This function writes out all models into a html formatted string, alongside their price and a selection button to be inserted into a div container.
function writeAllModels() {

    models_table = "<table style=\"width:100%;\">";
    $.get('https://api.chief.ai/api/v1.0/ms', {},
        function(data) {
            $.each(data.allModels, function(key, value) {
                let res = value.modelname.replaceAll("_", "-");
                res = res.replaceAll(" ", "-");


                models_table = models_table + // This html string is very large and has been string written across many lines for readability. Each record is formatted into a row and each element is enclosed in <td> tags.
                    "<div class = \"row\">" +
                    "<div class = \"col-8\">" + // Infomation tooltip and model name are inserted into this <td>. NOTE: separated only by a space.
                    "<i class=\"fa fa-info-circle\" data-toggle=\"tooltip\" style = \"color:green;\"; title=\"PUT THE TOOLTIP INFORMATION HERE!!\"></i>" +
                    "<span style = \"cursor:pointer;\"  class = \"modelid " + value.model_id + " " + value.tag + "\">" + value.modelname + "</span>" +
                    "</div>" +
                    "<div class = \"col-4\">" + // Price is inserted here
                    "<span class = \"modelprice " + value.model_id + "\">Credits: " + value.price + " </span>" +
                    "</div>" +

                    "</div> <div class = \"row\"><div class = \"col-4\"><span class = \"modelprice " + value.model_id + "\"><a href =\"https://chief.ai/model/" + res + "\" class=\"btn btn-primary btn-circle btn-sm\">Details</a></span></div><div class = \"col-8\"><span style=\"border-bottom: 1px solid #ddd; font-size:10px;\" class = \"modeltag " + value.tag + "\">" + value.tag + "</span></div> </div> <hr>"
            });
            models_table = models_table + "</table>";
            $(".allmodels").html("Available Models: " + models_table);
        });
}


function writemodels(apikey) {

    apiurl = "https://api.chief.ai/api/v1.0/ms";
    console.log(apikey);
    models_table = "<table style=\"width:100%;\">";

    console.log("ojong");



    /* TEST CODE: Variable & data type check: */
    console.log("api key: " + apikey);



    //alert("url is "+apiurl);          
    $.ajax({
        type: 'GET',
        url: apiurl,
        beforeSend: function(request) {
            request.setRequestHeader("x-api-key", apikey);
        },
        contentType: false,
        processData: false,
        timeout: 600000,
        success: function(response) {

            //start function iterate

            $.each(response.allModels, function(key, value) {
                let res = value.modelname.replaceAll("_", "-");
                res = res.replaceAll(" ", "-");

                console.log("ojong");

                models_table = models_table + // This html string is very large and has been string written across many lines for readability. Each record is formatted into a row and each element is enclosed in <td> tags.
                    "<div class = \"row\">" +
                    "<div class = \"col-8\">" + // Infomation tooltip and model name are inserted into this <td>. NOTE: separated only by a space.
                    "<i class=\"fa fa-info-circle\" data-toggle=\"tooltip\" style = \"color:green;\"; title=\"PUT THE TOOLTIP INFORMATION HERE!!\"></i>" +
                    "<span style = \"cursor:pointer;\"  class = \"modelid " + value.model_id + " " + value.tag + "\">" + value.modelname + "</span>" +
                    "</div>" +
                    "<div class = \"col-4\">" + // Price is inserted here
                    "<span class = \"modelprice " + value.model_id + "\">Credits: " + value.price + " </span>" +
                    "</div>" +

                    "</div> <div class = \"row\"><div class = \"col-4\"><span class = \"modelprice " + value.model_id + "\"><a href =\"https://chief.ai/model/" + res + "\" class=\"btn btn-primary btn-circle btn-sm\">Details</a></span></div><div class = \"col-8\"><span style=\"border-bottom: 1px solid #ddd; font-size:10px;\" class = \"modeltag " + value.tag + "\">" + value.tag + "</span></div> </div> <hr>"
            });


            //end function iterate
            console.log("ojong");
            console.log(models_table);

            models_table = models_table + "</table>";
            $(".allmodels").html("Available Models: " + models_table);

        }
    });

}



// This function writes out all models into a html formatted string, alongside their price and a selection button to be inserted into a div container.
function writeModelPreviews() {
    searchParam = $('#pageterm').text();
    models_table = "";
    $.post('https://chief.ai/dashboard/searchmodelspecific.php', {
            model: searchParam
        },
        function(data) {
            $.each(data.models, function(key, value) {


                if (value.score) {
                    score = value.score;
                } else {
                    score = 1;
                }

                models_table = models_table + // This html string is very large and has been string written across many lines for readability. Each record is formatted into a row and each element is enclosed in <td> tags.
                    "<div class=\"row model-preview-row\">" +
                    "<div class=\"card model-preview-card\">" +
                    "<div class=\"card-header model-preview-card-header\">" +
                    "<ul class=\"nav nav-pills card-header-pills\">" +
                    "<li class=\"nav-item\">" +
                    "<a class=\"nav-link active\" href=\"#\">Summary</a>" +
                    "</li>" +
                    "<li class=\"nav-item\">" +
                    "<a class=\"nav-link statisticslink\" href=\"#\">Statistics</a>" +
                    "</li>" +
                    "<li class=\"nav-item\">" +
                    "<a class=\"nav-link disabled\" href=\"#\"> Use</a>" +
                    "</li>" +
                    "</ul>" +
                    "</div>" +
                    "<div class=\"row no-gutters\">" +
                    "<div class=\"col-auto\">" +
                    "<img src=\"//placehold.it/160\" class=\"model-icon\" alt=\"\">" +
                    "</div>" +
                    "<div class=\"col outer\">" +

                    "<div class=\"col main\">" +
                    "<div class=\"card-block px-2\">" +
                    "<h5 class=\"card-title\">" + value.modelname + "</h5>" +
                    "<h5 class=\"card-title\">By " + value.company + "</h5>" +
                    "<h5 class=\"card-title\">Overall Score " + score + "</h5>" +

                    "<h5 class=\"card-title\">Anatomy: " + value.structurename + "Relevance: " + value.modeltoanatomyscore + "</h5>" +

                    "<h6 class=\"card-subtitle mb-2 text-muted\">" + value.modeltext + "</h6>" +
                    "<p class=\"card-text\">Description of the selected model, at a glance statistics, usage caveats etc. Model Price: " + value.modelprice + "by" + value.company + "</p>" +
                    "<a href=\"#\" class=\"card-link\">Sign up to use</a>" +
                    "<a href=\"#\" class=\"card-link\">Similar Models</a>" +
                    "</div>" +
                    "</div>" +



                    "</div>" +

                    "</div>" +
                    "</div>" +
                    "</div>"
            });
            $(".preview-models").html(models_table);
        });
}

// Function below creates an API key by called PHP script.
function createApiKey() {
    $(document).on('click', '.createapikey', function() {
        command = "one";
        $.post("http://chief.ai/dashboard/createapikey.php", {
                command: command,
            },

            function(data, status) {
                alert(data);
            });
    });
}


// Function below writes out all completed exeuctions into a string for inserting into container.


function executionhistory(memberid) {

    alert("about to fire");

    completed_executions = "";
    executionshtml = "";

    $.post('https://api.chief.ai/api/v1.0/executions/retrieve', {
            member_id: memberid
        },
        function(data) {






            $.each(data.Executions, function() {


                alert("about to fire");

                //get the result for each execution

                $.post('https://api.chief.ai/api/v1.0/result/retrieve', {
                        execution_id: this.execution_id,
                    },
                    function(data) {



                        $.each(data.allResults, function() {


                            alert(this.imagename);


                        });

                    });


                executionshtml = executionshtml + "Execution ID: " + this.execution_id + "<br>" + "Date: " + this.created_on + "<br>" + "Credits Expended: " + this.charged_credits + "<br>" + "<span class  = 'execution details executionid " + this.execution_id + "'><strong>Details</strong></span> <br>";
                executiontime.push(this.execution_time);
                executedmodels.push(this.model_id);
                alert(this.model_id);
                alert(this.execution_time);


                $.each(this, function(k, v) {
                    completed_executions = completed_executions + k + " " + v + "<br>";
                });
            });
            $(".completedexecutions").html("Completed Executions:<br />" + executionshtml);
        });
}




function getcredits(memberid, apikey) {

    apiurl = "https://api.chief.ai/api/v1.0/customers/credits";
    console.log("attempting credits retreival from compute engine");

    console.log(memberid);
    console.log(apikey);


    var form_data = new FormData();
    form_data.append("member_id", memberid);


    /* TEST CODE: Variable & data type check: */
    console.log("api key: " + apikey + " " + memberid);



    //alert("url is "+apiurl);          
    $.ajax({
        type: 'POST',
        url: apiurl,
        beforeSend: function(request) {
            request.setRequestHeader("x-api-key", apikey);
        },
        contentType: false,
        processData: false,
        timeout: 600000,
        data: form_data,
        success: function(response) {


            $(".credits").html("Credits " + response.Current_Balance_Credits);

        }
    });
}






/*
// Code below is unknown to me !!!!!!!!!!!!(IS THIS NEEDED?)!!!!!!!!!!!!!!!
$.post("http://172.83.9.18:5000/retrieveownerpostmethod",
	{
	  modelowner: 20,
	},
	function(data,status){
		$( ".currentmodels" ).html("Current Model " + data.ModelName );
	});
*/