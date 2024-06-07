function setComponentsValues() {
    $('#username').val(currentUser.fields.username);
    $('#email').val(currentUser.fields.email);
    $('#isSuperUser').prop("checked", currentUser.fields.is_superuser);
    $('#isStaff').prop("checked", currentUser.fields.is_staff);
    $('#isActive').prop("checked", currentUser.fields.is_active);
}

function loadSingleUserPage(id){
    httpGet(`/permissions/users/get_user/${id}`, (request) => {
        if(request.status != 200)
            return;
        currentUser = JSON.parse(request.responseText)[0];
        setComponentsValues();
    });
}