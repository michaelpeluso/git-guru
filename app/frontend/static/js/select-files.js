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

    // check all files in directory when directory is set
    document.querySelectorAll('input[type="checkbox"].form-check-input').forEach(function (checkbox) {
        checkbox.addEventListener("change", function () {
            dir_is_checked = this.checked;

            // find checkboxes in directory
            let directoryPath = this.getAttribute("id").replace("checkbox_id_", "");
            let fileCheckboxes = document.querySelectorAll(`input[type="checkbox"][id^="checkbox_id_${directoryPath}_"]`);

            // check all inside  directory
            fileCheckboxes.forEach(function (fileCheckbox) {
                // check or uncheck
                fileCheckbox.checked = dir_is_checked;
            });
        });
    });
});

// read json object and format it into html
function recursive_json_parse(structure) {
    let html = "";
    for (let x in structure) {
        // html element wrappers
        structure[x].path = structure[x].path.replaceAll("/", "_").replace(".", "-");

        const open_wrapper = `<div class=" type_${structure[x].path}" id="${structure[x].path}">`;
        const close_wrapper = `</div>`;

        html += open_wrapper;

        // directory
        if (structure[x].type == "directory") {
            count = Object.keys(structure[x].contents).length;
            count_str = count == 1 ? count + " item" : count + " items";
            dir_content = recursive_json_parse(structure[x].contents);

            html += `
                <div class="type_${structure[x].type} border-top" id="container_${structure[x].path}">
                    <div class="d-flex">
                        <input type="checkbox" class="form-check-input" id="checkbox_id_${structure[x].path}" name="name_${structure[x].name}" value="value_${structure[x].path}">
                        <button type="button" class="w-100 btn collapse_button btn-sm p-0" data-bs-toggle="collapse" data-bs-target="#collapse_id_${structure[x].path}" aria-expanded="false" aria-controls="collapseExample" on>
                            <div class="d-flex justify-content-between">
                                <div class="d-flex gap-2 align-items-center">
                                    <h6><i class="bi bi-caret-right-fill heading p-0 m-0"></i></h6>
                                    <h6 class="cursor-pointer">${structure[x].name}</h6>
                                </div>
                                <span class="d-flex text-end text-muted">${count_str}</span>
                            </div>
                        </button>
                    </div>
                    <div class="collapse" id="collapse_id_${structure[x].path}">
                        <div class="type_${structure[x].type} d-flex flex-column align-items-end" id="container_${structure[x].path}">
                            <div style="width: 95%">
                                ${dir_content}
                            </div>
                        </div>
                    </div>
                </div>`;
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
