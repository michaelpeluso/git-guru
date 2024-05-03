$(document).ready(function () {
    // retreive structure data
    var structure = JSON.parse($("#mySpan").text());

    let text = "";

    for (let x in structure) {
        text = `<label class="list-group-item d-flex gap-2">
                <input class="form-check-input flex-shrink-0" type="checkbox" value="" checked>
                <span>`;
        text += `<p>${structure[x].name}</p>`;
        text += `<p>${structure[x].name}</p>`;
        text += `<p>${structure[x].name}</p>`;
    }
    text += "</table>";

    $("#list_group").html(text);
});
