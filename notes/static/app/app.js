function getCookie(name) {
    var value = "; " + document.cookie;
    var parts = value.split("; " + name + "=");
    if (parts.length === 2) return parts.pop().split(";").shift();
  }
  











$(document).ready( function() {
    $.ajaxSetup({cache: false});

  
    console.log('app.js loaded!');


    //var div = $('#top');
    //var autoHeight = div.css('height', 'auto').height();

    function updateBackground(background) {

        var csrfToken = getCookie('csrftoken'); // Using jQuery

        $.ajax({
            type: 'POST',
            url: '/background/' + background + '/',
            data: { 'background': background},
            headers: { "X-CSRFToken": csrfToken },
            success: function(response) {
                console.log('Background saved successfully.');
            }, 
            error: function(error) {
                console.error('An error occurred while saving the background.')
            }, 
        }); 



    }



    function updateFolder(){
        var newtitle  = $('#newtitle').val();
        console.log(newtitle);
 
        var csrfToken = getCookie('csrftoken'); 

        $.ajax({
            type: 'POST',
            url: './rename_folder/', 
            data: { 'title': newtitle},
            headers: { "X-CSRFToken": csrfToken },
            success: function(response) {
                console.log('Folder renamed successfully.');
                $('#folderTitle').text(newtitle);
                $('#newtitle').val('');
            }, 
            error: function(error) {
                console.error('An error occurred while renaming the folder.')
            }
            


        }); 


    }


    function updateAccount() {
        var username = $('#username').val();
        var email = $('#email').val();
        var firstName = $('#first_name').val();
        var lastName = $('#last_name').val();
        var csrfToken = getCookie('csrftoken');

        $.ajax({
            type: 'POST', 
            url: '/update_account/',
            data: { 'username': username, 'email': email, 'first_name': firstName, 'last_name': lastName },
            headers: { "X-CSRFToken": csrfToken },
            success: function(response) {
                console.log('Account updated successfully.');
                var modal = $('#accountUpdateSuccess'); 
                modal.modal('show');

            }, 
            error: function(error) {
                console.error('An error occurred while updating the account.')
            },
        });
    }

    

    $('#updateAccountButton').on('click', function(event) {
        updateAccount();
    }); 


    $('#renameFolderButton').on('click', function(event) {
        updateFolder(); 
       
    }); 

    // Font change event handler
    $('#font-select').change(function() {
        var selectedFont = $(this).val();
        $('#textbox').css('font-family', selectedFont);
        $('#font-select').css('font-family', selectedFont);
    });
    
    // Font change event handler
    $('#fontSize-select').change(function() {
        var selectedFontSize = $(this).val();
        $('#textbox').css('font-size', selectedFontSize + 'px');
  
    });
    
    $('.card').on('mouseenter', function() {
        $(this).addClass('shadow-lg').css('cursor', 'pointer');
    }); 
    $('.card').on('mouseleave', function() {
        $(this).removeClass('shadow-lg');
    }); 

    $('.webSection').on('mouseenter', function() {
        $(this).addClass('shadow-lg');
    }); 
    $('.webSection').on('mouseleave', function() {
        $(this).removeClass('shadow-lg');
    }); 

    $('#wavy').on('click', function() {
        $('body').css('background-image', 'url("' + wavy +'")');
        updateBackground('wavy');
        console.log("done")
    }); 

    $('#hex').on('click', function() {
        $('body').css('background-image', 'url("' + hex +'")');
        updateBackground('hex');
    });
    
    $('#polyGrid').on('click', function() {
        $('body').css('background-image', 'url("' + polyGrid +'")');
        updateBackground('polygrid');
    }); 
    
    $('#circles').on('click', function() {
        $('body').css('background-image', 'url("' + circles +'")');
        updateBackground('cicles');
    }); 

    $('#blob').on('click', function() {
        $('body').css('background-image', 'url("' + blob +'")');
        updateBackground('blob');
    }); 

    $('#wavy-pink').on('click', function() {
        $('body').css('background-image', 'url("' + wavypink +'")');
        updateBackground('wavypink');
    }); 

    $('#retro').on('click', function() {
        $('body').css('background-image', 'url("' + retro +'")');
        updateBackground('retro');
    });
    
    $('#wavy-orange').on('click', function() {
        $('body').css('background-image', 'url("' + wavyorange +'")');
        updateBackground('wavyorange');
    }); 
   
    


});
