$(document).ready(function () {
    // url form
    $("#url-form").submit(function (event) {
        event.preventDefault(); // Prevent page reload

        // spinner
        $("#outputContainer").html("<p>Loading...</p>");

        // Get the form data
        let formData = new FormData(this);

        // Send an AJAX request to the backend
        $.ajax({
            url: "/",
            type: "POST",
            data: formData,
            processData: false,
            contentType: false,
            success: function (data) {
                console.log(data);

                // Display the output in the output container
                let outputContainer = $("#outputContainer");
                outputContainer.html(`<p>${data.message}</p>`);
            },
            error: function (error) {
                console.error("Error:", error);
                // Handle errors if any
            },
        });
    });

    // other form
    $("#other-form").submit(function (event) {
        event.preventDefault(); // Prevent page reload

        // Get the form data
        let formData = new FormData(this);

        // Send an AJAX request to the backend
        $.ajax({
            url: "/",
            type: "POST",
            data: formData,
            processData: false,
            contentType: false,
            success: function (data) {
                console.log(data);

                // Display the output in the output container
                let outputContainer = $("#outputContainer");
                outputContainer.html(`<p>${data.message}</p>`);
            },
            error: function (error) {
                console.error("Error:", error);
                // Handle errors if any
            },
        });
    });
});
