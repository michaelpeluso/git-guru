$(document).ready(function () {
    // url form
    $("#url_form").submit(function (event) {
        // repo api data
        apiData = {};

        // search for repo
        if ($(document.activeElement).attr("id") === "submitButton") {
            // Prevent page reload
            event.preventDefault();

            // update component visibility
            $("#repo_spinner").show();
            $("#repo_info").hide();
            $("#repo_invalidurl").hide();
            $("#repo_notfound").hide();

            // check for valid url format
            url = $("#repo_url").val().trim();
            url = url.startsWith("https://") ? url : "https://" + url;
            const [user, repo] = url.split("/").slice(3, 5);
            if (!/^https:\/\/github\.com\/[^\/]+\/[^\/]+/.test(url)) {
                $("#repo_spinner").hide();
                $("#repo_invalidurl").show();
                return;
            }

            // Get the url
            const apiUrl = `https://api.github.com/repos/${user}/${repo}`;

            // format date
            const formatted_date = (dateString) => new Date(dateString).toLocaleString("default", { month: "long" }) + " " + new Date(dateString).getFullYear();

            // api call for repo info
            $.ajax({
                url: apiUrl,
                method: "GET",
                dataType: "json",
                success: function (data) {
                    // publicize data
                    console.log(data);

                    // show info
                    $("#repo_info").show();

                    // user info
                    $("#repo_owner").html(data.owner.login);
                    $("#user_url").prop("href", data.owner.html_url);
                    $("#user_avatar").prop("src", data.owner.avatar_url);

                    // repo info
                    $("#repo_name").html(data.name);
                    $("#repo_id").html(data.id);
                    $("#repo_desc").html(data.description || "No description found.");
                    $("#repo_created").html(`<span class='text-muted'>Repository creation:</span> ${formatted_date(data.created_at)}`);
                    $("#repo_updated").html(`<span class='text-muted'>Last repository update:</span> ${formatted_date(data.updated_at)}`);
                    $("#repo_size").html(`<span class='text-muted'>Total repository size:</span> ${convertFromBytes(data.size * 1024)}`);
                    $("#repo_lang").prop("src", `https://cdn.jsdelivr.net/npm/programming-languages-logos/src/${data.language.toLowerCase()}/${data.language.toLowerCase()}.png`);
                    $("#repo_lang_name").html(data.language);

                    // enable confirm button
                    $("#confirmButton").prop("disabled", false).removeClass("disabled");
                },
                error: function (xhr, status, error) {
                    $("#repo_notfound").show();
                    console.error("There was a problem with the AJAX request:", error);
                },
                // always execute
                complete: function (data) {
                    $("#repo_spinner").hide();
                },
            });
        }
        // confirm repo
        else if ($(document.activeElement).attr("id") === "confirmButton") {
            // Send an AJAX request to the backend
            $.ajax({
                url: "/file-selection",
                type: "POST",
                data: $("#url_form").serialize(),
                success: function (response) {
                    console.log("Response from server:", response);
                },
                error: function (error) {
                    console.error("Error:", error);
                },
            });
        }
    });
});

function convertFromBytes(sizeInBytes) {
    var units = ["bytes", "KB", "MB", "GB", "TB"];
    var unitIndex = 0;
    var size = sizeInBytes;

    while (size >= 1024 && unitIndex < units.length - 1) {
        size /= 1024;
        unitIndex++;
    }

    return size.toFixed(3) + " " + units[unitIndex];
}
