"use strict"

window.onload = function() {    
    // get the contents of the JSON config file
    const CONFIG = JSON.parse(document.getElementById("config-id").textContent);
    const startBtn = document.getElementById(CONFIG.HTML.HOME.START_BTN.ID);
    startBtn.onclick = function() {
        if(!navigator.cookieEnabled) {
            alert("This site requires cookies to work. Please enable them in your browser and try again");
            return false; 
        }
        else {
            return true;
        }
    }

    const spans = document.querySelectorAll('.word span');
    spans.forEach((span, idx) => {
        span.addEventListener('mouseover', (e) => {
            e.target.classList.add('active');
        });
        span.addEventListener('animationend', (e) => {
            e.target.classList.remove('active');
        });
        
        // Initial animation
        setTimeout(() => {
            span.classList.add('active');
        }, 750 * (idx+1))
    });
}
