
function getCookie(name) {
  var value = "; " + document.cookie;
  var parts = value.split("; " + name + "=");
  if (parts.length === 2) return parts.pop().split(";").shift();
}





$(document).ready( function() {

  
    console.log('note.js loaded!');



    function saveNote() {
      
      var noteText = $('#textbox').val();
      var fontSize = $('#fontSize-select').val();
      var fontFamily = $('#font-select').val();

      //Only update the saved note if something has been modefied. Otherwise, we return to 
      //avoid unnecessary calls to the server.
      if(noteText === lastText && fontSize === lastSize && fontFamily === lastFont) {
        return;
      }

      $('#saveMessage').text('Saving Note ...'); 

      var csrfToken = getCookie('csrftoken'); // Using jQuery

      
      $.ajax({
        type: 'POST',
        url: './save_note/',
        data: { 'text': noteText, 'font': fontFamily, 'fontSize': fontSize},
        headers: { "X-CSRFToken": csrfToken },
        success: function(response) {

          ////update the lastest saved version of the note
          lastText = noteText;
          lastSize = fontSize;
          lastFont = fontFamily; 
          
          $('#saveMessage').text('Note Saved to the Cloud!');
       

         
        },
        error: function(error) {
          console.error('An error occurred while saving the note.');
        }
      });

      

    }
    
    // Autosave the note every 5 seconds (adjust the interval as needed)
    var lastText = $('#textbox').val();
    var lastSize = $('#fontSize-select').val();
    var lastFont = $('#font-select').val();
    setInterval(saveNote, 4000);


    $('#shareNote').on('click', function() {
        var user = $('#username').val();
        $('#username').val('');
        var csrfToken = getCookie('csrftoken'); // Using jQuery

        $.ajax({
            type: 'POST',
            url: './share_note/',
            data: { 'username': user},
            headers: { "X-CSRFToken": csrfToken },
            success: function(response) {
                console.log('Note shared successfully.');
            }, 
            error: function(error) {
              console.error('An error occurred while sharing the note.'); 
            }

        });




    }); 


    
    


});
