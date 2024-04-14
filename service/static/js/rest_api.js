$(function () {

    // ****************************************
    //  U T I L I T Y   F U N C T I O N S
    // ****************************************

    // Updates the form with data from the response
    function update_form_data(res) {
        $("#recommendation_id").val(res.recommendation_id);
        $("#recommendation_name").val(res.name);
        $("#recommendation_recommendation_name").val(res.recommendation_name);
        $("#recommendation_recommendation_type").val(res.recommendation_type);
    }

    /// Clears all form fields
    function clear_form_data() {
        $("#recommendation_name").val("");
        $("#recommendation_recommendation_name").val("");
        $("#recommendation_recommendation_type").val("");
    }

    // Updates the flash message area
    function flash_message(message) {
        $("#flash_message").empty();
        $("#flash_message").append(message);
    }

    // ****************************************
    // Create a Recommendation
    // ****************************************

    $("#create-btn").click(function () {

        let name = $("#recommendation_name").val();
        let recommendation_name = $("#recommendation_recommendation_name").val();
        let recommendation_type = $("#recommendation_recommendation_type").val();

        let data = {
            "name": name,
            "recommendation_name": recommendation_name,
            "recommendation_type": recommendation_type
        };

        $("#flash_message").empty();
        
        let ajax = $.ajax({
            type: "POST",
            url: "/recommendations",
            contentType: "application/json",
            data: JSON.stringify(data),
        });

        ajax.done(function(res){
            update_form_data(res)
            flash_message("Success")
        });

        ajax.fail(function(res){
            flash_message(res.responseJSON.message)
        });
    });


    // ****************************************
    // Update a Recommendation
    // ****************************************

    $("#update-btn").click(function () {

        let recommendation_id = $("#recommendation_id").val();
        let name = $("#recommendation_name").val();
        let recommendation_name = $("#recommendation_recommendation_name").val();
        let recommendation_type = $("#recommendation_recommendation_type").val();

        let data = {
            "name": name,
            "recommendation_name": recommendation_name,
            "recommendation_type": recommendation_type
        };

        $("#flash_message").empty();

        let ajax = $.ajax({
                type: "PUT",
                url: `/recommendations/${recommendation_id}`,
                contentType: "application/json",
                data: JSON.stringify(data)
            })

        ajax.done(function(res){
            update_form_data(res)
            flash_message("Success")
        });

        ajax.fail(function(res){
            flash_message(res.responseJSON.message)
        });

    });

    // ****************************************
    // Retrieve a Recommendation
    // ****************************************

    $("#retrieve-btn").click(function () {

        let recommendation_id = $("#recommendation_id").val();

        $("#flash_message").empty();

        let ajax = $.ajax({
            type: "GET",
            url: `/recommendations/${recommendation_id}`,
            contentType: "application/json",
            data: ''
        })

        ajax.done(function(res){
            //alert(res.toSource())
            update_form_data(res)
            flash_message("Success")
        });

        ajax.fail(function(res){
            clear_form_data()
            flash_message(res.responseJSON.message)
        });

    });

    // ****************************************
    // Delete a Recommendation
    // ****************************************

    $("#delete-btn").click(function () {

        let recommendation_id = $("#recommendation_id").val();

        $("#flash_message").empty();

        let ajax = $.ajax({
            type: "DELETE",
            url: `/recommendations/${recommendation_id}`,
            contentType: "application/json",
            data: '',
        })

        ajax.done(function(res){
            clear_form_data()
            flash_message("Recommendation has been Deleted!")
        });

        ajax.fail(function(res){
            flash_message("Server error!")
        });
    });

    // ****************************************
    // Clear the form
    // ****************************************

    $("#clear-btn").click(function () {
        $("#recommendation_id").val("");
        $("#flash_message").empty();
        clear_form_data()
    });

    // ****************************************
    // Search for a Recommendation
    // ****************************************

    $("#search-btn").click(function () {

        let name = $("#recommendation_name").val();
        let recommendation_name = $("#recommendation_recommendation_name").val();
        let recommendation_type = $("#recommendation_recommendation_type").val();

        let queryString = ""

        if (name) {
            queryString += 'name=' + name
        }
        if (recommendation_name) {
            if (queryString.length > 0) {
                queryString += '&recommendation_name=' + recommendation_name
            } else {
                queryString += 'recommendation_name=' + recommendation_name
            }
        }
        if (recommendation_type) {
            if (queryString.length > 0) {
                queryString += '&recommendation_type=' + recommendation_type
            } else {
                queryString += 'recommendation_type=' + recommendation_type
            }
        }

        $("#flash_message").empty();

        let ajax = $.ajax({
            type: "GET",
            url: `/recommendations?${queryString}`,
            contentType: "application/json",
            data: ''
        })

        ajax.done(function(res){
            //alert(res.toSource())
            $("#search_results").empty();
            let table = '<table class="table table-striped" cellpadding="10">'
            table += '<thead><tr>'
            table += '<th class="col-md-2">ID</th>'
            table += '<th class="col-md-2">Name</th>'
            table += '<th class="col-md-2">Recommendation Name</th>'
            table += '<th class="col-md-2">Recommendation Type</th>'
            table += '</tr></thead><tbody>'
            let firstRecommendation = "";
            for(let i = 0; i < res.length; i++) {
                let recommendation = res[i];
                table +=  `<tr id="row_${i}"><td>${recommendation.recommendation_id}</td><td>${recommendation.name}</td><td>${recommendation.recommendation_name}</td><td>${recommendation.recommendation_type}</td></tr>`;
                if (i == 0) {
                    firstRecommendation = recommendation;
                }
            }
            table += '</tbody></table>';
            $("#search_results").append(table);

            // copy the first result to the form
            if (firstRecommendation != "") {
                update_form_data(firstRecommendation)
            }

            flash_message("Success")
        });

        ajax.fail(function(res){
            flash_message(res.responseJSON.message)
        });

    });

})