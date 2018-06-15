function localizeDatesJSON(sel, key){ 
  sel.each(function(index, element){
      var obj;
      var date;
      obj = JSON.parse($(element).html());
      if(obj[key] != undefined){
          date = new Date(obj[key]);
          $(element).html(date.toLocaleString());
      } else {
          $(this).html('not readed yet')
      }
      $(element).css('visibility', 'visible');
      return;
  });
}
