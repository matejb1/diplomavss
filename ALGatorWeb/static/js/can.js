// API Examples
// can({'uid': 'u0', 'eid': 'e1', 'codename': 'can_write'}).then((data) => {...})
// can({'eid': 'e1', 'codename': 'can_write'}).then((data) => {...})

var can_dict = {};
function can(dataToSend) {
    if(can_dict.hasOwnProperty(`${dataToSend.eid}${dataToSend.codename}`))
        return new Promise((resolve, reject) => {resolve(can_dict[`${dataToSend.eid}${dataToSend.codename}`])});
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