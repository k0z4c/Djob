function add_friend(e){
  function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
  }

  var csrftoken = Cookies.get('csrftoken');
  $.post({
    url: $('#add-friend-button').data('url'),
    data: {'XCSRFToken': csrftoken},
    beforeSend: function(xhr, settings) {
      if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
        xhr.setRequestHeader("X-CSRFToken", csrftoken);
      }
    },
    dataType: 'json',
    success: function(data){
      $('#messages-box').html(`<span style="text-align: center; width: 100%;" class="alert alert-success">${data.message}</span>`);
      $('#add-friend-button').prop("disabled", true);
      $('#add-friend-button').html(data.message);
    }
  });
}

$().ready(function(){
  $("#add-friend-button").click(add_friend);
}); 