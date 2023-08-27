const container = svg.node().querySelector("g");
const transform = container.getAttribute("transform");
const [translate, scaleStr] = transform.split("scale(");
const [translateX, translateY] = translate
    .replace("translate(", "")
    .replace(")", "")
    .split(",");
    
const initialScale = parseFloat(scaleStr.replace(")", ""));
let initialTranslateX = parseFloat(translateX);
let initialTranslateY = parseFloat(translateY);

let isDragging = false;
let initialMouseX, initialMouseY;

tree_container.addEventListener("mousedown", (event) => {
    isDragging = true;
    initialMouseX = event.clientX;
    initialMouseY = event.clientY;

    const transformAttr = container.getAttribute("transform");
    const translateValues = transformAttr.match(/translate\(([^,]+),([^)]+)\)/);
    
    if (translateValues) {
        initialTranslateX = parseFloat(translateValues[1]);
        initialTranslateY = parseFloat(translateValues[2]);
    } else {
        initialTranslateX = 0;
        initialTranslateY = 0;
    }
});

window.addEventListener("mousemove", (event) => {
    if (!isDragging) return;

    const dx = event.clientX - initialMouseX;
    const dy = event.clientY - initialMouseY;
    
    const newTranslateX = initialTranslateX + dx / initialScale;
    const newTranslateY = initialTranslateY + dy / initialScale;

    const newTransform = `translate(${newTranslateX}, ${newTranslateY}) scale(1)`;
    container.setAttribute("transform", newTransform);
});

window.addEventListener("mouseup", () => {
    isDragging = false;
});
