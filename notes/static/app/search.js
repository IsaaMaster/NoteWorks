


///javascript to manage search functionality in the navbar used across the website

function getCookie(name) {
    var value = "; " + document.cookie;
    var parts = value.split("; " + name + "=");
    if (parts.length === 2) return parts.pop().split(";").shift();
  }
  
  

$(document).ready( function() {
    console.log('search.js loaded!');


    function updateSearchSuggestions(notes, folders) {
        $('#noteSuggestions').empty();
        for (let i = 0; i < notes.length; i++) {

            $('#noteSuggestions').append(`
            <a href="/note/${notes[i]['id']}/" class="text-decoration-none text-dark">
                <div class = "row mb-3 searchSuggestion">
                    <div class = "col-6">
                        <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" fill="currentColor" class="bi bi-file-earmark" viewBox="0 0 16 16">
                            <path d="M14 4.5V14a2 2 0 0 1-2 2H4a2 2 0 0 1-2-2V2a2 2 0 0 1 2-2h5.5zm-3 0A1.5 1.5 0 0 1 9.5 3V1H4a1 1 0 0 0-1 1v12a1 1 0 0 0 1 1h8a1 1 0 0 0 1-1V4.5z"/>
                        </svg>
                        ${notes[i]['title']}
                    </div>
                    <div class="col-6 text-end text-secondary">
                        Last Opened ${notes[i]['time']}
                    </div>
                </div>
            </a>
            ` );
        }
        if (notes.length === 0) {
            $('#noteSuggestions').append(`
                <div class = "mb-3 text-secondary">No notes match your search &#128542</div>
            `);
        }


        $('#folderSuggestions').empty();
        for (let i = 0; i < folders.length; i++) {

            $('#folderSuggestions').append(`
            <a href="/notes/${folders[i]['id']}/" class="text-decoration-none text-dark">
                <div class = "row mb-3 searchSuggestion">
                    <div class = "col-6">
                        <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" fill="currentColor" class="bi bi-folder" viewBox="0 0 16 16">
                            <path d="M.54 3.87.5 3a2 2 0 0 1 2-2h3.672a2 2 0 0 1 1.414.586l.828.828A2 2 0 0 0 9.828 3h3.982a2 2 0 0 1 1.992 2.181l-.637 7A2 2 0 0 1 13.174 14H2.826a2 2 0 0 1-1.991-1.819l-.637-7a1.99 1.99 0 0 1 .342-1.31zM2.19 4a1 1 0 0 0-.996 1.09l.637 7a1 1 0 0 0 .995.91h10.348a1 1 0 0 0 .995-.91l.637-7A1 1 0 0 0 13.81 4H2.19zm4.69-1.707A1 1 0 0 0 6.172 2H2.5a1 1 0 0 0-1 .981l.006.139C1.72 3.042 1.95 3 2.19 3h5.396l-.707-.707z"/>
                        </svg>
                        ${folders[i]['title']}
                    </div>

                </div>
            </a>
            ` );
        }
        if (folders.length === 0) {
            $('#folderSuggestions').append(`
                <div class = "mb-3 text-secondary">No folders match your search &#128542</div>
            `);
        }
    }



    function getSearchSuggestions(keyword){
        var csrfToken = getCookie('csrftoken');
        $.ajax({
            type: 'GET',
            url: '/searchSuggestions/',
            data: { 'keyword': keyword},
            headers: { "X-CSRFToken": csrfToken },
            success: function(response) {
                if (response['success']) {
                    console.log('Search suggestions retrieved successfully.');
                    updateSearchSuggestions(response['notes'], response['folders'])
                }
                else {
                    console.log('An error occurred while retrieving search suggestions.')
                }

            }, 
            error: function(error) {
                console.log('An error occurred while retrieving search suggestions')
            },
        });
    }


    
    $('#searchModal').on('shown.bs.modal', function() {
        $('#searchInput').val('');
        $('#searchInput').focus();
        getSearchSuggestions($('#searchInput').val()); 
    });

    $('#searchInput').keyup(function(event) {
        getSearchSuggestions($('#searchInput').val()); 
    });




}); 