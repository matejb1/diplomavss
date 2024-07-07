// API Examples:
// add_entity({'name': 'MyProject', 'et': 'et1', 'uid': 'u2', 'parent': 'e0'});
// add_entity({'name': 'MyQuickSort', 'et': 'et2', 'uid': 'u2', 'is_private': false, 'parent': 'e4'});
// remove_entity('e4');
// remove_user('u5');
// add_user({'username': 'lolek', 'email': 'lolek@bolek.si', 'password': 'Bolek123'});
function add_entity(dataToSend){
    return new Promise((resolve, reject) => {
        $.ajax({
            url: '/permissions/add_entity',
            data: dataToSend,
            type: 'POST',
            success: (data) => resolve(data),
            error: (err) => reject(false),
         });
    });
}

function remove_entity(eid){
    return new Promise((resolve, reject) => {
        $.ajax({
            url: '/permissions/remove_entity',
            data: {'eid': eid},
            type: 'DELETE',
            success: (data) => resolve(data),
            error: (err) => reject(false),
         });
    });
}

function add_user(dataToSend){
    return new Promise((resolve, reject) => {
        $.ajax({
            url: '/permissions/add_user',
            data: dataToSend,
            type: 'POST',
            success: (data) => resolve(data),
            error: (err) => reject(false),
         });
    });
}

function remove_user(uid){
    return new Promise((resolve, reject) => {
        $.ajax({
            url: '/permissions/users/remove_user',
            data: {'uid': uid},
            type: 'DELETE',
            success: (data) => resolve(data),
            error: (err) => reject(false),
         });
    });
}