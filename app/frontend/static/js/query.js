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
            query = $("#query_input").val();
        }
        // syntax prompt
        else if (event.originalEvent.submitter.id == "findErrorsButton") {
            $("#response").html("Searching for errors...");
            query = `
            Generate a comprehensive README.md file that effectively describes a GitHub repository based on provided code snippets. Ensure the README.md includes:

            - Suitable title and short description
            - Table of contents
            - Project overview
            - Features
            - Requirements and dependencies
            - Installation and execution instructions
            - Configuration file
            - Visual file structure tree using 'file_structure.json' (use characters like '├', '─', and '└')
            - Troubleshooting and FAQ
            - Any other relevant information for users or contributors

            The README.md should be long and comprehensive, filling more than a page. Display the contents as markdown text, without describing how to build one.
            `;
        }
        // readme prompt
        else if (event.originalEvent.submitter.id == "buildReadmeButton") {
            $("#response").html("Generating a README.md file...");
            query = `Generate a comprehensive README.md file that effectively describes a GitHub repository based on a set of provided code snippets. The code snippets are the most relevant to the project. Please create a detailed README.md file that includes the following sections: * A suitable title and short description * Table of contents * Project overview * Features * Requirements and dependencies * Installation and execution instructions * Configuration file * A visual file structure tree using 'file_structure.json' (use characters like '├', '─', and '└') * Troubleshooting and FAQ * Any other relevant information for potential users or contributors The generated README.md file should be long and comprehensive, filling more than a page. Please display the contents of the file as markdown text, without simply describing how to build one.`;
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
