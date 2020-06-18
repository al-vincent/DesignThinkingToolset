"use strict";

// AFAIK, the *only* way to do the resize correctly is to use variables with 
// global scope :-(  
// [Could potentially use sessionStorage or similar, but that's surely overkill]
let startWidth = 0, startHeight = 0;

window.onload = function() {    
    // get the contents of the JSON config file
    const CONFIG = JSON.parse(document.getElementById("config-id").textContent);

    // load the image selected by the user in step 1
    previewImage(CONFIG.HTML.APP.IMAGE_PANE.IMAGE.ID, 
        CONFIG.HTML.APP.IMAGE_PANE.IMAGE.FILE_DATA_KEY,
        CONFIG.HTML.APP.IMAGE_PANE.IMAGE.FILE_NAME_KEY);
    
    const IMG = document.getElementById(CONFIG.HTML.APP.IMAGE_PANE.IMAGE.ID);
    const svg = createSvg(CONFIG.HTML.APP.IMAGE_PANE.CONTAINER.ID, 
        IMG.clientWidth, 
        IMG.clientHeight);

    startWidth = IMG.clientWidth;
    startHeight = IMG.clientHeight;
    
    // add click events to buttons
    addClickEventsToButtons(CONFIG);       
}

window.onresize  = function() {
    const CONFIG = JSON.parse(document.getElementById("config-id").textContent);
    const REGION_GRP = CONFIG.CONSTANTS.CLASSES.REGION;
    const IMG = document.getElementById(CONFIG.HTML.APP.IMAGE_PANE.IMAGE.ID);
    
    console.log("Resizing window: height=" + $(window).height() + ", width=" + $(window).width());
    // get the current data (i.e. x,y,width,height all using image coords)
    const data = d3.selectAll("." + REGION_GRP).data();
    // rescale to put x,y,width,height on scale of [0,1]
    const rescaledData = rescaleDataToRelativeCoords(data, startWidth, startHeight);
    // remove the old SVGs
    d3.selectAll("svg").remove();
    // get the x,y,width,height vals for the new window size
    const newData = rescaleDataToAbsoluteCoords(rescaledData, IMG.clientWidth, IMG.clientHeight);
    // regenerate the SVG, image and resizable boxes
    const svg = createSvg(CONFIG.HTML.APP.IMAGE_PANE.CONTAINER.ID, 
        IMG.clientWidth, 
        IMG.clientHeight);
    createRegions(svg, newData);

    startWidth = IMG.clientWidth;
    startHeight = IMG.clientHeight;
}

function addClickEventsToButtons(config) {
    // Add click event to the Add Region button
    const addRgnBtn = document.getElementById(config.HTML.SET_REGIONS.ADD_REGION_BTN.ID);
    addRgnBtn.onclick = function() { clickAddRegion(); }    
}
