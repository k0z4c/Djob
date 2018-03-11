function fetchFriendship(){
    $.ajax({
      url:  $('#friendship-badge').data('url'),
      error: function(jqXHR, textStatus, errorTrown){
        console.log(textStatus);
        console.log(errorTrown);
      },
      datatype: 'json',
      success: function(data){
        $('#friendship-badge').html(data.unread_notifications);
        setTimeout(fetchFriendship,3000);
      }

    });
  }

  $(document).ready(function(){setTimeout(fetchFriendship, 3000);});