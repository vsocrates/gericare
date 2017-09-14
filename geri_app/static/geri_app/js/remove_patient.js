function remove_patient(ptID){
	var csrftoken = getCookie('csrftoken');

	console.log("csrftoken", csrftoken);
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

    // console.log("done sending that");

    $.ajax({
        url : '/removept/',
        type : "POST",
        data : {id : ptID}
    }).done(function(returned_data){
        // console.log("no idea: ", returned_data);
        // This is the ajax.done() method, where you can fire events after the ajax method is complete 

        // For instance, you could hide/display your add/remove button here

    });
}