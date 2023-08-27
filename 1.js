// Set up the SVG canvas dimensions
const width = 928;
const root = d3.hierarchy(fam_data); //treeData.members
const dx = 10
const dy = width / (root.height + 1)

// Create a tree layout
const tree = d3.tree().nodeSize([dx, dy]);

// Assign position of each node
tree(root);

// Compute horizontal extent of the tree
let x0 = Infinity;
  let x1 = -x0;
  root.each(d => {
    if (d.x > x1) x1 = d.x;
    if (d.x < x0) x0 = d.x;
  });

// Compute the adjusted height of the tree.
const height = x1 - x0 + dx * 2;

// Create the SVG element
const svg = d3.create("svg")
    .attr("width", width)
    .attr("height", height)
    .attr("viewBox", [-dy / 2, x0 - dx, width, height])
    .attr("style", "max-width: 100%; height: auto; font: 10px sans-serif;");

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
        .attr("transform", d => `translate(${d.y},${d.x})`);

node.append("circle")
    .attr("fill", d => d.children ? "#555" : "#999")
    .attr("r", 2.5);

node.append("text")
    .attr("dy", "0.31em")
    .attr("x", d => d.children ? -6 : 6)
    .attr("text-anchor", d => d.children ? "end" : "start")
    .text(d => d.data.name)
    .clone(true).lower()
        .attr("stroke", "white");

console.log(svg)
console.log(document.getElementById('tree_container'))
d3.select(document.getElementById('tree_container')).append(svg)