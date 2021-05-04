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
 * Return the first 4 bytes of a file as a hex string, and check whether it is
 * of a valid image type. If so, display the image; if not, display an alert to 
 * the user. Using the file header info should make it difficult to spoof the 
 * file info.
 * 
 * Based on this post: https://stackoverflow.com/a/29672957. 
 * @param {File} blob, the file to be examined 
 * @param {String} imgID, the DOM ID that holds the valid image 
 * @param {Number} NUM_BYTES, the number of bytes to read. Defaults to 4
 */
function getBLOBFileHeader(blob, imgID, NUM_BYTES=4) {
    const fileReader = new FileReader();
    fileReader.onloadend = function(e) {
        // get the first 4 bytes of the file and store them as a hex string
        let arr = (new Uint8Array(e.target.result)).subarray(0, NUM_BYTES);
        let header = "";
        for (var i = 0; i < arr.length; i++) {
            header += arr[i].toString(16);
        }

        // check whether the file MIME type is valid. If so, display the image;
        // if not, display an alert
        const mType = mimeType(header);
        printFileInfo(mType, blob.type, header);
        if(mType.valid) {
            displayImage(blob, imgID);
        } else {
            alert(`The file type ${mType.type} is not permitted. Only JPEG, PNG and BMP files can be used.`);
        }
    };
    fileReader.readAsArrayBuffer(blob);    
}

/**
 * Print information on MIME type and file header to the console for debugging.
 * @param {Object} mType, object of the form {"type": String, "valid": Boolean}.
 * "type" is the actual MIME type, derived from the file header.
 * @param {String} believedType, the MIME type that the browser believes the file 
 * is, from the fiole extension (can be spoofed)
 * @param {String} headerString, the first 4 bytes of the file header
 */
function printFileInfo(mType, believedType, headerString) {
    console.log(`Real MIME type: ${mType.type}`);
    console.log(`Permitted type: ${mType.valid}`);
    console.log(`Browser MIME type: ${believedType}`);
    console.log(`File header: 0x${headerString}`);
}
  
/**
 * Checks whether the header provided matches a pattern for any of the acceptable
 * image types. 
 * @param {String} headerString, the first 4 bytes of the file header
 * @returns {Object}, of the form {"type": String, "valid": Boolean}. If the file
 * is valid, "type" will be the MIME type of the file; if is isn't, "type" will be
 * "unknown".
 * @todo: replace the forEach with a for..loop or .some()
 */
// Add more from http://en.wikipedia.org/wiki/List_of_file_signatures
function mimeType(headerString) {
    let result = {"type": "unknown", "valid": false};

    const SIGS = [
        {"type": "image/bmp", "sig": "424d"},
        {"type": "image/png", "sig": "89504e47"},
        {"type": "image/jpeg", "sig": "ffd8ff"}        
    ]
    
    // NOTE: this loop could be changed for a .some(), or a normal for..loop with a
    // break, for a small efficiency saving. But since SIGS only contains 3 elements
    // (and is only called once when an image is selected), this is low-priority
    SIGS.forEach(function(d) {
        if(headerString.slice(0, d.sig.length) === d.sig) { 
            result = {"type": d.type, "valid": true}; 
        }
    })

    return result;
}

/**
 * Displays the image in the correct place within the web page.
 * https://stackoverflow.com/questions/922057/is-it-possible-to-preview-local-images-before-uploading-them-via-a-form,
 * https://stackoverflow.com/a/20535454 
 * 
 * @param {File} file, the image to be displayed
 * @param {String} imgID, the ID of the DOM element where the image will be displayed.
 */
function displayImage(file, imgID) {
    const reader = new FileReader();
    reader.onloadend = function(myFile) {
        const img = new Image();
        img.src = myFile.target.result;
        img.onload = function() {
            $('#' + imgID).attr('src', this.src);
            $('#' + imgID).prop('alt', file.name);
        }
    };            
    reader.readAsDataURL(file);
}
 

/**
 * Checks whether an image selected by a user from the local filesystem via an 
 * HTML input control is of an acceptable type. If it is, display the image.
 * Otherwise, display an alert.
 * 
 * @param {string} imgID - the ID of the HTML <img> element that will display the image
 * @param {object} fileData - a key/value pair of the form 
 *      {"data": <str, base64 encoding of image bytes>,
 *       "name": <str, name of the file>}
 * @param {object} input - the HTML input control that was clicked
 * @param {number} maxImageSize - the maximum allowed file size, in bytes
 * @todo - add .onerror events for reader, img (in addition to the .onloads)
 * @todo - add code to final else{} clause - may be better to handle in Django?
 */
function previewImage(imgID, fileData, maxImageSize, input) {
    // case 1: user selects a file using input
    if (input !== undefined && input.files && input.files[0]) {
        const fileSize = input.files[0].size;
        if(fileSize <= maxImageSize) {
            getBLOBFileHeader(input.files[0], imgID);
        } else {
            const fileSizeMB = Number.parseFloat(fileSize / (1024 * 1024)).toFixed(1);
            const maxImageSizeMB = Number.parseFloat(maxImageSize / (1024 * 1024)).toFixed(1);
            alert("The file selected is " +  fileSizeMB + "MB. The max file size for image processing is " + maxImageSizeMB + "MB.");
        }
    } else {
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