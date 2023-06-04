$(document).ready( function() {
    
    
    //font type options
    $('#TimesNewRoman').on('click', () => {
        $('#textbox').css('font-family', 'Times New Roman');
        $('#fontButton').text('Times New Roman');
    }); 

    $('#Helvetica').on('click', () => {
        $('#textbox').css('font-family', 'Helvetica');
        $('#fontButton').text('Helvetica');
    }); 



    $('#Georgia').on('click', () => {
        $('#textbox').css('font-family', 'Georgia');
        $('#fontButton').text('Georgia');
    }); 



    ///font size options
    $('#10').on('click', () => {
        $('#textbox').css('font-size', '13px');
        $('#fontSizeButton').text('10px');
    }); 

    $('#12').on('click', () => {
        $('#textbox').css('font-size', '16px');
        $('#fontSizeButton').text('12px');
    }); 

    $('#14').on('click', () => {
        $('#textbox').css('font-size', '19px');
        $('#fontSizeButton').text('14px');
    }); 

    $('#18').on('click', () => {
        $('#textbox').css('font-size', '24px');
        $('#fontSizeButton').text('18px');
    }); 

    $('#24').on('click', () => {
        $('#textbox').css('font-size', '32px');
        $('#fontSizeButton').text('24px');
    }); 

    $('#30').on('click', () => {
        $('#textbox').css('font-size', '40px');
        $('#fontSizeButton').text('30px');
    }); 






});
