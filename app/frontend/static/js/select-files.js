$(document).ready(function () {
    // retreive structure data
    var structure = JSON.parse($("#mySpan").text());

    let text = "";

    for (let x in structure) {
        // wrapper html
        text = `<label class="list-group-item d-flex gap-2">
                <input class="form-check-input flex-shrink-0" type="checkbox" value="" checked>
                <span>`;

        // common attributes
        text += `<p>Name: ${structure[x].name}</p>`;
        text += `<p>type: ${structure[x].type}</p>`;

        // directory
        if (structure[x].type == "directory") {
            text += `<p>Content count: ${Object.keys(structure[x].contents).length}</p>`;
        }

        // file
        else if (structure[x].type == "file") {
            text += `<p>Name: ${structure[x].path}</p>`;
            text += `<p>type: ${structure[x].size}</p>`;
            text += `<p>type: ${structure[x].top_content}</p>`;
        }

        // symbolic link
        else if (structure[x].type == "link") {
            text += `<p>Name: ${structure[x].path}</p>`;
            text += `<p>type: ${structure[x].target}</p>`;
        }
    }
    text += `</span></label></input>`;

    $("#list_group").html(text);
});
