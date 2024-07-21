// API Examples:
// add_entity({'name': 'MyProject', 'et': 'et1', 'uid': 'u2', 'parent': 'e0'});
// add_entity({'name': 'MyQuickSort', 'et': 'et2', 'uid': 'u2', 'is_private': false, 'parent': 'e4'});
// remove_entity('e4');
// remove_user('u5');
// add_user({'username': 'lolek', 'email': 'lolek@bolek.si', 'password': 'Bolek123'});
// add_project({'name': 'Project 1', 'is_private': false, 'owner': 'u2', 'parent': 'e0'});
var ALGATOR_SERVER = 'http://localhost:12321';

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

function add_project(checkData){
    if (!('name' in checkData) || !('owner' in checkData)) {
        throw new Error("add_project: name and owner are required!")
    }
    let dataToSend = {};

    dataToSend.name = checkData.name;
    dataToSend.owner = checkData.owner;
    dataToSend.is_private = true;

    if('parent' in checkData && checkData.parent != null) {
        dataToSend.parent = checkData.parent;
    }

    if('is_private' in checkData && typeof checkData.is_private == "boolean") {
        dataToSend.is_private = checkData.is_private;
    }

    return new Promise((resolve, reject) => {
        $.ajax({
            url: 'http://localhost:12321/PERMISSIONS/ADDPROJECT', // `${ALGATOR_SERVER}/PERMISSIONS/ADDPROJECT`,
            data: JSON.stringify(dataToSend),
            type: 'POST',
    	    headers: {
    	         "Accept": "application/json",
    	         "Authorization": `Bearer ${jwtToken}` //eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzIxNDg1MjM3LCJpYXQiOjE3MjE0ODI1MzcsImp0aSI6ImZjMTBiN2ZmYWRiYjQ3YzFiYzAzMDljMDA1YjMxNGY2IiwidXNlcl9pZCI6MSwidXNlcm5hbWUiOiJyb290IiwiaXNfc3VwZXJ1c2VyIjp0cnVlLCJ1aWQiOiJ1MCJ9.wuP_L-wpm5gjReFgzIwipLW5tGpaIIgqPvloi-c6G48"
    	    },
            success: (data) => resolve(data),
            error: (err) => reject(err),
         });
    });
}