/****************************************************************************************************
 * @name: drawAndEditBoxes.js
 * @description: functions to add a series of resizable boxes to a parent SVG.
 * 
 * These functions are (broadly) intended to be library functions; i.e. freestanding and callable 
 * from 'driver' files.
 ****************************************************************************************************/


/** 
 * References to CSS classes
*/
const BOX_GROUP = "box"
const HANDLE_GROUP = "handle-group";
const TOP_LEFT = "top-left";
const BOTTOM_RIGHT = "bottom-right";

const HANDLE_RADIUS = 3;
const CORNER_RADIUS = 3;
const MIN_RECT_WIDTH = 20;
const MIN_RECT_HEIGHT = 20;
const DEFAULT_RECT_WIDTH = 60;
const DEFAULT_RECT_HEIGHT = 40;

let IMAGE_WIDTH = 0;
let IMAGE_HEIGHT = 0;

/**
 * @description: adds resizable boxes on the image / SVG, at locations defined by 'data'. 
 * Also sets callbacks for resizing of boxes.
 * @param: 
 *  - svg, object, the parent SVG that the image is appended to.
 *  - data, object array, the data used to position and size each of the boxes. One box is 
 * created for each object in the array.
 * @returns: none.
 * @throws: none.
 * @todo: several variables currently declared via 'let'; should be 'const'?
 */
function createRegion(svg, data) {
    // setup drag behaviour for the rectangle part of the box
    const dragRect = d3.behavior.drag()
        .origin(function(d) { return d; })
        .on("dragstart", dragStarted)
        .on("drag", dragBox);
    
    // setup drag behaviour for the top-left handle
    const dragTopLeftHandle = d3.behavior.drag()
        .origin(function(d) { return d; })
        .on("dragstart", dragStarted)
        .on("drag", dragTlHandle);
    
    // setup drag behaviour for the bottom-right handle
    const dragBottomRightHandle = d3.behavior.drag()
        .origin(function(d) { return d; })
        .on("dragstart", dragStarted)
        .on("drag", dragBrHandle);

    // create the boxes
    // https://stackoverflow.com/questions/43297888/d3-js-grouping-with-g-with-the-data-join-enter-update-exit-cycle/43298892
    // let grps = svg.selectAll("g").data(data);
    let grps = svg.selectAll("." + BOX_GROUP).data(data);

    // create the boxes that will be used to highlight post-it notes; 1 x rect element, 
    // plus 2 x circle elements as "grab handles" to resize the rect (one circle on 
    // top-left corner, one on bottom-right corner)
    let newGrps = grps.enter();
    // setting properties for the group also sets the properties for all elements
    // contained within the group
    let newGrp = newGrps.append("g")    
                        .attr("stroke-width", 3)
                        .attr("fill", "orange")
                        .attr("opacity", 0.3)
                        .attr("stroke", "black")
                        .attr("class", BOX_GROUP)
                        .on("dblclick", function() {
                            deleteBoxGrp(this);
                        });
    
    // add the rect element
    newGrp.append("rect"); 
    // handles are a bit trickier; we want to create a new group (so that we can bind 
    // the resize event to both sets of handles), and have two classes of circle in it,
    // one for the handles on the top-left of rects, and one for bottom-right handles.
    let handleGrp = newGrp.append("g").attr("class", HANDLE_GROUP); 
    handleGrp.append("circle").attr("class", TOP_LEFT);
    handleGrp.append("circle").attr("class", BOTTOM_RIGHT);

    // set attributes for all the SVG shapes
    grps.select("rect")
        .attr("x", function(d) { return d.x; })
        .attr("y", function(d) { return d.y; })            
        .attr("width", function(d) { return d.width; })
        .attr("height", function(d) { return d.height; })
        .attr("rx", CORNER_RADIUS)
        .on("click", function(d) { console.log(d); })
        .call(dragRect);
    
    // set attributes for the top-left set of handles (i.e. circle elements) 
    grps.select("." + TOP_LEFT)
        .attr("cx", function(d) { return d.x; })
        .attr("cy", function(d) { return d.y; })
        .attr("r", HANDLE_RADIUS )
        .on("click", function(d) { console.log(d); })
        .call(dragTopLeftHandle);
    
    // set attributes for the bottom-right set of handles (i.e. circle elements) 
    grps.select("." + BOTTOM_RIGHT)
        .attr("cx", function(d) { return d.x + d.width; })
        .attr("cy", function(d) { return d.y + d.height; })
        .attr("r", HANDLE_RADIUS )
        .on("click", function(d) { console.log(d); })
        .call(dragBottomRightHandle);
}

/****************************************************************************************************
 * CALLBACKS
 ***************************************************************************************************/

/**
 * @description: callback that deletes a single resizable box.
 * @param: boxGrp, group of 3 x SVG elements (1 x 'body' rect element and 2 x 'handle' 
 * circle elements) that fired the event; e.g the rect or handle that was double-clicked 
 * by the user.
 * @returns: none.
 * @throws: none.
 * @todo: none.
 */
function deleteBoxGrp(boxGrp) {
    console.log("Delete box");
    d3.select(boxGrp).remove();
}

/**
 * @description: callback to drag a resizable box (i.e. rect body and handles). The 
 * box cannot be dragged outside the edges of the image. Callback is bound to the 
 * rect element.
 * 
 * Inspired by https://bl.ocks.org/Herst/093ff9962405dd564ef58ad8af9544d0, though 
 * implemented differently.
 * @param: d, object array, the data bound to the calling element (i.e. the rect).
 * Each object is of format {"x": number, "y": number, "width": number, "height": number}
 * @returns: none.
 * @throws: none.
 * @todo: consider refactoring so that IMAGE_WIDTH and IMAGE_HEIGHT are parameters.
 */
function dragBox(d) {        
    // The Math.min and Math.max prevent the boxes being dragged outside the image
    d.x = Math.min(Math.max(d3.event.x, 0), IMAGE_WIDTH - d.width);
    d.y = Math.min(Math.max(d3.event.y, 0), IMAGE_HEIGHT - d.height);

    // start by moving the rect element
    d3.select(this)
        .attr("x", d.x)
        .attr("y", d.y);
    
    // get the parent group of the rect element 
    const boxGroup = d3.select(this).node().parentNode;

    // get the bottom-right circle, and set the new coords    
    d3.select(boxGroup).select("." + HANDLE_GROUP).select("." + BOTTOM_RIGHT)
        .attr("cx", d.x + d.width)
        .attr("cy", d.y + d.height);
    
    // get the bottom-right circle, and set the new coords
    d3.select(boxGroup).select("." + HANDLE_GROUP).select("." + TOP_LEFT)
        .attr("cx", d.x)
        .attr("cy", d.y);    
}

/**
 * @description: callback to overwrite any callbacks that might be bound to the 
 * calling element. 
 * 
 * May not be 100% required, but defensive against unexpected behaviour.
 * @param: none.
 * @returns: none.
 * @throws: none.
 * @todo: none.
 */
function dragStarted() {
    d3.event.sourceEvent.stopPropagation();
}

/**
 * @description: callback to resize the box when the top-left handle is dragged.
 * The handle cannot be dragged outside the image boundaries, and the box has a
 * minimum width and height (which also prevents "inversions" of the box, where
 * the top-left handle could become the bottom-right handle).
 * @param: d, object array, the data bound to the calling element (i.e. the top-left 
 * circle element). 
 * Each object is of format {"x": number, "y": number, "width": number, "height": number}
 * @returns: none.
 * @throws: none.
 * @todo: none.
 */
function dragTlHandle(d) {
    console.log("Dragging top-left"); 

    // navigate up the SVG element tree to the top-level group
    const handleGroup = d3.select(this).node().parentNode;
    const boxGroup = d3.select(handleGroup).node().parentNode;
    
    // Ensure the box  doesn't go below the min size, or outside the edges of the image
    const newWidth = Math.min(Math.max(d.width - d3.event.dx, MIN_RECT_WIDTH), d.x + d.width);
    d.x += d.width - newWidth;
    d.width = newWidth;

    const newHeight = Math.min(Math.max(d.height - d3.event.dy, MIN_RECT_HEIGHT), d.y + d.height);
    d.y += d.height - newHeight;
    d.height = newHeight

    // move the handle to the new position 
    d3.select(this)
        .attr("cx", d.x)
        .attr("cy", d.y); 

    // resize the rect element
    d3.select(boxGroup).select("rect")
        .attr("x", d.x)
        .attr("y", d.y)
        .attr("width", d.width)
        .attr("height", d.height);
}

/**
 * @description: callback to resize the box when the bottom-right handle is dragged.
 * The handle cannot be dragged outside the image boundaries, and the box has a
 * minimum width and height (which also prevents "inversions" of the box, where
 * the bottom-right handle could become the top-left handle).
 * @param: d, object array, the data bound to the calling element (i.e. the top-left 
 * circle element). 
 * Each object is of format {"x": number, "y": number, "width": number, "height": number}
 * @returns: none.
 * @throws: none.
 * @todo: none.
 */
function dragBrHandle(d) {
    console.log("Dragging bottom-right");       
    
    // navigate up the SVG element tree to the top-level group
    const handleGroup = d3.select(this).node().parentNode;
    const boxGroup = d3.select(handleGroup).node().parentNode;
    
    // Set width and height so that the box doesn't go below the min size, or outside
    // the edges of the image
    d.width = Math.min(Math.max(d.width + d3.event.dx, MIN_RECT_WIDTH), IMAGE_WIDTH - d.x);
    d.height = Math.min(Math.max(d.height + d3.event.dy, MIN_RECT_HEIGHT), IMAGE_HEIGHT - d.y);
    
    // move the handle to the new position 
    d3.select(this)
        .attr("cx", d.x + d.width)
        .attr("cy", d.y + d.height); 

    // resize the rect element
    d3.select(boxGroup).select("rect")
        .attr("width", d.width)
        .attr("height", d.height);               
}

/**
 * @description: exception raised if the user tries to create a new box and there isn't enough
 * space in the image for it.
 * @param: 
 *  - x, number, x-coordinate of the last box created. 
 *  - y, number, y-coordinate of the last box created. 
 * @returns: none.
 * @throws: none.
 * @todo: none.
 */
function OutOfBoundsException(x,y) {
    this.coords = [x,y];
    this.message = "Out of space - no more boxes permitted";
}

/**
 * @description: function to decide on coords for a new box. By default, new boxes are placed in 
 * the top-left corner of the image, and then tiled horizontally in rows (starting a new row when 
 * the next box would go outside the edge of the image). When the image is completely tiled, an 
 * exception is thrown.
 * A new box cannot be colocated with an existing box.
 * @param: none.
 * @returns: [x,y], array of numbers giving the [x,y] coords of the new location IN THE IMAGE 
 * COORDINATE SPACE (i.e. using image coords, NOT whole page coords).
 * @throws: OutOfBoundsException if the image is believed to be full of boxes.
 * @todo: consider adding a control that allows users to set minimum box size.
 */
function getNewBoxLocation() {
    
    let x = 0;
    let y = 0;

    while(!isNewLocationFree(x, y)) {
        // debugger;
        // Cases:
        // 1. next rect will go over the image edge in x and y: throw exception        
        if (x + 2 * DEFAULT_RECT_WIDTH > IMAGE_WIDTH) {            
            if (y + 2 * DEFAULT_RECT_HEIGHT > IMAGE_HEIGHT) {                
                throw new OutOfBoundsException(x,y);
            } 
        // 2. next rect will go over image in x, but not y: set x to 0, increment y by rect height
            else {                
                x = 0;
                y += DEFAULT_RECT_HEIGHT; 
            }
        } 
        // 3. next rect will not go over image edge in x: increment x by rect width
        else {
            x += DEFAULT_RECT_WIDTH;
        }
    }

    return [x,y];
}

/**
 * @description: checks if the proposed new location overlaps with an existing box. Boxes are
 * considered to be 'too overlapping' if the difference between the top-left corner of the new
 * box is less than 2 handle-radii from an existing box.
 * @param: 
 *  - x, number, proposed x-coordinate of the new box. 
 *  - y, number, proposed y-coordinate of the new box. 
 * @returns: locationFree, boolean. True if the proposed location is ok, false if not.
 * @throws: custom exceptions.
 * @todo: change exceptions to be functions, as per OutOfBoundsException().
 */
function isNewLocationFree(x,y) {
    // some error checking on the parameters
    if (typeof(x) !== "number" || isNaN(x)) { throw "x coord is not a number"; }
    if (typeof(x) !== "number" || isNaN(y)) { throw "y coord is not a number"; }
    if (x < 0 || x > IMAGE_WIDTH) { throw "x coord is outside image bounds"; }
    if (y < 0 || y > IMAGE_HEIGHT) { throw "y coord is outside image bounds"; }

    // main section of function
    let locationFree = true;
    d3.selectAll("rect").each(function() {
        const rect = d3.select(this);
        if( (Math.abs(rect.attr("x") - x) <= 2 * HANDLE_RADIUS) && (Math.abs(rect.attr("y") - y) <= 2 * HANDLE_RADIUS) ) {
            locationFree = false;
        }
    });
    return locationFree;
}

/** 
 * @todo: consider - should this (and the two fns above) be moved into the driver function instead?
 * Arguments both ways I think.
*/
function clickAddRegion() {
    // get the new coordinates and create a data object
    console.log("Click add region");
    try {
        const coords = getNewBoxLocation();
        const newData = {"x": coords[0],
                        "y": coords[1],
                        "width": DEFAULT_RECT_WIDTH,
                        "height": DEFAULT_RECT_HEIGHT
                        };
        // add the new data to the existing array
        const data = d3.selectAll("." + BOX_GROUP).data();
        data.push(newData);

        /**************************************************************************************
         * NOTE: the below is not the best way to achieve the goal. It *should* be possible to 
         * to do this via d3 enter() and exit(), just updating the data; but I can't get it to 
         * work properly, and does what I want, so...
         ***************************************************************************************/
        // delete all existing boxes, and recreate them with the new data
        d3.selectAll("." + BOX_GROUP).remove();
        createRegion(d3.select("svg"), data);
    }
    catch (err) {
        console.log(err);
        console.error(err.message + "; coords: (" + err.coords[0] + "," + err.coords[1] + ")");
        alert(err.message);
    }
}