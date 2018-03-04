function myFunction(target){
    console.log('event fired!');
    var url = $(target).attr('data-remove-url');
    var data = $(target).attr('data-friendship');
    console.log(url)
    $.ajax({
        type: 'POST',
        beforeSend: function(request){
            request.setRequestHeader('X-CSRFToken', Cookies.get('csrftoken'))
        },
        url: url,
        data: {
            'X-CSRFToken': Cookies.get('csrftoken'),
            'data': data,
        },
        dataType: 'json',
        success: function(data){
            console.log(data.msg)
            // must bid the entry from the page
            $(target).closest('li').remove()
        }
    });
};
