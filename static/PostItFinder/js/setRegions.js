"use strict";


window.onload = function() {
    // get the contents of the JSON config file
    const CONFIG = JSON.parse(document.getElementById("config-id").textContent);

    previewImage(CONFIG.HTML.APP.IMAGE_PANE.ID, 
        CONFIG.HTML.HOME.IMAGE_PANE.FILE_DATA_KEY,
        CONFIG.HTML.HOME.IMAGE_PANE.FILE_NAME_KEY);
}

