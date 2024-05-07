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
            $("#response").html("Generating a response...");
            query = $("#query_input").val() + "\n\nIf you can not answer, simply say 'Unable to answer your request. Please reword your request and try again.' if you cannot provide adequate information.";
        }
        // syntax prompt
        else if (event.originalEvent.submitter.id == "findErrorsButton") {
            $("#response").html("Searching for errors...");
            hint = $("#query_input").val();
            query = `
            Determine the syntax errors in the provided code. Provide the following information for each error:
            - File location
            - Line number
            - Assumed programming language of the file (i.e. "Python", "Java", etc.)
            - Relevant code lines where the error is apparent
            - A clear and concise description of the fix required to resolve the error
            
            If no errors are found, respond with a confirmation statement (e.g., 'No errors detected.') rather than providing any additional details
            
            Here is a hint: ${hint}`;
        }
        // readme prompt
        else if (event.originalEvent.submitter.id == "buildReadmeButton") {
            $("#response").html("Generating a README.md file...");
            hint = $("#query_input").val();
            query = `
            Generate a comprehensive README.md file for a GitHub repository based on a set of provided code snippets with slight overlaps. The README.md may include the following relevant sections:

            1. A suitable title and short description
            2. Table of contents
            3. Project overview (including popular languages)
            4. Features
            5. Requirements and dependencies
            6. Installation and execution instructions
            7. Configuration file
            8. Full file structure tree using 'file_structure.json' (use characters like '├', '│', '─', and '└')
            9. Troubleshooting
            10. Any other relevant information for potential users or contributors

            Don't include the section if there is no information on it.

            Please ensure that the README.md file is long and comprehensive, filling several pages. Display the contents as markdown test.
            Please write the content, DO NOT DESCRIBE HOW TO BUILD ONE.
            
            Here is a hint: ${hint}`;
        } else {
            $("#response").html("Generating a response...");
        }

        $.ajax({
            url: "/ai",
            type: "POST",
            data: { query_input: query },
            success: function (data) {
                console.log("Success:", data);
                formatted_response = data.response.replace(/\n/g, "<br>");
                $("#response").html(formatted_response);
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
