/****************************************************************************************************
 * @name: drawSvgAndImage.js
 * @description: functions to create a parent SVG and append an image to it.
 * 
 * These functions are (broadly) intended to be library functions; 
 * i.e. freestanding and callable from 'driver' files.
 ****************************************************************************************************/

"use strict";

/**
 * @description: function to create the SVG container.
 * @param: 
 *  - svgID, string, the DOM ID of the div that will contain the SVG element 
 *    (and everything else)
 *  - width, number, the width of the SVG (and image)
 *  - height, number, the height of the SVG (and image)
 * @returns: svg, a Scalable Vector Graphics object.
 * @throws: none.
 * @todo: throw an exception if no element with svgID exists in the DOM.
 */
function createSvg(svgID, width, height) {
    // create svg element:
    const svg = d3.select("#" + svgID).append("svg")
        .attr("width", width)
        .attr("height", height);

    return svg;
}

/**
 * @description: function to append an image to the container and update 
 * the image attributes to correctly show the image provided.
 * @param: 
 *  - svg, object, the parent SVG that the image is appended to.
 *  - imgFile, string, the name of the local image file to display
 *  - width, number, the width of the SVG (and image)
 *  - height, number, the height of the SVG (and image)
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