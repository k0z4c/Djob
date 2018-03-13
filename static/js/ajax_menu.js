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

function formatDate(date){
  var d = new Date(date);
  return d.getFullYear() + '/' + d.getMonth() + '/' + d.getDay()
}

function fetchFriendshipList(){
  $.ajax({
    url: $('#friendship-request-list').data('url'),
    datatype: 'json',
    success: function(data){
      notifications = '';
      for (let k of Object.keys(data)){
        notifications += '<li class="dropdown-item">' + 
          `<a href=\"${data[k][2]}\"> ${data[k][0]} ${formatDate(data[k][1])} </a>` +
          '</li>';
      }
      $('#friendship-request-list').html(notifications);
      setTimeout(fetchFriendshipList, 3000);
    }
  });
}

$(document).ready(function(){setTimeout(fetchFriendship, 3000);});
$(document).ready(function(){setTimeout(fetchFriendshipList, 3000);});

