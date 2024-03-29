let startWidth = 0, startHeight = 0;

window.onload = function() {    
    // get the contents of the JSON config file
    const CONFIG = JSON.parse(document.getElementById("config-id").textContent);
        
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

window.onresize  = function() {
    const CONFIG = JSON.parse(document.getElementById("config-id").textContent);
    const IMG = document.getElementById(CONFIG.HTML.APP.IMAGE_PANE.IMAGE.ID);
    
    console.log("Resizing window: height=" + $(window).height() + ", width=" + $(window).width());
    deleteRegionsAndRedraw();

    startWidth = IMG.clientWidth;
    startHeight = IMG.clientHeight;
}

function addClickEventsToButtons(config) {
    const analyseTextBtn = document.getElementById(config.HTML.ANALYSE_TEXT.ANALYSE_TEXT_BTN.ID);
    analyseTextBtn.onclick = function() { 
        // change the button text        
        analyseTextBtn.innerHTML = config.HTML.ANALYSE_TEXT.ANALYSE_TEXT_BTN.WAIT_TEXT;

        // Make the AJAX GET request
        const alertText = "The OCR algorithm did not find any text.";
        getDataFromServer(clickAnalyseTextAJAX, alertText, config.HTML.ANALYSE_TEXT.ANALYSE_TEXT_BTN);
        return false;
    }
}

function clickAnalyseTextAJAX(returnData) {
    const CONFIG = JSON.parse(document.getElementById("config-id").textContent);

    // draw the text regions and tooltip
    drawStaticRegions(returnData["data"]);

    const downloadResultsBtn = document.getElementById(CONFIG.HTML.ANALYSE_TEXT.DOWNLOAD_RESULTS_BTN.ID);
    // change the href of the Download Results button
    downloadResultsBtn.href = returnData["url"];

    // change the Download Results button to be enabled
    downloadResultsBtn.classList.remove("disabled");
    downloadResultsBtn.setAttribute("aria-disabled", false);
}