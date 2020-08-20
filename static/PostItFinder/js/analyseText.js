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
    
    // update the image width and height
    startWidth = IMG.clientWidth;
    startHeight = IMG.clientHeight;
    
    // add click events to buttons
    addClickEventsToButtons(CONFIG);
}

function addClickEventsToButtons(config) {
    const analyseTextBtn = document.getElementById(config.HTML.ANALYSE_TEXT.ANALYSE_TEXT_BTN.ID);
    analyseTextBtn.onclick = function() { 
        // change the button text        
        analyseTextBtn.innerHTML = config.HTML.ANALYSE_TEXT.ANALYSE_TEXT_BTN.WAIT_TEXT;

        // Make the AJAX GET request
        const alertText = "The OCR algorithm did not find any text.";
        getDataFromServer(analyseTextBtnAjax, alertText);
        return false;
    }
}

function analyseTextBtnAjax(regionData) {
    const CONFIG = JSON.parse(document.getElementById("config-id").textContent);

    // draw the regions, apply tooltips etx.
    drawStaticRegions(regionData);

    // update the text in the button, to show that we're done
    const analayseTxtBtn = document.getElementById(CONFIG.HTML.ANALYSE_TEXT.ANALYSE_TEXT_BTN.ID);
    analayseTxtBtn.innerHTML = CONFIG.HTML.ANALYSE_TEXT.ANALYSE_TEXT_BTN.TEXT;
}