"use strict";


window.onload = function() {
    // get the contents of the JSON config file
    const CONFIG = JSON.parse(document.getElementById("config-id").textContent);
    const FILE_KEY = CONFIG.HTML.HOME.IMAGE_PANE.FILE_STORE_KEY;    

    previewImage(CONFIG.HTML.APP.IMAGE_PANE.ID, FILE_KEY);
}

