function searchByField(isUserTable) {
    let table = isUserTable ? "#tbodyusers" : "#tbodygroups";
    let key = $("#searchDropdown").find(":selected").val();
    let s = $("#searchField").val();

    $(table).empty();
    let filtered = data.filter((o) => (o[key]).toString().toLowerCase().includes((s).toString().toLowerCase().trim()));
    for(let item of filtered){
        let content = "";
        if(isUserTable){
            content = `<tr scope='row'>
            <td>${wrapAtag(item.id,item.id,'users')}</td>
            <td>${wrapAtag(item.email,item.id,'users')}</td>
            <td>${wrapAtag(item.username,item.id,'users')}</td>
            <td><input class='form-check-input' type='checkbox' ${item.is_superuser ? 'checked' : ''}></td>
            </tr>`;
        }
        else {
            content = `<tr scope='row'>
            <td>${wrapAtag(item.id,item.id,'users')}</td>
            <td>${wrapAtag(item.name,item.id,'groups')}</td>
            </tr>`;
        }
        $(table).append(content);
    }
}

$(window).load(function () {
    searchByField(window.location.pathname == '/permissions/users');
});
