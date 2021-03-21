"use strict";

window.onload = function() {
    // get the contents of the JSON config file
    const CONFIG = JSON.parse(document.getElementById("config-id").textContent);
    const IMAGE_DATA = JSON.parse(document.getElementById("image-data-id").textContent);
    
    // get the Next and Upload Image button elements
    const nextBtn = document.getElementById(CONFIG.HTML.APP.NEXT_BTN.ID);
    const uploadImgBtn = document.getElementById(CONFIG.HTML.CHOOSE_IMAGE.UPLOAD_IMG_BTN.ID);

    // check whether there's any image data; if there isn't, the buttons should 
    // be disabled
    if(IMAGE_DATA === undefined || IMAGE_DATA === null) {
        if(!nextBtn.classList.contains("disabled")) {
            nextBtn.classList.add("disabled");
        }

        if(nextBtn.getAttribute("aria-disabled") !== true) {
            nextBtn.setAttribute("aria-disabled", true);
        }

        if(uploadImgBtn.disabled !== true) {
            uploadImgBtn.disabled = true;
        }
    }
    // if there is image data, load the image
    else {
        previewImage(CONFIG.HTML.APP.IMAGE_PANE.IMAGE.ID, 
                    IMAGE_DATA,
                    CONFIG.CONSTANTS.VALUES.MAX_IMAGE_SIZE);
    }

    // add click event to Upload Image button
    clickUploadImage();
}

function uploadSuccessful() {
    // get the contents of the JSON config file
    const CONFIG = JSON.parse(document.getElementById("config-id").textContent);

    // set the class and ARIA state of the Next button to active
    const nextBtn = document.getElementById(CONFIG.HTML.APP.NEXT_BTN.ID);
    if(nextBtn.classList.contains("disabled")){
        nextBtn.classList.remove("disabled");
    }
    if(nextBtn.getAttribute("aria-disabled") !== false){
        nextBtn.setAttribute("aria-disabled", false);
    }

    // change the text in the Upload Image button and disable
    const uploadImgBtn = document.getElementById(CONFIG.HTML.CHOOSE_IMAGE.UPLOAD_IMG_BTN.ID);
    uploadImgBtn.innerHTML = CONFIG.HTML.CHOOSE_IMAGE.UPLOAD_IMG_BTN.SUCCESS_TEXT;
    uploadImgBtn.disabled = true;
}

function uploadFailed() {
    // fire an alert to the user
    alert("WARNING: the file failed to upload failed. Please try again.");

    // get the contents of the JSON config file
    const CONFIG = JSON.parse(document.getElementById("config-id").textContent);
    // change the text in the Upload Image button and disable
    const uploadImgBtn = document.getElementById(CONFIG.HTML.CHOOSE_IMAGE.UPLOAD_IMG_BTN.ID);
    uploadImgBtn.innerText = CONFIG.HTML.CHOOSE_IMAGE.UPLOAD_IMG_BTN.TEXT;
}

function resetButtons() {
    // reset the text in the Upload Image button, and disable the Next button
    const CONFIG = JSON.parse(document.getElementById("config-id").textContent);
    
    // get the Next and Upload Image button elements
    const nextBtn = document.getElementById(CONFIG.HTML.APP.NEXT_BTN.ID);
    const uploadImgBtn = document.getElementById(CONFIG.HTML.CHOOSE_IMAGE.UPLOAD_IMG_BTN.ID);

    if(!nextBtn.classList.contains("disabled")) {
        nextBtn.classList.add("disabled");
    }
    if(nextBtn.getAttribute("aria-disabled") !== true) {
        nextBtn.setAttribute("aria-disabled", true);
    }

    uploadImgBtn.innerHTML = CONFIG.HTML.CHOOSE_IMAGE.UPLOAD_IMG_BTN.TEXT;
}

// ---------------------------------------------------------------------------
// SETUP EVENTS
// ---------------------------------------------------------------------------
// input change event
// https://www.w3schools.com/bootstrap4/bootstrap_forms_custom.asp
$(".custom-file-input").on("change", function() {
    resetButtons();
    const fileName = $(this).val().split("\\").pop();    
    $(this).siblings(".custom-file-label").addClass("selected").html(fileName);

    // get the contents of the JSON config file
    const CONFIG = JSON.parse(document.getElementById("config-id").textContent);
    const IMAGE_DATA = JSON.parse(document.getElementById("image-data-id").textContent);

    // preview the image selected by the user
    previewImage(CONFIG.HTML.APP.IMAGE_PANE.IMAGE.ID, 
                IMAGE_DATA, 
                CONFIG.CONSTANTS.VALUES.MAX_IMAGE_SIZE,
                this);
    
    // enable the Upload Image button
    const uploadImgBtn = document.getElementById(CONFIG.HTML.CHOOSE_IMAGE.UPLOAD_IMG_BTN.ID);
    if(uploadImgBtn.disabled === true){
        uploadImgBtn.disabled = false;
    }
});

// Upload Image click event
function clickUploadImage() {
    // get the contents of the JSON config file
    const CONFIG = JSON.parse(document.getElementById("config-id").textContent);
    
    // get the Upload Image button
    const uploadImgBtn = document.getElementById(CONFIG.HTML.CHOOSE_IMAGE.UPLOAD_IMG_BTN.ID);
    uploadImgBtn.onclick = function() {
        uploadImgBtn.innerHTML = CONFIG.HTML.CHOOSE_IMAGE.UPLOAD_IMG_BTN.WAIT_TEXT;
        const img_data = document.getElementById(CONFIG.HTML.APP.IMAGE_PANE.IMAGE.ID).src;
        const img_name = document.querySelector("label[for=" + CONFIG.HTML.CHOOSE_IMAGE.CHOOSE_IMG_BTN.ID  + "]").innerText;
        sendDataToServer({"data": img_data, "name": img_name}, 30000, uploadSuccessful, uploadFailed);
    }
}
