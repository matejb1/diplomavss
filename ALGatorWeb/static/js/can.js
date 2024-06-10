var can_dict = {};


function can(eid, pid) {
    if(can_dict.hasOwnProperty(`${eid}${pid}`))
        return new Promise((resolve, reject) => {resolve(can_dict[`${eid}${pid}`])});
    return new Promise(function(resolve, reject) {
        $.ajax({
            url: '/permissions/can',
            data: {'eid': eid, 'pid': pid},
            type: 'POST',
            success: function(data) {
                let result = data.toLowerCase() === 'true';
                can_dict[`${eid}${pid}`] = result;
                resolve(result);
            },
            error: function(err) {
                reject(false);
            }
      });
    });
}