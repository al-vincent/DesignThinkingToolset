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
 * Displays an image selected by a user from the local filesystem via an HTML input control in the UI.
 * https://stackoverflow.com/questions/922057/is-it-possible-to-preview-local-images-before-uploading-them-via-a-form, 
 * https://stackoverflow.com/questions/15491193/getting-width-height-of-an-image-with-filereader
 * @param {object} input - the HTML input control that was clicked
 * @param {string} imgID - the ID of the HTML <img> element that will display the image
 * @todo - add .onerror events for reader, img (in addition to the .onloads)
 */
function previewImage(input, imgID) {
    if (input.files && input.files[0]) {        
        const reader = new FileReader();
        reader.onload = function(myFile) {            
            const img = new Image();
            img.src = myFile.target.result;

            img.onload = function() {
                $('#' + imgID).attr('src', this.src);
            }            
        };

        reader.readAsDataURL(input.files[0]);
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
function createSvg(svgID, width, height) {
    // create svg element:
    const svg = d3.select("#" + svgID).append("svg")
        .attr("width", width)
        .attr("height", height);

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