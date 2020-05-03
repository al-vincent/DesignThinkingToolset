"use strict";

// Add the following code if you want the name of the file appear on select
// https://www.w3schools.com/bootstrap4/bootstrap_forms_custom.asp
$(".custom-file-input").on("change", function() {
    const fileName = $(this).val().split("\\").pop();    
    $(this).siblings(".custom-file-label").addClass("selected").html(fileName);


    const CONFIG = JSON.parse(document.getElementById("config-id").textContent);
    previewImage(this, CONFIG.HTML.APP.IMAGE_PANE.ID);
});


