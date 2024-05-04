$(document).ready(function () {
    // retrieve structure data
    const structure = JSON.parse($("#json_data").text());

    // get html from json
    let html = recursive_json_parse(structure);
    $("#json_items").html(html);

    // add css to content
    add_css();

    // control button collapse
    $(".collapse_button").click(function () {
        $(this).find("i").toggleClass("bi-caret-right-fill").toggleClass("bi-caret-down-fill");
    });
});

// read json object and format it into html
function recursive_json_parse(structure) {
    let html = "";
    for (let x in structure) {
        // html element wrappers
        const open_wrapper = `<div class="border p-2 type_${structure[x].path}" id="${structure[x].path}">`;
        const close_wrapper = `</div>`;

        html += open_wrapper;

        // directory
        if (structure[x].type == "directory") {
            html += `
                <div class="type_${structure[x].type}" id="container_${structure[x].path}">
                    <h2>${structure[x].name}</h2>
                    <ul class="list-group">
                        <li class="list-group-item" id="repo_desc"><span class="text-muted">Type: </span>${structure[x].type}</li>
                        <li class="list-group-item" id="repo_created"><span class="text-muted">Path: </span>${structure[x].path}</li>
                        <li class="list-group-item" id="repo_size"><span class="text-muted">Content: </span>${Object.keys(structure[x].contents).length}</li>
                    </ul>
                    <button class="collapse_button" type="button" data-bs-toggle="collapse" data-bs-target="#collapse_id_${structure[x].path}" aria-expanded="false" aria-controls="collapseExample" on>
                        <i class="bi bi-caret-right-fill"></i>
                    </button>`;

            let dir_content = recursive_json_parse(structure[x].contents);
            html += `
                <div class="collapse" id="collapse_id_${structure[x].path}">
                ${dir_content}
                </div>`;

            html += `</div>`;
        }

        // file
        else if (structure[x].type == "file") {
            html += `
                <div class="type_${structure[x].type}" id="container_${structure[x].path}">
                    <div class="d-flex justify-content-between">
                        <input type="checkbox" class="form-check-input" id="checkbox_id_${structure[x].path}" name="name_${structure[x].name}" value="value_${structure[x].path}">
                        <label for="${structure[x].path}" style="order: -1">
                            <h2>${structure[x].name}</h2>
                        </label>
                    </div>
                    <ul class="list-group">
                        <li class="list-group-item" id="repo_desc"><span class="text-muted">Type: </span>${structure[x].type}</li>
                        <li class="list-group-item" id="repo_created"><span class="text-muted">Path: </span>${structure[x].path}</li>
                        <li class="list-group-item" id="repo_created"><span class="text-muted">Size: </span>${structure[x].size}</li>
                        <li class="list-group-item" id="repo_created"><span class="text-muted">Content:</span><br/>${structure[x].top_content.join("<br>")}</li>
                    </ul>
                </div>`;
        }

        // symbolic link
        else if (structure[x].type == "link") {
            html += `
                <div class="type_${structure[x].type}" id="container_${structure[x].path}">
                    <h2>${structure[x].name}</h2>
                    <ul class="list-group">
                        <li class="list-group-item" id="repo_desc"><span class="text-muted">Type: </span>${structure[x].type}</li>
                        <li class="list-group-item" id="repo_created"><span class="text-muted">Path: </span>${structure[x].path}</li>
                        <li class="list-group-item" id="repo_created"><span class="text-muted">Target: </span>${structure[x].target}</li>
                    </ul>
                </div>`;
        }

        html += close_wrapper;
    }

    return html;
}

// add css to elements
function add_css() {
    $(".collapse_button").addClass("btn btn-secondary");

    $(".type_directory").addClass("p-3");
    $(".type_file").addClass("p-3");
    $(".type_link").addClass("p-3");
}
