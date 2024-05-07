$(document).ready(function () {
    // auto sizing textarea
    var text = $("#query_input");

    text.on("change", resize);
    text.on("cut", delayedResize);
    text.on("paste", delayedResize);
    text.on("drop", delayedResize);
    text.on("keydown", delayedResize);

    text.focus();
    text.select();
    resize();

    // send an AJAX request to the backend
    $("#query_form").on("submit", function (event) {
        event.preventDefault();
        query = "";

        // detect what button is pressed
        // user prompt
        if (event.originalEvent.submitter.id == "submitButton") {
            query = $("#query_input").val();

            if ($("#query_input").val() == "") {
                $("#response").html("Please enter a request.");
                return;
            }
            $("#response").html("Generating a response...");

            query += "\nIf you cannot provide adequate information, respond with 'Unable to answer your request. Please reword your request and try again.'";
        }
        // syntax prompt
        else if (event.originalEvent.submitter.id == "findErrorsButton") {
            $("#response").html("Searching for errors...");
            query = `
            Identify and correct any syntax errors in the following code. Please provide the file location, line number, and clear and concise explanation for each correction made.
            If no errors are found respond with 'No errors detected.'`;

            hint = $("#query_input").val();
            query += hint != "" ? `\nHere is a provided request: ${hint}` : "";
        }
        // readme prompt
        else if (event.originalEvent.submitter.id == "buildReadmeButton") {
            $("#response").html("Generating a README.md file...");
            query = `
            Generate a comprehensive README.md file for a GitHub repository based on a set of provided code snippets with slight overlaps. The README.md may include the following relevant sections:
            - A suitable title and short description
            - Table of contents
            - Project overview (including popular languages)
            - Features
            - Requirements and dependencies
            - Installation and execution
            - Full file structure tree using 'file_structure.json' (use characters like '├', '│', '─', and '└')
            - Troubleshooting
            - Any other relevant information for potential users or contributors
            Don't include the section if there is no information on it.
            Please ensure that the README.md file is long and comprehensive, filling several pages. Display the contents as markdown test.
            Please write the content, DO NOT DESCRIBE HOW TO BUILD ONE.`;

            hint = $("#query_input").val();
            query += hint != "" ? `\nHere is a provided request: ${hint}` : "";
        } else {
            $("#response").html("Generating a response...");
        }

        $.ajax({
            url: "/ai",
            type: "POST",
            data: { query_input: query },
            success: function (data) {
                console.log("Success:", data);
                if (data.response) {
                    $("#response").html(data.response.replace(/\n/g, "<br>"));
                } else {
                    $("#response").html(data.response_status);
                }
            },
            error: function (error) {
                console.error("Error:", error);
                $("#response").html("Error: No response.");
            },
        });
    });
});

function resize() {
    text = $("#query_input");
    text.css("height", "auto");
    text.css("height", text.prop("scrollHeight") + "px");
}

function delayedResize() {
    setTimeout(resize, 0);
}
