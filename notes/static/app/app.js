$(document).ready( function() {

    console.log('app.js loaded!');
    

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
        
      


});
