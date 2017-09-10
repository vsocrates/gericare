function open_in_new_window(id, new_page_title, features, vidID) {
    var VIDEO_COMPLETE_THRESHOLD = 0.90;

    console.log('make it here');

    var new_window;

    if(features !== undefined && features !== '') {
        new_window = window.open('', '_blank', features);
    }
    else {
        new_window = window.open('', '_blank');
    }

    var html_contents = document.getElementById(id);
    if(html_contents !== null) {
        new_window.document.write('<!doctype html><html><head><title>' + new_page_title + '</title><meta charset="UTF-8" /></head><body>' + html_contents.innerHTML + '</body></html>');
        console.log(new_window.document.getElementById('test'))
        var new_video = new_window.document.getElementById('test');
        new_video.autoplay = true;
        new_video.addEventListener("timeupdate", (handler = function(){
            if((this.currentTime/this.duration) >= VIDEO_COMPLETE_THRESHOLD) {
                    new_video.removeEventListener("timeupdate", handler);

                    var csrftoken = getCookie('csrftoken');

                    function csrfSafeMethod(method) {
                        // these HTTP methods do not require CSRF protection
                        return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
                    }

                    $.ajaxSetup({
                        beforeSend: function(xhr, settings) {
                            if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                                xhr.setRequestHeader("X-CSRFToken", csrftoken);
                                console.log('center');
                            }
                        }
                    });

                    console.log("done sending that");

                    $.ajax({
                        url : '/seenvideo/',
                        type : "POST",
                        data : { id : vidID, seen: true}
                    }).done(function(returned_data){
                        console.log("no idea: ", returned_data);
                        // This is the ajax.done() method, where you can fire events after the ajax method is complete 

                        // For instance, you could hide/display your add/remove button here

                    });

                    // var f = document.createElement("form");
                    // f.setAttribute('method',"post");
                    // f.setAttribute('action',"/seenvideo/");

                    // var i = document.createElement("input"); //input element, text
                    // i.setAttribute('type',"hidden");
                    // i.setAttribute('name',"seenVideo");
                    // i.setAttribute('value', "True");

                    // f.appendChild(i);

                    // document.body.appendChild(f);

                    // console.log("form: ", f);
                    // f.submit();

                    

//                    <input type='hidden' name='csrfmiddlewaretoken' value='DptZcEU8N9KoSHLXucGEpwdcX2hL8bgE3w5KSdzV86sOaVeEtQQRIsGqsOivkbsh' />

                }
            }));
    
    }
}

// using jQuery
function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}