

$(document).ready( function() {

    
    console.log('app.js loaded!');

    //Preparing the 'Experience the magic today' text animation
    let magic = document.querySelector('#magic');
    let strmagic = magic.textContent;
    let splitmagic = strmagic.split("");
    magic.textContent = "";
    for(let i=0; i < splitmagic.length; i++) {
        magic.innerHTML += "<span class = 'magic'>" + splitmagic[i] + "</span>";

    }

    //Preparing the 'Reimagined' text animation
    let imagine = document.querySelector('#reimagined');
    let strImagine = imagine.textContent;
    let splitImagine = strImagine.split("");
    imagine.textContent = "";
    for(let i=0; i < splitImagine.length; i++) {
        imagine.innerHTML += "<span class = 'reimagined'>" + splitImagine[i] + "</span>";
    }

    let char = 0;
    let time = setInterval(blueIn, 70);

    function blueIn() {
        const span = imagine.querySelectorAll('span')[char];
        span.classList.add('fadeIn');
        span.classList.remove('fadeOut')
        char++; 
        if(char === splitImagine.length) {
            char = 0; 
            clearInterval(time);
            time = setInterval(blueOut, 80);
            return; 
        }
    }

    function blueOut() {
        const span = imagine.querySelectorAll('span')[char];
        span.classList.add('fadeOut');
        span.classList.remove('fadeIn');
        char++; 
        if(char === splitImagine.length) {
            char = 0;
            clearInterval(time);
            time = setInterval(blueIn, 80);
            return; 
        }
    }




    //Simply Elegant text fadeIn animation
    var reveal =  $('#simpleandelegant').animate({opacity: '1'}, 2000);



    

    $.when(reveal).done(function() {
        $('#signupbutton').animate({opacity: '1'}, 2500);

        
        ///finishing the 'Experience the magic today' text animation
        let char = 0;
        let appear = setInterval(onTick, 50);

        function onTick() {
            const span = magic.querySelectorAll('span')[char];
            span.classList.add('fadeIn');
            char++
            if(char === splitmagic.length) {
                complete();
                return;
            }
        }
        function complete() {
            clearInterval(appear);
            appear = null; 
        }
    

    }); 


});
