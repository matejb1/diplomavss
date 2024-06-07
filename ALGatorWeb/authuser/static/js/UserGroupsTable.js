

function appendGroupOptions() {
    $('#group-name').find("option").remove().end();
    let content = "";
    for(let item of allGroups) {
        content += `<option value='${item.pk}'>${item.fields.name}</option>`;
    }
    $('#group-name').append(content);
}



