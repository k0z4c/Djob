function FetchUnreadedNotificationsCount(target, key){
  $.ajax({
    url: target.data('url'),
    datatype: 'json',
    error: function(jqXHR, textStatus, errorTrown){
             console.log(textStatus);
             console.log(errorTrown);
           },
    success: function(data){
      if(data[key] !== 0){
        target.html(data[key]);
        target.css('visibility', 'visible');
      }
      else{
        target.css('visibility', 'hidden');
      }
    }
  });
  setTimeout(FetchUnreadedNotificationsCount, 1500, target, key);
}

$().ready(function(){
  setTimeout(FetchUnreadedNotificationsCount, 1500, $('#notifications-badge'), 'unread_count');
  setTimeout(FetchUnreadedNotificationsCount, 1500, $('#messanger-badge'), 'unreaded_count');

  $('[data-toggle="tooltip"]').tooltip()
});
