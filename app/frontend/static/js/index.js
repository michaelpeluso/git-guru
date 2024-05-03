$(document).ready(function () {
    // url form
    $("#url_form").submit(function (event) {
        event.preventDefault(); // Prevent page reload

        // update component visibility
        $("#repo_spinner").show();
        $("#repo_info").hide();
        $("#repo_invalidurl").hide();
        $("#repo_notfound").hide();

        // check for valid url format
        url = $("#url_input").val().trim();
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
                $("#repo_created").html("<span class='text-muted'>Repository creation:</span> " + formatted_date(data.created_at));
                $("#repo_updated").html("<span class='text-muted'>Last repository update:</span> " + formatted_date(data.updated_at));
                $("#repo_size").html("<span class='text-muted'>Total repository size (in KB):</span> " + data.size);
                $("#repo_lang").prop("src", "https://cdn.jsdelivr.net/npm/programming-languages-logos/src/" + data.language.toLowerCase() + "/" + data.language.toLowerCase() + ".png");
                $("#repo_lang_name").html(data.language);
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
    });
});

// Send an AJAX request to the backend
/*      
        $.ajax({
            url: "/",
            type: "POST",
            data: formData,
            processData: false,
            contentType: false,
            success: function (data) {
                console.log(data);
                $("#repo_spinner").hide();
                // TODO: get repo info with https://api.github.com/repos/{user}/{repo}
                getRepoInfo();
            },
            error: function (error) {
                console.error("Error:", error);
            },
        });
*/