"use strict";

// console.log("Hello, this is the index");
function main() {    
    const CONFIG = JSON.parse(document.getElementById("config-id").textContent);
    const CONTAINER = document.getElementById(CONFIG.HTML.APP.IMAGE_PANE.ID);
    const WIDTH = CONTAINER.clientWidth;
    const HEIGHT = (WIDTH / 4608) * 3456;
    const FILE = "C:\\Users\\al_vi\\OneDrive\\Code\\DesignThinkingToolset\\media\\test\\test_img.jpg"
    
    const svg = createSvg(CONFIG.HTML.APP.IMAGE_PANE.ID, WIDTH, HEIGHT);
    createImage(svg, FILE, WIDTH, HEIGHT);
}

main();
