"use strict";


window.onload = function() {
    // get the contents of the JSON config file
    const CONFIG = JSON.parse(document.getElementById("config-id").textContent);

    // set the class and ARIA state of the Next button to active
    const nextBtn = document.getElementById(CONFIG.HTML.APP.NEXT_BTN.ID);
    if(!nextBtn.classList.contains("disabled")){
        nextBtn.classList.add("disabled");
    }

    if(nextBtn.getAttribute("aria-disabled") !== true){
        nextBtn.setAttribute("aria-disabled", true);
    }

    // 
    previewImage(CONFIG.HTML.APP.IMAGE_PANE.ID, 
        CONFIG.HTML.HOME.IMAGE_PANE.FILE_DATA_KEY,
        CONFIG.HTML.HOME.IMAGE_PANE.FILE_NAME_KEY);
    
}

// https://www.w3schools.com/bootstrap4/bootstrap_forms_custom.asp
$(".custom-file-input").on("change", function() {
    const fileName = $(this).val().split("\\").pop();    
    $(this).siblings(".custom-file-label").addClass("selected").html(fileName);

    // get the contents of the JSON config file
    const CONFIG = JSON.parse(document.getElementById("config-id").textContent);

    // preview the image selected by the user
    previewImage(CONFIG.HTML.APP.IMAGE_PANE.ID,
        CONFIG.HTML.HOME.IMAGE_PANE.FILE_DATA_KEY,
        CONFIG.HTML.HOME.IMAGE_PANE.FILE_NAME_KEY,
        this); 
    
    // set the class and ARIA state of the Next button to active
    const nextBtn = document.getElementById(CONFIG.HTML.APP.NEXT_BTN.ID);
    if(nextBtn.classList.contains("disabled")){
        nextBtn.classList.remove("disabled");
    }

    if(nextBtn.getAttribute("aria-disabled") !== false){
        nextBtn.setAttribute("aria-disabled", false);
    }
});


