function getCookie(name) {
    var value = "; " + document.cookie;
    var parts = value.split("; " + name + "=");
    if (parts.length === 2) return parts.pop().split(";").shift();
  }
  



$(document).ready( function() {
    $.ajaxSetup({cache: false});

  
    console.log('app.js loaded!');

    //masonary configuration
    var masonryContainer = document.querySelector('.masonry-container');
    var masonry = new Masonry(masonryContainer, {
    itemSelector: '.masonry-card',
    columnWidth: '.masonry-card',
    gutter: 0, // Adjust as needed
    });

    try{
        var myModal = new bootstrap.Modal(document.getElementById('welcomeModal'), {
            keyboard: false
        })
        myModal.show(); 
    } catch(err) {
        console.log("welcome modal not found");
    }




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


    ///This function updates the Folder title
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


    function updateNote() {
        var newtitle  = $('#newNoteTitle').val();

        var csrfToken = getCookie('csrftoken');
        console.log(newtitle)
        $.ajax({
            type: 'POST',
            url: './rename_note/', 
            data: {'title': newtitle},
            headers: { "X-CSRFToken": csrfToken },
            success: function(response) {
                console.log('Note renamed successfully.');
                $('#noteTitle').text(newtitle);
                $('#newtitle').val('');
            }, 
            error: function(error) {
                console.error('An error occurred while renaming the note.')
            }
            


        }); 


    }

    ///This function updates the Account information
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
                console.log(response['success']);
                if (response['success']) {
                    console.log('Account updated successfully.');
                    var modal = $('#accountUpdateSuccess'); 
                    modal.modal('show');

                    $('#accountName').text(username);

                }
                else {
                    var modal = $('#accountUpdateError');
                    modal.modal('show');
                }

            }, 
            error: function(error) {
                console.log('An error occurred while updating the account.')
            },
        });
    }


    $('#newNoteTitle').keyup(function(event) {
        if (event.keyCode === 13) {
            event.preventDefault();
            $('#renameNoteButton').click(); 
            $('#noteTitle').click();
        }
    });

    $('#newtitle').keyup(function(event) {
        if (event.keyCode === 13) {
            event.preventDefault();
            $('#renameFolderButton').click();
        }
    });

    

    
    ///welcome modal javascript
    var curr = 1; 
    $('#intronext').on('click', function(event) {
        if(curr === 4){
            myModal.hide();
        }

        $('#intro' + curr).css({display: 'none'}, 500);
        curr++;
        $('#intro' + curr).css({display: 'block'}, 500);

        if(curr === 4){
            $('#intronext').text('Finish');
            $('#introclose').css({display: 'none'});
        }
    });



    $('#updateAccountButton').on('click', function(event) {
        updateAccount();
    }); 


    $('#renameFolderButton').on('click', function(event) {
        updateFolder(); 
       
    }); 

    $('#renameNoteButton').on('click', function(event) {
        updateNote(); 
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


    ///change the background of the page
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
   



    ///section of code for dragging and dropping notes into folders
    const draggables = document.querySelectorAll('.draggable');
    const folders = document.querySelectorAll('.folder');

    draggables.forEach((draggable) => {
        draggable.addEventListener('dragstart', (e) => {
            e.dataTransfer.setData('itemID', e.target.getAttribute('data-item-id'));
        });
    });

    folders.forEach((folder) => {
        folder.addEventListener('dragover', (e) => {
            e.preventDefault();
            folder.classList.add('dragover');
            
        });

        folder.addEventListener('dragleave', () => {
            folder.classList.remove('dragover');
        });

        folder.addEventListener('drop', (e) => {
            e.preventDefault();

            
            //remove the black outline hover hightlight
            folder.classList.remove('dragover');

            const itemID = e.dataTransfer.getData('itemID');
            const folderID = folder.getAttribute('data-folder-id');
            var csrfToken = getCookie('csrftoken');
            
            var path = window.location.pathname;
            var pathArray = path.split('/');
            if(pathArray[2] === folderID){
                return;
            }

            // Send an AJAX request to update the database
            $.ajax({
                type: 'POST', 
                url: '/updateNoteFolder/',
                data: {'noteID': itemID, 'folderID': folderID},
                headers: { "X-CSRFToken": csrfToken },
                ///on success, remove the note from the page
                success: function(response) {
                    const item = document.querySelector('#note' + itemID);
                    item.remove();

                    //resets the masonry layout
                    masonry.layout();
                }, 
                error: function(error) {
                    console.error('An error occurred while updating the account.')
                },
            }); 

        });
    });

    


});
