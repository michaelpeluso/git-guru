$(document).ready(function () {
    // retrieve structure data
    const jsonData = $("#json_data").text().trim();
    const structure = jsonData ? JSON.parse(jsonData) : {};

    console.log(structure);

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
        const open_wrapper = `<div class=" type_${structure[x].path}" id="${structure[x].path}">`;
        const close_wrapper = `</div>`;

        html += open_wrapper;

        // directory
        if (structure[x].type == "directory") {
            count = Object.keys(structure[x].contents).length;
            count_str = count == 1 ? count + " item" : count + " items";
            html += `
                <div class="type_${structure[x].type} border-top" id="container_${structure[x].path}">
                    <button type="button" class="w-100 btn collapse_button btn-sm" data-bs-toggle="collapse" data-bs-target="#collapse_id_${structure[x].path}" aria-expanded="false" aria-controls="collapseExample" on>
                    <div class="d-flex justify-content-between">
                            <div class="d-flex gap-2 align-items-center">
                                <h6><i class="bi bi-caret-right-fill heading p-0 m-0"></i></h6>
                                <h6 class="cursor-pointer">${structure[x].name}</h6>
                            </div>
                        <span class="d-flex text-end text-muted">${count_str}</span>
                    </button>`;

            let dir_content = recursive_json_parse(structure[x].contents);
            html += `
                <div class="collapse" id="collapse_id_${structure[x].path}">
                    <div class="type_${structure[x].type} d-flex flex-column align-items-end" id="container_${structure[x].path}">
                        <div style="width: 95%">
                            ${dir_content}
                        </div>
                    </div>
                </div>`;

            html += `</div>`;
        }

        // file
        else if (structure[x].type == "file") {
            html += `
                <div class="type_${structure[x].type} border-top" id="container_${structure[x].path}">
                    <div class="d-flex flex-wrap justify-content-between pb-2">
                        <div class="d-flex flex-wrap align-items-center">
                            <input type="checkbox" class="form-check-input" id="checkbox_id_${structure[x].path}" name="name_${structure[x].name}" value="value_${structure[x].path}">
                            <label for="${structure[x].path}" >
                                <h6">${structure[x].name}</h6>
                            </label>
                        </div>
                        <span class="text-muted">${structure[x].size} bytes</span>
                    </div>
                </div>`;
        }

        // symbolic link
        else if (structure[x].type == "link") {
            html += `
                <div class="type_${structure[x].type}" id="container_${structure[x].path}">
                    <span>${structure[x].name}</span>
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
    $(".type_directory").addClass("p-3");
    $(".type_file").addClass("p-3");
    $(".type_link").addClass("p-3");
}
