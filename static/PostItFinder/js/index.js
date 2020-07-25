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
}