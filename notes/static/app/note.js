/**
 * @file This file contains the JavaScript code for the note-taking application.
 * It includes functions for handling user interactions, saving notes, and sharing notes.
 * The code uses the Quill library for rich text editing and the jQuery library for AJAX requests.
 * The file also includes comments explaining the purpose and functionality of each section of code.
 *
 * @see {@link https://quilljs.com/|Quill}
 * @see {@link https://jquery.com/|jQuery}
 */
// 

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


    ///keybindings for Quill. Description of the keybindings is as follows:
    var bindings = {
      /*
      CustomSubSeciton: creates a new subsection in the note. 
      */
      customSubSection: {
        key: 'S',
        shortKey: true,
        handler: function(range, context) {
          this.quill.format('bold', true);
          this.quill.format('color', '#0066cc');
          this.quill.format('header', 3);
        }
      }, 

      /*
      CustomClean: removes all formatting from the selected text.
      */
      customClean: {
        key: 'D', 
        shortKey: true,
        handler: function(range, context) {
          this.quill.format('bold', false);
          this.quill.format('color', '#000000');
          this.quill.format('underline', false);
          this.quill.format('strike', false);
          this.quill.format('italic', false);
          this.quill.format('header', false);
        }
      }, 

      /*
      CustomSubScript: creates a subscript for the selected text.
      */
      customSubScript:{
        key: 188,
        shortKey: true,
        handler: function(range, context) {
          if (quill.getFormat().script === 'sub') {
            this.quill.format('script', false);
          }
          else{
            this.quill.format('script', 'sub');
          }
        }
      }, 

      /*
      CustomSuperScript: creates a superscript for the selected text.
      */
      customSuperScript:{
        key: 190,
        shortKey: true,
        handler: function(range, context) {
          if (quill.getFormat().script === 'super') {
            this.quill.format('script', false);
          } 
          else {
            this.quill.format('script', 'super');
          }
        }
      }

    }

    var quill = new Quill('#textedit', {
      modules: {
        syntax: true,
        toolbar: toolbarOptions, 
        keyboard: {
          bindings: bindings
        }
      },
      placeholder: '   Jot something down...',
      theme: 'snow'  
    });

    quill.formatLine(0, 1, 'header', 1);

    

    /*  
    For some reason, we cannot get custom keybindinds to work with Quill. 
    We have tried the following:
      Using the syntax in the Quill documentation
      Looking at the source code in the Github repo
      Trying keybindings with things that already work - like Bold 
      Worked on it some in the Quill Playground - couldn't even get it to work there (but could do some more)
    */
 




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



  function downloadPDF() {
    var title = $('#noteTitle').html();
    var text = $('#textedit').html(); 
    var doc = new jsPDF();
    doc.fromHTML(title, 15, 15, {'width': 170});
    doc.fromHTML(text, 15, 40, {
      'width': 170,
    });    
    doc.save($('#noteTitle').text() + '.pdf');
  }

  $('#downloadPDF').on('click', downloadPDF); 

});
