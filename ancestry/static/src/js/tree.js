// In this representation, 'children' does not refer to a human parent-child relationship, 
// but rather the position of the tree entry relative to the others
const treeData = JSON.parse(document.getElementById('loaded_data').innerHTML.replaceAll("\'", "\"").replaceAll("False", "\"\""));

// Create the representation
const root = d3.hierarchy(treeData.members);

// Compute the tree height; this approach will allow the height of the
// SVG to scale according to the breadth (width) of the tree layout.
const width = document.getElementById("tree_container").clientWidth;
const dx = 60;
const dy = width / (root.height + 1) ;

// Create the tree layout
const tree = d3.tree().nodeSize([dx, dy]);

// Sort the tree and apply the layout.
root.sort((a, b) => d3.ascending(a.data.name, b.data.name));
tree(root);

// Compute the extent of the tree. Note that x and y are swapped here
// because in the tree layout, x is the breadth, but when displayed, the
// tree extends right rather than down.
let x0 = Infinity;
let x1 = -x0;
root.each(d => {
  if (d.x > x1) x1 = d.x;
  if (d.x < x0) x0 = d.x;
});

// Compute the adjusted height of the tree.
const height = x1 - x0 + dx * 2;

// The actual svg element that all entries will be added to
const svg = d3.create("svg")
    .attr("width", width)
    .attr("height", height)
    .attr("viewBox", [-dy / 3, x0 - dx, width, height])
    .attr("style", "max-width: 100%; height: auto; font: 14px sans-serif;");

const link = svg.append("g")
    .attr("fill", "none")
    .attr("stroke", "#555")
    .attr("stroke-opacity", 0.4)
    .attr("stroke-width", 1.5)
  .selectAll()
    .data(root.links())
    .join("path")
      .attr("d", d3.linkHorizontal()
          .x(d => d.y)
          .y(d => d.x));

const node = svg.append("g")
    .attr("stroke-linejoin", "round")
    .attr("stroke-width", 3)
  .selectAll()
  .data(root.descendants())
  .join("g")
    .attr("class", "node") //add node class to text
    .attr("transform", d => `translate(${d.y},${d.x})`);

// Profile picture for each entry
const path = "/ancestry/static/src/img/profile/"
node.append("image")
  .attr("xlink:href", d => path.concat(d.data.gender == "male" ? "M" : d.data.gender == "female" ? "F" : "X", ".JPG"))
  .attr("x", -20)
  .attr("y", -20)
  .attr("width", 40)
  .attr("height", 40);

// The text associated with each entry, in this case each entry's name
// Each entry is given class 'node' for css purposes
node.append("text")
    .attr("dy", "0.31em") // vertical offset of text to circle
    .attr("x", d => d.children ? -4 : 24) // horizontal offset of text to circle
    .attr("y", d => d.children ? -28 : 0) // vertical offset of text to circle
    .attr("text-anchor", d => d.children ? "middle" : "start") // where text is in relation to the circle
    .text(d => d.data.name) // text that is displayed on the page
  .clone(true).lower()
    .attr("stroke", "white");

// Add an action listener to each node to handle click
document.addEventListener("DOMContentLoaded", () => {
  const nodes = document.getElementsByClassName("node");
  for (let i = 0; i < nodes.length; i++) {
    nodes[i].addEventListener("click", (event) => openPopup(event))
  }
});

// Add to dom
const tree_container = d3.select(document.getElementById('tree_container')).node()
tree_container.appendChild(svg.node());

// Bounding for zoom
const containerRect = tree_container.getBoundingClientRect();