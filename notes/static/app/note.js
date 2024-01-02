
function getCookie(name) {
  var value = "; " + document.cookie;
  var parts = value.split("; " + name + "=");
  if (parts.length === 2) return parts.pop().split(";").shift();
}





$(document).ready( function() {

  
    console.log('note.js loaded!');

    var Delta = Quill.import('delta');

    var toolbarOptions = [
      [{ 'header': [1, 2, 3, 4, 5, 6, false] }, { 'font': [] }],
      
      ['bold', 'italic', 'underline', 'strike'],    
      [{ 'color': [] }, { 'background': [] }],  
      // toggled buttons
      ['code-block', 'blockquote'],
  
      [{ 'list': 'ordered'}, { 'list': 'bullet' }],
      [{ 'script': 'sub'}, { 'script': 'super' }],      // superscript/subscript
      [{ 'indent': '-1'}, { 'indent': '+1' }, { 'align': [] }],          // outdent/indent
    
      ['link'],
      
      ['formula', 'clean']
                           
    ];

    hljs.configure({   // optionally configure hljs
      languages: ['javascript', 'java', 'python']
    });

    var quill = new Quill('#textedit', {
      modules: {
        syntax: true,
        toolbar: toolbarOptions, 
      },
      placeholder: '   Jot something down...',
      theme: 'snow'  
    });

    quill.formatLine(0, 1, 'header', 1);

 




    //get the contents of the note from the server
    $.ajax({
      type: 'GET',
      url: './get_note_contents/',
      success: function(response) {
        var content = JSON.parse(response['text']);
        quill.setContents(content);
      },
    })

    
    // Store accumulated changes
    var change = new Delta();
    quill.on('text-change', function(delta) {
      change = change.compose(delta);
    });



    // Save periodically
    setInterval(function() {
      if (change.length() > 0) {
        console.log('Saving changes', change);

       // Get the CSRF token from the cookie (you may need to adjust this based on your setup)
      var csrftoken = getCookie('csrftoken');

      // Include the CSRF token in the headers of the AJAX request
      $.ajax({
        url: './new_save_note/',
        type: 'POST',
        headers: {
          'X-CSRFToken': csrftoken
        },
        data: {
          'text': JSON.stringify(quill.getContents())
        },
        success: function(response) {
          console.log('Save successful', response);
        },
        error: function(error) {
          console.error('Error saving changes', error);
        }
      });

        change = new Delta();
      }
    }, 2.5*1000);

    

    /*
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
    */

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

    $('#downloadPDF').on('click', function() {
      var html = $('#textedit').html(); 
      var doc = new jsPDF();
      doc.setFont('sans-serif');
      doc.fromHTML(html, 15, 15, {
        'width': 170,
      });    
      doc.save($('#noteTitle').text() + '.pdf');
    }); 




    
    


});
