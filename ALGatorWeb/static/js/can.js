// API Examples
// can({'uid': 'u0', 'eid': 'e1', 'codename': 'can_write'}).then((data) => {...})
// can({'eid': 'e1', 'codename': 'can_write'}).then((data) => {...})

var can_dict = {};
function can(checkdata) {

    // Return if you have in cache.
    if(can_dict.hasOwnProperty(`${checkdata.eid}${checkdata.codename}`)) {
        return new Promise((resolve, reject) => {resolve(can_dict[`${checkdata.eid}${checkdata.codename}`])});
    }

    let dataToSend = {};
    if(!('eid' in checkdata) || !('codename' in checkdata)){
        throw new Error("can: 'eid' and 'codename' are missing!")
    }
    dataToSend.eid = checkdata.eid;
    dataToSend.codename = checkdata.codename;

    if('uid' in checkdata) {
        dataToSend.uid = checkdata.uid;
    }

    return new Promise((resolve, reject) => {
        $.ajax({
            url: '/permissions/can',
            data: dataToSend,
            type: 'POST',
            success: function(data) {
                let result = data.toLowerCase() === 'true';
                can_dict[`${dataToSend.eid}${dataToSend.codename}`] = result;
                resolve(result);
            },
            error: function(err) {
                reject(false);
            }
      });
    });
}