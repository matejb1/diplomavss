function appendPermissionOptions() {
    $('#permission-name').find("option").remove().end();
    let content = "";
    for(let item of allPermissions) {
        content += `<option value='${item.id}' title='${item.codename}'>${item.name}</option>`;
    }
    $('#permission-name').append(content);
}

function appendEnttiesOptions() {
    $('#entity-name').find("option").remove().end();
    let content = "";
    for(let item of allEntties) {
        content += `<option value='${item[0]}' title='Type: ${item[4]} by "${item[6]}"'>${item[1]}</option>`;
    }
    $('#entity-name').append(content);
}

function renderPermissionTable() {
    let table = "#tbodypermissions";
    for(let item of permissions) {
        let content = `<tr scope='row' title='${item[6]}'>
                       <td>${item[0]}</td>
                       <td>${item[3]}</td>
                       <td>${item[5]}</td>
                       <td><input type='checkbox' ${item[4] == 1 ? 'checked' : ''} value=${item[4]} /></td>
                       <td><button type='submit' class='btn btn-danger' onclick='delete_permission(this)' data-entity_id="${item[1]}" data-permission_id='${item[2]}' value='${item[0]}'>DELETE</button></td>
                       </tr>`;
        $(table).append(content);
    }
}

function post_permission(event) {
    let isUserView = window.location.pathname.startsWith('/permissions/users');
    let endpoint = `/permissions/${isUserView ? "users": "groups"}/add_permission`;
    let dataToSend = {
        "permission_id": $("#permission-name").val(),
        "entity_id": $("#entity-name").val(),
    };
    if(isUserView)
        dataToSend.user_id = currentUser.pk;
    else
        dataToSend.group_id = group.pk;

    $.ajax({
        url: endpoint,
        data: dataToSend,
        type: 'POST',
        success: function(data, status) {
            if(status == "success"){
                alert("Permission has been added!");
                document.location.reload();
            }
        }
    });
}

function delete_permission(event) {
    let isUserView = window.location.pathname.startsWith('/permissions/users');
    let endpoint = `/permissions/${isUserView ? "users": "groups"}/remove_permission`;

    let dataToSend = {
        "id": event.value,
        "permission_id": event.dataset.permission_id,
        "entity_id": event.dataset.entity_id,
    };
    if(isUserView)
        dataToSend.user_id = currentUser.pk;
    else
        dataToSend.group_id = group.pk;

    $.ajax({
        url: endpoint,
        data: dataToSend,
        type: 'DELETE',
        success: function(data, status) {
            if(status == "success"){
                alert("Permission has been deleted!");
                document.location.reload();
            }
        }
    });
}


function wrapAtag(content, id, usergroup){
    return `<a style='color:black' href='/permissions/${usergroup}/${id}'>${content}</a>`;
}