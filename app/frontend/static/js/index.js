$(document).ready(function () {
    // url form
    $("#url_form").submit(function (event) {
        event.preventDefault(); // Prevent page reload

        // spinner
        $("#repo_spinner").show();

        // Get the url
        let formData = new FormData(this);
        const [username, repoName] = $("#url_input").val().split("/").slice(-2);
        const apiUrl = `https://api.github.com/repos/${username}/${repoName.split("/")[0]}`;

        console.log(apiUrl);

        $.ajax({
            url: apiUrl,
            method: "GET",
            dataType: "json",
            success: function (data) {
                $("#repo_info").show();

                $("#repo_owner").html("owner: " + data.owner.login);
                $("#user_url").prop("href", data.owner.html_url);
                $("#user_avatar").prop("src", data.owner.avatar_url);
            },
            error: function (xhr, status, error) {
                $("#repo_container").append(`<p>Unable to locate repository.${error}</p>`);
                console.error("There was a problem with the AJAX request:", error);
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
