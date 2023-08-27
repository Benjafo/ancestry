// Add a CSS class to the 'tree_container' element when the mouse enters
tree_container.addEventListener("mouseenter", () => {
    tree_container.classList.add("hover-pointer");
});

// Remove the CSS class when the mouse leaves
tree_container.addEventListener("mouseleave", () => {
    tree_container.classList.remove("hover-pointer");
});