function csrfSafeMethod(method) {
  // these HTTP methods do not require CSRF protection
  return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}

function delete_skill(e){
  var csrftoken = Cookies.get('csrftoken');
  var receiver = $(this);
  $.ajax({
    type: 'post',
    url: receiver.data('url'),
    data: {'XCSRFToken': csrftoken, 'skill_pk': $(this).data('id')},
    beforeSend: function(xhr, settings) {
      if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
        xhr.setRequestHeader("X-CSRFToken", csrftoken);
      }
    },
    success: function(data){
      if(data.status === 'success'){
        receiver.closest('tr').remove();
        $('#messages-box').html(`<span style="width: 100%; text-align: center;" class='alert alert-success'>${data.message}</span>`);
        window.setTimeout(function(){ 
          $('#messages-box').fadeOut('700', function(){ $(this).remove()})
        }, 1000);
      }
      window.scrollTo(0, 0);
    }
  });
}

function confirm_skill(e){
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
        $('#messages-box').html(`<span style="width: 100%;" class='alert alert-success'>${data['message']}</span>`);
      }
      else{
        $('#messages-box').html(`<span style="width: 100%;" class='alert alert-danger'>${data['message']}</span>`);
      }
      window.setTimeout(function(){ 
        $('#messages-box').fadeOut('700', function(){ $(this).remove()})
      }, 1000);
      window.scrollTo(0, 0);
    }
  });
}

$().ready(function(){
  $('.confirmation-button').click(confirm_skill);
  $('.remove-skill-button').click(delete_skill);
});