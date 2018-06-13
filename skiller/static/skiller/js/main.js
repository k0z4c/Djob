
function confirm_skill(e){
  function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
  }
  var csrftoken = Cookies.get('csrftoken');
  var receiver = $(this)
  $.ajax({
    type: 'post',
    url: receiver.data('url'),
    data: {'XCSRFToken': csrftoken, 'skill_pk': receiver.data('key') },
    beforeSend: function(xhr, settings) {
      if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
        xhr.setRequestHeader("X-CSRFToken", csrftoken);
      }
    },
    dataType: 'json',
    success: function(data){
      console.log(data['message']);
      if(data['status'] === 'success'){
        console.log("success");
        $('#confirmation-box').html(`<span style="width: 100%;" class='alert alert-success'>${data['message']}</span>`);
      }
      else{
        $('#confirmation-box').html(`<span style="width: 100%;" class='alert alert-danger'>${data['message']}</span>`);
      }
      window.scrollTo(0, 0)
    }
  });
}

$().ready(function(){
  $('.confirmation-button').click(confirm_skill);
});