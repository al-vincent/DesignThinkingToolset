"use strict";


window.onload = function() {
    // get the contents of the JSON config file
    const CONFIG = JSON.parse(document.getElementById("config-id").textContent);

    // load the image selected by the user in step 1
    previewImage(CONFIG.HTML.APP.IMAGE_PANE.IMAGE.ID, 
        CONFIG.HTML.APP.IMAGE_PANE.IMAGE.FILE_DATA_KEY,
        CONFIG.HTML.APP.IMAGE_PANE.IMAGE.FILE_NAME_KEY);
    
    const img = document.getElementById(CONFIG.HTML.APP.IMAGE_PANE.IMAGE.ID);
    const svg = createSvg(CONFIG.HTML.APP.IMAGE_PANE.CONTAINER.ID, 
        img.clientWidth, 
        img.clientHeight);    
    
    IMAGE_WIDTH = img.clientWidth;
    IMAGE_HEIGHT = img.clientHeight;
    console.log("clientWidth: " + img.clientWidth + ", clientHeight: " + img.clientHeight);

    // add click events to buttons
    const addRgnBtn = document.getElementById(CONFIG.HTML.SET_REGIONS.ADD_REGION_BTN.ID);
    addRgnBtn.onclick = function() {
        clickAddRegion();
    }
}

