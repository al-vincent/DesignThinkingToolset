"use strict";


// AFAIK, the *only* way to do the resize correctly is to use variables with 
// global scope :-(  
// [Could potentially use sessionStorage or similar, but that's surely overkill]
let startWidth = 0, startHeight = 0;

window.onload = function() {    
    // get the contents of the JSON config file
    const CONFIG = JSON.parse(document.getElementById("config-id").textContent);
    const IMAGE_DATA = JSON.parse(document.getElementById("image-data-id").textContent);
    const REGION_DATA = JSON.parse(document.getElementById("region-data-id").textContent);

    // load the image selected by the user in step 1
    previewImage(CONFIG.HTML.APP.IMAGE_PANE.IMAGE.ID, 
                IMAGE_DATA,
                CONFIG.CONSTANTS.VALUES.MAX_IMAGE_SIZE);
    
    // create a wrapper SVG, for other SVG elements to sit inside
    const IMG = document.getElementById(CONFIG.HTML.APP.IMAGE_PANE.IMAGE.ID);
    const svg = createSvg(CONFIG.HTML.APP.IMAGE_PANE.CONTAINER.ID,
        CONFIG.HTML.APP.IMAGE_PANE.SVG.ID,
        CONFIG.HTML.APP.IMAGE_PANE.SVG.CLASS,
        IMG.clientWidth, 
        IMG.clientHeight);
    
    startWidth = IMG.clientWidth;
    startHeight = IMG.clientHeight;
    
    // draw the regions
    if(REGION_DATA !== null && REGION_DATA !== undefined) {
        const absData = rescaleDataToAbsoluteCoords(REGION_DATA, startWidth, startHeight);
        createRegions(svg, absData);
    }
    else {
        console.log("No regions found");
    }

    // add click events to buttons
    addClickEventsToButtons(CONFIG);
}

window.onresize  = function() {
    const CONFIG = JSON.parse(document.getElementById("config-id").textContent);
    const IMG = document.getElementById(CONFIG.HTML.APP.IMAGE_PANE.IMAGE.ID);
    
    console.log("Resizing window: height=" + $(window).height() + ", width=" + $(window).width());
    deleteRegionsAndRedraw();

    startWidth = IMG.clientWidth;
    startHeight = IMG.clientHeight;
}

function addClickEventsToButtons(config) {
    
    // Add click event to the Add Region button
    const addRgnBtn = document.getElementById(config.HTML.SET_REGIONS.ADD_REGION_BTN.ID);
    addRgnBtn.onclick = function() { clickAddRegion(); }
    
    // Add click event to the Find Regions button
    const findRgnsBtn = document.getElementById(config.HTML.SET_REGIONS.FIND_REGIONS_BTN.ID);
    findRgnsBtn.onclick = function() { 
        getRegionDataFromServer();
        // NOTE: the line below ensures that the AJAX call doesn't reload the whole
        // page; it just gets the new data and stops there. 
        // Not essential in a GET request, but does prevent the URL from having a 
        // rogue '?' at the end.
        return false;
    }

    // Add click event to the Next anchor tag
    const nextBtn = document.getElementById(config.HTML.APP.NEXT_BTN.ID);
    nextBtn.onclick = function() {
        // get region data, send to server in POST request, browse to next page
        const data = d3.selectAll("." + config.CONSTANTS.CLASSES.REGION).data();
        // convert data to relative coords, for consistency with Azure
        const rescaledData = rescaleDataToRelativeCoords(data, startWidth, startHeight);
        sendDataToServer({"data": JSON.stringify(rescaledData)}, 10000);        
        return true;
    }
}
