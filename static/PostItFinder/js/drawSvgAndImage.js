/****************************************************************************************************
 * @name: drawSvgAndImage.js
 * @description: functions to create a parent SVG and append an image to it.
 * Also includes function to preview image selected by user from the local filesystem.
 * 
 * These functions are (broadly) intended to be library functions; 
 * i.e. freestanding and callable from 'driver' files.
 ****************************************************************************************************/


"use strict";


/**
 * Displays an image selected by a user from the local filesystem via an 
 * HTML input control in the UI. Also stores the file data and file name in 
 * sessionStorage for retrieval by other pages.
 * https://stackoverflow.com/questions/922057/is-it-possible-to-preview-local-images-before-uploading-them-via-a-form,
 * https://stackoverflow.com/a/20535454 
 * @param {string} imgID - the ID of the HTML <img> element that will display the image
 * @param {string} fileDataKey - the key for the image data string in sessionStorage
 * @param {string} fileNameKey - the key for the image file name in sessionStorage
 * @param {object} input - the HTML input control that was clicked
 * @todo - add checks to see if sessionStorage can be used
 * @todo - add .onerror events for reader, img (in addition to the .onloads)
 * @todo - add code to final else{} clause - may be better to handle in Django?
 * @todo - factor out some of the functionality into other functions?
 */
function previewImage(imgID, fileData, input) {
    // case 1: user selects a file using input
    if (input !== undefined && input.files && input.files[0]) { 
        const reader = new FileReader();
        reader.onload = function(myFile) {            
            const img = new Image();
            img.src = myFile.target.result;

            img.onload = function() {
                $('#' + imgID).attr('src', this.src);
                $('#' + imgID).prop('alt', input.files[0].name);
                // send the image data to the server as an AJAX POST request
                sendDataToServer({"data": this.src, "name": input.files[0].name}, 10000);
            }                       
        };

        reader.readAsDataURL(input.files[0]);
    } 
    else {
        if (fileData !== undefined && fileData !== null) {
            // case 2: user has previously selected a file 
            $('#' + imgID).attr('src', fileData.data);
            $('#' + imgID).prop('alt', fileData.name);
        }
        // case 3: user has browsed direct to set-regions or later pages (e.g. by
        // typing the URL into the browser directly),so has not selected an image.
        else {
            // ?? Need to redirect the user to home (if not already there); 
            // but how?
        }

    }
}

/**
 * @description - function to create the SVG container.
 * @param {string} svgID - DOM ID of the div that will contain the SVG element (and everything else)
 * @param {number} width - the width of the SVG (and image)
 * @param {number} height - the height of the SVG (and image)
 * @returns - svg, a Scalable Vector Graphics object.
 * @throws - none.
 * @todo - throw an exception if no element with svgID exists in the DOM.
 */
function createSvg(svgContainerID, svgID, svgClass, width, height) {
    // create svg element:
    const svg = d3.select("#" + svgContainerID).append("svg")
        .attr("width", width)
        .attr("height", height)
        .attr("id", svgID)
        .attr("class", svgClass);

    return svg;
}

/**
 * @description - function to append an image to the container and update 
 * the image attributes to correctly show the image provided.
 * @param {object} svg - the parent SVG that the image is appended to.
 * @param {string} imgFile - the name of the local image file to display
 * @param {number} width - the width of the SVG (and image)
 * @param {number} height - the height of the SVG (and image)
 * @returns: none.
 * @throws: none.
 * @todo: throw an exception if an invalid filename is provided.
 */
function createImage(svg, imgFile, width, height) {
    // load image
    let newImg = svg.selectAll("image")
        .data([0])
        .enter()
        .append("svg:image");

    // set image parameters
    newImg.attr("xlink:href", imgFile)
          .attr("x", 0)
          .attr("y", 0)
          .attr("width", width)
          .attr("height", height);
}