/****************************************************************************************************
 * @name: drawAndEditRegions.js
 * @description: functions to add a series of resizable regions to a parent SVG.
 * 
 * These functions are (broadly) intended to be library functions; i.e. freestanding and callable 
 * from 'driver' files.
 ****************************************************************************************************/


// ================================================================================================
// CREATE AND DESTROY REGIONS
// ================================================================================================

/**
 * @description: adds resizable regions on the image / SVG, at locations defined by 'data'. 
 * Also sets callbacks for resizing of regions.
 * @param: 
 *  - svg, object, the parent SVG that the image is appended to.
 *  - data, object array, the data used to position and size each of the regions. One region is 
 * created for each object in the array.
 * @returns: none.
 * @throws: none.
 * @todo: several variables currently declared via 'let'; should be 'const'?
 */
function createRegions(svg, data) {
    // Get constants from config.json
    const CONFIG = JSON.parse(document.getElementById("config-id").textContent);
    const REGION_CLASS = CONFIG.CONSTANTS.CLASSES.REGION;
    const BODY_RECT_CLASS = CONFIG.CONSTANTS.CLASSES.BODY_RECT;
    const HANDLE_CLASS = CONFIG.CONSTANTS.CLASSES.HANDLE;
    const TOP_LEFT_CLASS = CONFIG.CONSTANTS.CLASSES.TOP_LEFT_HANDLE;
    const BOTTOM_RIGHT_CLASS = CONFIG.CONSTANTS.CLASSES.BOTTOM_RIGHT_HANDLE;
    const HANDLE_RADIUS = CONFIG.CONSTANTS.VALUES.HANDLE_RADIUS;
    const CORNER_RADIUS = CONFIG.CONSTANTS.VALUES.CORNER_RADIUS;
    const FILL_COLOUR = CONFIG.CONSTANTS.COLOURS.REGION_COLOUR;
    const STROKE_COLOUR = CONFIG.CONSTANTS.COLOURS.REGION_EDGE_COLOUR;

    // setup drag behaviour for the rectangle part of the region
    const dragRect = d3.behavior.drag()
        .origin(function(d) { return d; })
        .on("dragstart", dragStarted)
        .on("drag", dragRegion);
    
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

    // create the regions
    // https://stackoverflow.com/questions/43297888/d3-js-grouping-with-g-with-the-data-join-enter-update-exit-cycle/43298892
    // let grps = svg.selectAll("g").data(data);
    let grps = svg.selectAll("." + REGION_CLASS).data(data);

    // create the regions that will be used to highlight post-it notes; 1 x rect element, 
    // plus 2 x circle elements as "grab handles" to resize the rect (one circle on 
    // top-left corner, one on bottom-right corner)
    let newGrps = grps.enter();
    // setting properties for the group also sets the properties for all elements
    // contained within the group
    let newGrp = newGrps.append("g")    
                        .attr("stroke-width", 3)
                        .attr("fill", FILL_COLOUR)
                        .attr("opacity", 0.3)
                        .attr("stroke", STROKE_COLOUR)
                        .attr("class", REGION_CLASS)
                        .on("dblclick", function() {
                            deleteRegionGrp(this);
                        });
    
    // add the rect element
    newGrp.append("rect").attr("class", BODY_RECT_CLASS); 
    // handles are a bit trickier; we want to create a new group (so that we can bind 
    // the resize event to both sets of handles), and have two classes of circle in it,
    // one for the handles on the top-left of rects, and one for bottom-right handles.
    let handleGrp = newGrp.append("g").attr("class", HANDLE_CLASS); 
    handleGrp.append("circle").attr("class", TOP_LEFT_CLASS);
    handleGrp.append("circle").attr("class", BOTTOM_RIGHT_CLASS);

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
    grps.select("." + TOP_LEFT_CLASS)
        .attr("cx", function(d) { return d.x; })
        .attr("cy", function(d) { return d.y; })
        .attr("r", HANDLE_RADIUS )
        .on("click", function(d) { console.log(d); })
        .call(dragTopLeftHandle);
    
    // set attributes for the bottom-right set of handles (i.e. circle elements) 
    grps.select("." + BOTTOM_RIGHT_CLASS)
        .attr("cx", function(d) { return d.x + d.width; })
        .attr("cy", function(d) { return d.y + d.height; })
        .attr("r", HANDLE_RADIUS )
        .on("click", function(d) { console.log(d); })
        .call(dragBottomRightHandle);
}

function deleteRegionsAndRedraw(extraData) {
    const CONFIG = JSON.parse(document.getElementById("config-id").textContent);
    const REGION_GRP = CONFIG.CONSTANTS.CLASSES.REGION;
    const IMG = document.getElementById(CONFIG.HTML.APP.IMAGE_PANE.IMAGE.ID);

    // get the current data (i.e. x,y,width,height all using image coords)
    const data = d3.selectAll("." + REGION_GRP).data();
    // rescale to put x,y,width,height on scale of [0,1]
    const rescaledData = rescaleDataToRelativeCoords(data, startWidth, startHeight);
    // if there's extra data to add (e.g. from Azure obj detection), append it
    if(extraData !== undefined) {
        extraData.forEach( function(elem) { 
            rescaledData.push(elem);
        });
    }

    // remove the old SVGs
    d3.selectAll("svg").remove();
    // get the x,y,width,height vals for the new window size
    const newData = rescaleDataToAbsoluteCoords(rescaledData, IMG.clientWidth, IMG.clientHeight);
    // regenerate the SVG, image and resizable boxes
    const svg = createSvg(CONFIG.HTML.APP.IMAGE_PANE.CONTAINER.ID,
        CONFIG.HTML.APP.IMAGE_PANE.SVG.ID,
        CONFIG.HTML.APP.IMAGE_PANE.SVG.CLASS,
        IMG.clientWidth, 
        IMG.clientHeight);
    createRegions(svg, newData);
}

// ================================================================================================
// CALLBACKS
// ================================================================================================

/**
 * @description: callback that deletes a single resizable region.
 * @param: regionGrp, group of 3 x SVG elements (1 x 'body' rect element and 2 x 'handle' 
 * circle elements) that fired the event; e.g the rect or handle that was double-clicked 
 * by the user.
 * @returns: none.
 * @throws: none.
 * @todo: none.
 */
function deleteRegionGrp(regionGroup) {
    console.log("Delete region");
    d3.select(regionGroup).remove();
}

/**
 * @description: callback to drag a resizable region (i.e. rect body and handles). The 
 * region cannot be dragged outside the edges of the image. Callback is bound to the 
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
function dragRegion(d) {    
    // Get constants from config.json
    const CONFIG = JSON.parse(document.getElementById("config-id").textContent);
    const HANDLE_CLASS = CONFIG.CONSTANTS.CLASSES.HANDLE;
    const BOTTOM_RIGHT_CLASS = CONFIG.CONSTANTS.CLASSES.BOTTOM_RIGHT_HANDLE;
    const TOP_LEFT_CLASS = CONFIG.CONSTANTS.CLASSES.TOP_LEFT_HANDLE;
    
    const IMG = document.getElementById(CONFIG.HTML.APP.IMAGE_PANE.IMAGE.ID);
    const IMG_WIDTH = IMG.clientWidth;
    const IMG_HEIGHT = IMG.clientHeight;

    // The Math.min and Math.max prevent the regions being dragged outside the image
    d.x = Math.min(Math.max(d3.event.x, 0), IMG_WIDTH - d.width);
    d.y = Math.min(Math.max(d3.event.y, 0), IMG_HEIGHT - d.height);

    // start by moving the rect element
    d3.select(this)
        .attr("x", d.x)
        .attr("y", d.y);
    
    // get the parent group of the rect element 
    const regionGroup = d3.select(this).node().parentNode;

    // get the bottom-right circle, and set the new coords    
    d3.select(regionGroup).select("." + HANDLE_CLASS).select("." + BOTTOM_RIGHT_CLASS)
        .attr("cx", d.x + d.width)
        .attr("cy", d.y + d.height);
    
    // get the bottom-right circle, and set the new coords
    d3.select(regionGroup).select("." + HANDLE_CLASS).select("." + TOP_LEFT_CLASS)
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
 * @description: callback to resize the region when the top-left handle is dragged.
 * The handle cannot be dragged outside the image boundaries, and the region has a
 * minimum width and height (which also prevents "inversions" of the region, where
 * the top-left handle could become the bottom-right handle).
 * @param: d, object array, the data bound to the calling element (i.e. the top-left 
 * circle element). 
 * Each object is of format {"x": number, "y": number, "width": number, "height": number}
 * @returns: none.
 * @throws: none.
 * @todo: none.
 */
function dragTlHandle(d) {
    // Get constants from config.json
    const CONFIG = JSON.parse(document.getElementById("config-id").textContent);
    const MIN_RECT_WIDTH = CONFIG.CONSTANTS.VALUES.MIN_RECT_WIDTH;
    const MIN_RECT_HEIGHT = CONFIG.CONSTANTS.VALUES.MIN_RECT_HEIGHT;

    console.log("Dragging top-left"); 

    // navigate up the SVG element tree to the top-level group
    const handleGroup = d3.select(this).node().parentNode;
    const regionGroup = d3.select(handleGroup).node().parentNode;
    
    // Ensure the region  doesn't go below the min size, or outside the edges of the image
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
    d3.select(regionGroup).select("rect")
        .attr("x", d.x)
        .attr("y", d.y)
        .attr("width", d.width)
        .attr("height", d.height);
}

/**
 * @description: callback to resize the region when the bottom-right handle is dragged.
 * The handle cannot be dragged outside the image boundaries, and the region has a
 * minimum width and height (which also prevents "inversions" of the region, where
 * the bottom-right handle could become the top-left handle).
 * @param: d, object array, the data bound to the calling element (i.e. the top-left 
 * circle element). 
 * Each object is of format {"x": number, "y": number, "width": number, "height": number}
 * @returns: none.
 * @throws: none.
 * @todo: none.
 */
function dragBrHandle(d) {
    // Get constants from config.json
    const CONFIG = JSON.parse(document.getElementById("config-id").textContent);
    const MIN_RECT_WIDTH = CONFIG.CONSTANTS.VALUES.MIN_RECT_WIDTH;
    const MIN_RECT_HEIGHT = CONFIG.CONSTANTS.VALUES.MIN_RECT_HEIGHT;

    const IMG = document.getElementById(CONFIG.HTML.APP.IMAGE_PANE.IMAGE.ID);
    const IMG_WIDTH = IMG.clientWidth;
    const IMG_HEIGHT = IMG.clientHeight;

    console.log("Dragging bottom-right");       
    
    // navigate up the SVG element tree to the top-level group
    const handleGroup = d3.select(this).node().parentNode;
    const regionGroup = d3.select(handleGroup).node().parentNode;
    
    // Set width and height so that the region doesn't go below the min size, or outside
    // the edges of the image    
    d.width = Math.min(Math.max(d.width + d3.event.dx, MIN_RECT_WIDTH), IMG_WIDTH - d.x);
    d.height = Math.min(Math.max(d.height + d3.event.dy, MIN_RECT_HEIGHT), IMG_HEIGHT - d.y);
    
    // move the handle to the new position 
    d3.select(this)
        .attr("cx", d.x + d.width)
        .attr("cy", d.y + d.height); 

    // resize the rect element
    d3.select(regionGroup).select("rect")
        .attr("width", d.width)
        .attr("height", d.height);               
}


/** 
 * @todo: consider - should this (and the two fns above) be moved into the driver function instead?
 * Arguments both ways I think.
*/
function clickAddRegion() {
    const CONFIG = JSON.parse(document.getElementById("config-id").textContent);
    const REGION_CLASS = CONFIG.CONSTANTS.CLASSES.REGION;
    const DEFAULT_RECT_WIDTH = CONFIG.CONSTANTS.VALUES.DEFAULT_RECT_WIDTH;
    const DEFAULT_RECT_HEIGHT = CONFIG.CONSTANTS.VALUES.DEFAULT_RECT_HEIGHT;

    // get the new coordinates and create a data object
    console.log("Clicked Add Region");
    try {
        const coords = getNewRegionLocation();
        const newData = {"x": coords[0],
                        "y": coords[1],
                        "width": DEFAULT_RECT_WIDTH,
                        "height": DEFAULT_RECT_HEIGHT
                        };
        // add the new data to the existing array
        const data = d3.selectAll("." + REGION_CLASS).data();
        data.push(newData);

        /**************************************************************************************
         * NOTE: the below is not the best way to achieve the goal. It *should* be possible to 
         * to do this via d3 enter() and exit(), just updating the data; but I can't get it to 
         * work properly, and does what I want, so...
         ***************************************************************************************/
        // delete all existing regions, and recreate them with the new data
        d3.selectAll("." + REGION_CLASS).remove();
        createRegions(d3.select("svg"), data);
    }
    catch(err) {
        console.log(err);
        console.error(err.message + "; coords: (" + err.coords[0] + "," + err.coords[1] + ")");
        // alert(err.message);
    }
}

function clickFindRegions() {
    const CONFIG = JSON.parse(document.getElementById("config-id").textContent);
    const FILE_DATA_KEY = CONFIG.HTML.APP.IMAGE_PANE.IMAGE.FILE_DATA_KEY;

    // get the new coordinates and create a data object
    console.log("Clicked Find Regions");

    try {
        const imageData = sessionStorage.getItem(FILE_DATA_KEY);
        const b64start = imageData.indexOf(",") + 1;        
        sendImageDataToServer(imageData.slice(b64start));
    }
    catch(err) {
        console.error(err);
    }    
}
// ================================================================================================
// CUSTOM EXCEPTIONS
// ================================================================================================

/**
 * @description: exception raised if the user tries to create a new region and there isn't enough
 * space in the image for it.
 * @param: 
 *  - x, number, x-coordinate of the last region created. 
 *  - y, number, y-coordinate of the last region created. 
 * @returns: none.
 * @throws: none.
 * @todo: none.
 */
function OutOfBoundsException(x,y) {
    this.coords = [x,y];
    this.message = "Out of space - no more regions permitted";
}


// ================================================================================================
// REGION LOCATION FUNCTIONS
// ================================================================================================

/**
 * @description: function to decide on coords for a new region. By default, new regions are placed in 
 * the top-left corner of the image, and then tiled horizontally in rows (starting a new row when 
 * the next region would go outside the edge of the image). When the image is completely tiled, an 
 * exception is thrown.
 * A new region cannot be colocated with an existing region.
 * @param: none.
 * @returns: [x,y], array of numbers giving the [x,y] coords of the new location IN THE IMAGE 
 * COORDINATE SPACE (i.e. using image coords, NOT whole page coords).
 * @throws: OutOfBoundsException if the image is believed to be full of regions.
 * @todo: consider adding a control that allows users to set minimum region size.
 */
function getNewRegionLocation() {
    // Get constants from config.json
    const CONFIG = JSON.parse(document.getElementById("config-id").textContent);
    const DEFAULT_RECT_WIDTH = CONFIG.CONSTANTS.VALUES.DEFAULT_RECT_WIDTH;
    const DEFAULT_RECT_HEIGHT = CONFIG.CONSTANTS.VALUES.DEFAULT_RECT_HEIGHT;

    const IMG = document.getElementById(CONFIG.HTML.APP.IMAGE_PANE.IMAGE.ID);
    const IMG_WIDTH = IMG.clientWidth;
    const IMG_HEIGHT = IMG.clientHeight;

    let x = 0;
    let y = 0;
    while(!isNewLocationFree(x, y)) {
        // debugger;
        // Cases:
        // 1. next rect will go over the image edge in x and y: throw exception        
        if (x + 2 * DEFAULT_RECT_WIDTH > IMG_WIDTH) {            
            if (y + 2 * DEFAULT_RECT_HEIGHT > IMG_HEIGHT) {                
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
 * @description: checks if the proposed new location overlaps with an existing region. regions are
 * considered to be 'too overlapping' if the difference between the top-left corner of the new
 * region is less than 2 handle-radii from an existing region.
 * @param: 
 *  - x, number, proposed x-coordinate of the new region. 
 *  - y, number, proposed y-coordinate of the new region. 
 * @returns: locationFree, boolean. True if the proposed location is ok, false if not.
 * @throws: custom exceptions.
 * @todo: change exceptions to be functions, as per OutOfBoundsException().
 */
function isNewLocationFree(x,y) {
    // Get constants from config.json
    const CONFIG = JSON.parse(document.getElementById("config-id").textContent);
    const HANDLE_RADIUS = CONFIG.CONSTANTS.VALUES.HANDLE_RADIUS;

    const IMG = document.getElementById(CONFIG.HTML.APP.IMAGE_PANE.IMAGE.ID);
    const IMG_WIDTH = IMG.clientWidth;
    const IMG_HEIGHT = IMG.clientHeight;

    // some error checking on the parameters
    if (typeof(x) !== "number" || isNaN(x)) { throw "x coord is not a number"; }
    if (typeof(x) !== "number" || isNaN(y)) { throw "y coord is not a number"; }    
    if (x < 0 || x > IMG_WIDTH) { throw "x coord is outside image bounds"; }
    if (y < 0 || y > IMG_HEIGHT) { throw "y coord is outside image bounds"; }

    // main section of function
    let locationFree = true;
    d3.selectAll("rect").each(function() {
        const rect = d3.select(this);
        if( (Math.abs(rect.attr("x") - x) <= 2 * HANDLE_RADIUS) && 
            (Math.abs(rect.attr("y") - y) <= 2 * HANDLE_RADIUS) ) {
            locationFree = false;
        }
    });
    return locationFree;
}

// ================================================================================================
// DATA RESCALE FUNCTIONS
// ================================================================================================
function rescaleDataToRelativeCoords(data, imgWidth, imgHeight) {
    const scaledData = data.map(function(d) {
        return {"x": d.x / imgWidth,
                "y": d.y / imgHeight,
                "width": d.width / imgWidth,
                "height": d.height / imgHeight
                };
    })

    return scaledData;
}

// NOTE: 'data' parameter in the below is rescaled on [0,1]!! <= include in @params
function rescaleDataToAbsoluteCoords(data, imgWidth, imgHeight) {
    const scaledData = data.map(function(d) {
        return {"x": d.x * imgWidth,
                "y": d.y * imgHeight,
                "width": d.width * imgWidth,
                "height": d.height * imgHeight
                };
    })

    return scaledData;
}

// ================================================================================================
// AJAX REQUESTS
// ================================================================================================
function sendImageDataToServer(imageData){
    
    // ----------
    // This section is from the Django docs, to reduce Cross Site Request Forgeries
    // https://docs.djangoproject.com/en/3.0/ref/csrf/#ajax
    const csrftoken = jQuery("[name=csrfmiddlewaretoken]").val();    

    function csrfSafeMethod(method) {
        // these HTTP methods do not require CSRF protection
        return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
    }
    // ----------

    // Now make the AJAX POST request and send imageData to the Django server
    $.ajax({     
        type: "POST",
        data: { "data": imageData },
        dataType: "json",
        timeout: 10000,
        beforeSend: function(jqXHR, settings) {
            // if not safe, set csrftoken
            if (!csrfSafeMethod(settings.type) && !this.crossDomain) {               
                jqXHR.setRequestHeader("X-CSRFToken", csrftoken);
            }
        }
    })
    .done(function(returnData) {
        console.log("AJAX RESPONSE SUCCEEDED"); 
        // deleteRegionsAndRedraw(returnData["data"]);  
    })
    .fail(function(jqXHR) {
        console.log("AJAX RESPONSE FAILED");
        console.log("Status: " +  jqXHR.status);
        console.log("Status text: " + jqXHR.statusText);
        console.log("Response type: " + jqXHR.responseType);
        console.log("Response text: " + jqXHR.responseText);
        console.log("Ready state: " + jqXHR.readyState);

        if(jqXHR.statusText === "timeout") {
            alert("The request timed out");
        }
    }) 
}
