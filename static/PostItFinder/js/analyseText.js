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
        $.ajax({     
            type: "GET",
            dataType: "json",
            timeout: 5000
        })
        .done(function(returnData) {
            console.log("AJAX RESPONSE SUCCEEDED"); 
            console.log(returnData);
        })
        .fail(function(jqXHR) {
            console.log("AJAX RESPONSE FAILED");
            console.log("Status: " +  jqXHR.status);
            console.log("Status text: " + jqXHR.statusText);
            console.log("Response type: " + jqXHR.responseType);
            console.log("Response text: " + jqXHR.responseText);
            console.log("Ready state: " + jqXHR.readyState);

            if(jqXHR.statusText === "timeout") {
                alert("The request timed out. The Azure server may be experiencing issues; please try again later.");
            }
        }) 
        return false;
    }
}