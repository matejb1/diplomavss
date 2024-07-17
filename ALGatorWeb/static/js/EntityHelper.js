// API Examples:
// add_entity({'name': 'MyProject', 'et': 'et1', 'uid': 'u2', 'parent': 'e0'});
// add_entity({'name': 'MyQuickSort', 'et': 'et2', 'uid': 'u2', 'is_private': false, 'parent': 'e4'});
// remove_entity('e4');
// remove_user('u5');
// add_user({'username': 'lolek', 'email': 'lolek@bolek.si', 'password': 'Bolek123'});
function add_entity(checkData){

    if(!('name' in checkData) || !('et' in checkData) || !('uid' in checkData)) {
        throw new Error('add_entity: Missing name, et and uid.')
    }
    let dataToSend = {};

    dataToSend.name = checkData.name;
    dataToSend.et = checkData.et;
    dataToSend.uid = checkData.uid;

    if('parent' in checkData && checkData.parent != null) {
        dataToSend.parent = checkData.parent;
    }

    if('is_private' in checkData && typeof checkData.is_private == "boolean") {
        dataToSend.is_private = checkData.is_private;
    }

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
    if(!('username' in dataToSend) || !('email' in dataToSend) || !('password' in dataToSend)) {
        throw new Error("add_user: username, email and password are required!")
    }

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