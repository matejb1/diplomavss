function saveUser(id) {
    sendRequest('/permissions/users/edit_user',
                 {
                    'id': id,
                    'username': $('#username').val(),
                    'email': $('#email').val(),
                    'isSuperUser': $('#isSuperUser').is(":checked"),
                    'isStaff': $('#isStaff').is(":checked"),
                    'isActive': $('#isActive').is(":checked"),
                 },
                'PUT').then((resolve, reject) => {
                    alert('Successfully modified user.');
                    document.location.reload();
                });
}

function removeUser(id) {
    sendRequest('/permissions/users/remove_user', {'uid': id}, 'DELETE').then((resolve, reject) => {
        alert('Successfully deleted user.');
        window.location.replace("/permissions/users");
    });
}

function searchByField(table) {
    let s = $("#searchField").val();
    $(table).empty();
    let filtered = searchRows.filter((o) => (o.toLowerCase().includes(s.toLowerCase().trim())));
    for(let item of filtered){
        $(table).append(item);
    }
}

function appendGroupOptions(table='#group-name') {
    $(table).find("option").remove().end();
    let content = "";
    for(let item of allGroups) {
        content += `<option value='${item.pk}' title='${item.fields.name}'>${item.fields.name}</option>`;
    }
    $(table).append(content);
}


function appendPermissionOptions() {
    $('#permission-name').find("option").remove().end();
    let content = "";
    for(let item of allPermissions) {
        can_dict.hasOwnProperty
        can($('#entity-name').val(), item.fields.codename).then((resolve, reject) => {
            if(resolve)
                $('#permission-name').append(`<option value='${item.fields.codename}' title='${item.pk}'>${item.fields.name}</option>`);
        });

    }

}

function appendEnttiesOptions() {
    $('#entity-name').find("option").remove().end();
    let first = true;
    for(let e of entities) {
        let eid = e.pk;
        can(eid, 'can_write').then((data) => {
            if(data)
                $('#entity-name').append(`<option value='${eid}'>${eid}</option>`);
            if(data && first){
                first = false;
                sendRequest('/permissions/groups/get_groups', {"eid": eid}, 'POST').then((resolve, reject) => {
                    allGroups = JSON.parse(resolve);
                    appendGroupOptions();
                    appendGroupOptions('#addusertogroup_groupname');
                    appendGroupOptions('#removeuserfromgroup_groupname');
                    appendPermissionOptions();
                });
            }
        });
    }


    document.querySelector('#entity-name').addEventListener('change', (e) => {
        sendRequest('/permissions/groups/get_groups', {"eid": e.target.value}, 'POST').then((resolve, reject) => {
            allGroups = JSON.parse(resolve);
            appendGroupOptions();
        });
    });
}

function renderUsersTable(request) {
    if(request.status != 200)
        return;
    searchRows = [];
    const data = JSON.parse(request.responseText);
    const table = "#tbodyusers";
    for(let item of data) {
        let content = `<tr scope='row' title='${item.fields.username}'>
                       <td>${wrapAtag(item.pk, item.pk, 'users')}</td>
                       <td>${wrapAtag(item.fields.email, item.pk, 'users')}</td>
                       <td>${wrapAtag(item.fields.username, item.pk, 'users')}</td>
                       <td><input type='checkbox' ${item.fields.is_superuser ? 'checked' : ''} /></td>
                       </tr>`;
        searchRows.push(content);
        $(table).append(content);
    }
}

function delete_group(event) {
    sendRequest('/permissions/groups/remove_group', {"group_id": event.value }, 'DELETE').then((resolve, reject) => {
        alert("Group has been deleted!");
        document.location.reload();
    });
}

function renderPermissionTable(data) {
    let table = "#tbodypermissions";
    let i = 1;
    searchRows = [];
    for(let item of data) {
        let eid = item[0], pvalue = item[1], isPrivate = item[2], userGroup = item[3];

        can(eid, 'can_write').then((data) => {
            let c = data;
            if(!c) return;
            for(let p of allPermissions) {
                let v = p.fields.value;
                if((item[1] & v) == v){
                    let content = `<tr scope='row'>
                                   <td>${i++}</td>
                                   <td>${item[0]}</td>
                                   <td title=${p.pk}>${p.fields.name}</td>
                                   <td><input type='checkbox' ${item[2] == 1 ? 'checked' : ''} value=${item[2]} /></td>
                                   <td>${item[3]}</td>
                                   <td><button type='submit' class='btn btn-danger' onclick='update_permission(this)' data-entity_id="${item[0]}" data-permission_id='${p.pk}' data-usergroup='${item[4]}' value='${v}'>DELETE</button></td>
                                   </tr>`;
                    searchRows.push(content);
                    $(table).append(content);
                }
            }
        });
    }
}

function post_permission(event) {
    let isUser = $("#use_username").is(":checked");
    let endpoint = `/permissions/${isUser ? "users": "groups"}/add_permission`;
    let dataToSend = {
        "id": isUser ? $("#username_all_permissions").val().trim(): $("#group-name").val(),
        "permission_id": $("#permission-name").val(),
        "entity_id": $("#entity-name").val(),
    };

    sendRequest(endpoint, dataToSend, 'PUT').then((resolve, reject) => {
        alert('Permission has been added!');
        document.location.reload();
    });
}

function update_permission(event) {

    let dataToSend = {
        "id": event.dataset.usergroup,
        "value": event.value,
        "permission_id": event.dataset.permission_id,
        "entity_id": event.dataset.entity_id,
    };

    let isUserView = dataToSend.id[0] == 'u';
    let endpoint = `/permissions/${isUserView ? "users": "groups"}/update_permission`;

    sendRequest(endpoint, dataToSend, 'PUT').then((resolve, reject) => {
        alert('Permission has been deleted!');
        document.location.reload();
    });
}

function httpGet(url, callback) {
    const request = new XMLHttpRequest();
    request.open('get', url, true);
    request.onload = function () {
        callback(request);
    }
    request.send();
}

function sendRequest(endpoint, dataToSend, method){
    return new Promise(function(resolve, reject) {
        $.ajax({
            url: endpoint,
            data: dataToSend,
            type: method,
            success: (data) => {resolve(data)},
            error: (err) => {reject(err)}
        });
    });
}

function loadRightsPage(){

    let requests = [sendRequest('/permissions/users/get_permissions', null, 'GET'),
                    sendRequest('/permissions/entities_permissions', null, 'GET'),
                    sendRequest('/permissions/groups/get_groups_user', null, 'GET'),
                    sendRequest('/permissions/get_entities', null, 'GET'),
                    // sendRequest('/permissions/groups/get_groups', {"eid": eid}, 'POST'),
                   ];
    Promise.all(requests).then((result) => {
        allPermissions = JSON.parse(result[0]);
        allEntties = JSON.parse(result[1]);
        userGroups = JSON.parse(result[2]);
        entities = JSON.parse(result[3]);
        renderPermissionTable(allEntties);
        appendEnttiesOptions();
        renderGroupsTable();
    });
}

function post_group() {
    sendRequest('/permissions/groups/add_group', {"name": $("#group_name").val().trim()}, 'POST').then((resolve, reject) => {
        alert("Group has been added!");
        document.location.reload();
    });
}

function add_user_to_group(event) {
    sendRequest('/permissions/groups/add_user_to_group',
                    {"gid": $("#addusertogroup_groupname").val(),
                    "username": $("#addusertogroup_username").val().trim(),},
                    'POST').then((resolve, reject) => {
        alert('Added user to group.');
        document.location.reload();
    });
}

function remove_user_from_group(event) {
    sendRequest('/permissions/groups/remove_user_from_group',
            {"gid": $("#removeuserfromgroup_groupname").val(),
            "username": $("#removeuserfromgroup_username").val().trim(),
            }, 'DELETE').then((resolve, reject) => {
        alert('User has been deleted from group.');
        document.location.reload();
    });
}


function renderGroupsTable() {
   let i = 1;
    for(let item of userGroups) {
        let content = `<tr scope='row'>
                       <td>${i++}</td>
                       <td title='${item.pk}'>${item.fields.name}</td>
                       <td><button type="submit" onclick="delete_group(this)" value="${item.pk}" class="btn btn-danger">Delete</button></td>
                       </tr>`;
        $("#tbodygroups").append(content);
    }
}

function wrapAtag(content, id, usergroup){
    return `<a style='color:black' href='/permissions/${usergroup}/${id}'>${content}</a>`;
}