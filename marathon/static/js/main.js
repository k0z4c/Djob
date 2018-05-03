function fetchData(){
    $.ajax({
      url:  $('#mydiv').data('url'),
      error: function(jqXHR, textStatus, errorTrown){
        console.log(textStatus);
        console.log(errorTrown);
      },
      datatype: 'json',
      success: function(data){
        $('#{{label}}_unread').data('url')
        $('#{{label}}_unread').html(data.unread);

        if(data.unread > 0){
          $('#{{label}}_unread').html(data.unread);
          $('#{{label}}_unread').css('visibility', 'visible');
        }
        setTimeout(fetchData,1000);
      }
    });
  }
