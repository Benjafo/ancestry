const zoom = (event) => {
    const container = svg.querySelector("g");
    const transform = container.getAttribute("transform");

    // Parse the existing transform attributes
    const [translate, scaleStr] = transform.split("scale(");
    const [translateX, translateY] = translate
        .replace("translate(", "")
        .replace(")", "")
        .split(",");
    
    const scale = parseFloat(scaleStr.replace(")", ""));
    const newScale = scale - event.deltaY * 0.0007; // Adjust the scaling factor as needed

    // Limit the minimum scale to prevent inversion
    const clampedScale = Math.max(0.1, newScale);

    // Calculate new translate values to keep the zoom centered
    const newTranslateX = parseFloat(translateX) + event.offsetX * (scale - clampedScale);
    const newTranslateY = parseFloat(translateY) + event.offsetY * (scale - clampedScale);

    // Apply the new transform to the container
    const newTransform = `translate(${newTranslateX}, ${newTranslateY}) scale(${clampedScale})`;
    container.setAttribute("transform", newTransform);
};

svg.node().addEventListener("wheel", (event) => {
    // Check if the event target is the SVG element
    if (
        event.target === svg &&
        event.clientX >= containerRect.left &&
        event.clientX <= containerRect.right &&
        event.clientY >= containerRect.top &&
        event.clientY <= containerRect.bottom
    ) {
        event.preventDefault(); // Prevent the default scroll behavior
        zoom(event);    // Call your updated zoom function
    }
});