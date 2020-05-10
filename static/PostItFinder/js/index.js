"use strict";

// Add the following code if you want the name of the file appear on select
// https://www.w3schools.com/bootstrap4/bootstrap_forms_custom.asp
$(".custom-file-input").on("change", function() {
    const fileName = $(this).val().split("\\").pop();    
    $(this).siblings(".custom-file-label").addClass("selected").html(fileName);

    // get the contents of the JSON config file
    const CONFIG = JSON.parse(document.getElementById("config-id").textContent);    

    // preview the image selected by the user
    previewImage(this, CONFIG.HTML.APP.IMAGE_PANE.ID, CONFIG.HTML.HOME.IMAGE_PANE.FILE_STORE_KEY);
    
    // set the class and ARIA state of the Next button to active
    const nextBtn = document.getElementById(CONFIG.HTML.APP.NEXT_BTN.ID);
    if(nextBtn.classList.contains("disabled")){
        nextBtn.classList.remove("disabled");
    }

    if(nextBtn.getAttribute("aria-disabled") === true){
        nextBtn.setAttribute("aria-disabled", false);
    }
});


