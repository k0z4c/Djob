
function confirm_skill(e){
  function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
  }
  var csrftoken = Cookies.get('csrftoken');
  console.log($(this).data('key'));
  $.ajax({
    type: 'post',
    url: $(this).data('url'),
    data: {'XCSRFToken': csrftoken, 'skill_pk': $(this).data('key') },
    beforeSend: function(xhr, settings) {
      if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
        xhr.setRequestHeader("X-CSRFToken", csrftoken);
      }
    },
    dataType: 'json',
    success: function(data){
      console.log("confirmation received");
    }
  });
}

$().ready(function(){
  $('.confirmation-button').click(confirm_skill);
});