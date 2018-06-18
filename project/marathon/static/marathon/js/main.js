
function csrfSafeMethod(method) {
  // these HTTP methods do not require CSRF protection
  return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}

function manageRequestAjax(e){
  var csrftoken = Cookies.get('csrftoken');
  $.post({
    url: $(e.target).data('url'),
    data: {'XCSRFToken': csrftoken, 'action': $(e.target).data('action')},
    beforeSend: function(xhr, settings) {
      if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
        xhr.setRequestHeader("X-CSRFToken", csrftoken);
      }
    },
    dataType: 'json',
    success: function(data){
      $(e.target).closest('li').remove()
    }
  });
}

$().ready(function(){
  $('.request-button').each(function(index, element){
    $(this).click(manageRequestAjax);
  });
});