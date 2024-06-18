var can_dict = {};


function can(eid, codename) {
    if(can_dict.hasOwnProperty(`${eid}${codename}`))
        return new Promise((resolve, reject) => {resolve(can_dict[`${eid}${codename}`])});
    return new Promise(function(resolve, reject) {
        $.ajax({
            url: '/permissions/can',
            data: {'eid': eid, 'codename': codename},
            type: 'POST',
            success: function(data) {
                let result = data.toLowerCase() === 'true';
                can_dict[`${eid}${codename}`] = result;
                resolve(result);
            },
            error: function(err) {
                reject(false);
            }
      });
    });
}