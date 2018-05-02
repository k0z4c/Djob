function localizeDatesJSON(sel, key){ 
                sel.each(function(index, element){
                    var obj;
                    var date;
                    obj = JSON.parse($(this).html());
                    if(obj[key] != undefined){
                        date = new Date(obj[key]);
                        $(this).html(date.toLocaleString());
                    } else {
                        sel.html('not readed yet')
                    }
                    $(this).css('visibility', 'visible');
                    return;
                });
            }