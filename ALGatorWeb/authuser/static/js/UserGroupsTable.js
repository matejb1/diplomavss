function setComponentsValues() {
    $('#username').val(currentUser.fields.username);
    $('#email').val(currentUser.fields.email);
    $('#isSuperUser').prop("checked", currentUser.fields.is_superuser);
    $('#isStaff').prop("checked", currentUser.fields.is_staff);
    $('#isActive').prop("checked", currentUser.fields.is_active);
}

function renderGroupsTable() {
    let table = "#tbodygroups";

    for(let item of userGroups) {
        let lGroupId = wrapAtag(item.id, item.id, 'groups');
        let lGroupName = wrapAtag(item.name, item.id, 'groups');
        let content = `<tr scope='row'>
                       <td>${lGroupId}</td>
                       <td>${lGroupName}</td>
                       <td><button type="submit" onclick="delete_group(this)" value="${item.id}" class="btn btn-danger">Delete</button></td>
                       </tr>`;
        $(table).append(content);
    }
}

function appendGroupOptions() {
    $('#group-name').find("option").remove().end();
    let content = "";
    for(let item of allGroups) {
        content += `<option value='${item.id}'>${item.name}</option>`;
    }
    $('#group-name').append(content);
}


function delete_group(event) {
    $.ajax({
        url: '/permissions/groups/remove_group',
        data: {"group_id": event.value, "user_id": currentUser.pk},
        type: 'DELETE',
        success: function(data, status) {
            alert(status == "success" ? "Group has been deleted!" : "Cannot delete this group!");
        }
    });
}

$(window).load(function () {
    setComponentsValues();
    appendGroupOptions();
    appendPermissionOptions();
    appendEnttiesOptions();
    renderGroupsTable();
    renderPermissionTable();

    $("#postgroup").click(function() {
        $.post("/permissions/groups/add_group", {"group_id": $("#group-name").val(), "user_id": currentUser.pk}, function(data, status){
            alert(status == "success" ? "Group has been added!" : "Cannot add to group!");
        });
    });


});


