function can(eid, pid) {
    return new Promise(function(resolve, reject) {
        $.ajax({
            url: '/permissions/can',
            data: {'eid': eid, 'pid': pid},
            type: 'POST',
            success: function(data) {
                let result = data.toLowerCase() === 'true';
                resolve(result);
            },
            error: function(err) {
                reject(false);
            }
      });
    });
}