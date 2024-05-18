function setComponentsValues() {
    $('#group-title').text(group.fields.name);
}

$(window).load(function () {
    setComponentsValues();
    appendPermissionOptions();
    appendEnttiesOptions();
    renderPermissionTable();
});