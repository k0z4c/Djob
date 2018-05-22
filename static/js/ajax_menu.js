// function fetchFriendship(){
//     $.ajax({
//       url:  $('#friendship-badge').data('url'),
//       error: function(jqXHR, textStatus, errorTrown){
//         console.log(textStatus);
//         console.log(errorTrown);
//       },
//       datatype: 'json',
//       success: function(data){
//         $('#friendship-badge').html(data.unread_notifications);
//         if(data.unread_notifications > 0){
//           $('#friendship-badge').html(data.unread_notifications);
//           $('#friendship-badge').css('visibility', 'visible');
//         }
//         setTimeout(fetchFriendship,1000);
//       }
//     });
//   }

// function fetchFriendshipList(){
//   $.ajax({
//     // url = {% url messanger:ajax_unreaded_count %}
//     url: $('#friendship-request-list').data('url'),
//     datatype: 'json',
//     success: function(data){
//       notifications = '';
//       for (let k of Object.keys(data)){
//         notifications += '<li class="px-auto dropdown-item">' + 
//           `<img class="img-thumbnail rounded img-fluid" src=${data[k][3]}/>` + 
//           `<a href=\"${data[k][2]}\"> ${data[k][0]} | ${formatDate(data[k][1])} </a>` +
//           '</li>';
//       }
//       $('#friendship-request-list').html(notifications);
//       setTimeout(fetchFriendshipList, 1000);
//     }
//   });
// }

// function fetchFriendshipList(){
//   $.ajax({
//     url: $('#friendship-request-list').data('url'),
//     datatype: 'json',
//     success: function(data){
//       data.unread_list.forEach(function(entry){
//         $('#friendship-request-list').append(`<a class="dropdown-item">${entry.description}</a>`);
//       });
//     }
//   });
// }

// function fetchUnreadedMessagesCount(){
//     $.ajax({
//       url:  $('#messanger-badge').data('url'),
//       error: function(jqXHR, textStatus, errorTrown){
//         console.log(textStatus);
//         console.log(errorTrown);
//       },
//       datatype: 'json',
//       success: function(data){
//         if(data.unreaded_count > 0){
//           $('#messanger-badge').html(data.unreaded_count);
//           $('#messanger-badge').css('visibility', 'visible');
//         }
//         setTimeout(fetchUnreadedMessagesCount,1000);
//       }
//     });
//   }


// function formatDate(date){
//   var d = new Date(date);
//   return d.getFullYear() + '/' + d.getMonth() + '/' + d.getDay()
// }

// $().ready(function(){
//   $('#friendship-dropdown').click(fetchFriendshipList);
// });
// $(document).ready(function(){setTimeout(fetchFriendship, 1000);});
// $(document).ready(function(){setTimeout(fetchFriendshipList, 1000);});
// $(document).ready(function(){setTimeout(fetchUnreadedMessagesCount, 1000);});

