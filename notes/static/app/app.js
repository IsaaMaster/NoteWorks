

















$(document).ready( function() {

  
    console.log('app.js loaded!');


    //var div = $('#top');
    //var autoHeight = div.css('height', 'auto').height();



    

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
    }); 

    $('#hex').on('click', function() {
        $('body').css('background-image', 'url("' + hex +'")');
    });
    
    $('#polyGrid').on('click', function() {
        $('body').css('background-image', 'url("' + polyGrid +'")');
    }); 
    $('#circles').on('click', function() {
        $('body').css('background-image', 'url("' + circles +'")');
    }); 
    


});
