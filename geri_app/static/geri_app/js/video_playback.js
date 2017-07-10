function open_in_new_window(id, new_page_title, features) {
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

        new_video.addEventListener("timeupdate", function(){
            if((this.currentTime/this.duration) >= VIDEO_COMPLETE_THRESHOLD) {
                    
                }
            });
    
    }
}