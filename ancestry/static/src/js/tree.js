// In this representation, 'children' does not refer to a human parent-child relationship, 
// but rather the position of the tree entry relative to the others

// The actual data to use
const treeData = JSON.parse(document.getElementById('loaded_data').innerHTML.replaceAll("\'", "\"").replaceAll("False", "\"\""));

// Test data
const data_childAsRoot = {
  "name": "Grandchild 1",
  "gender": "",
  "children": [
    {
      "name": "Parent 1",
      "gender": "male",
      "children": [
        {
          "name": "Grandparent 1",
          "gender": "male",
          "children": [],
        },
        {
          "name": "Grandparent 2",
          "gender": "female",
          "children": [],
        },
      ],
    },
    {
      "name": "Parent 2",
      "gender": "female",
      "children": [
        {
          "name": "Grandparent 3",
          "gender": "male",
          "children": [],
        },
        {
          "name": "Grandparent 4",
          "gender": "female",
          "children": [
            {
              "name": "Great Grandparent",
              "gender": "male",
              "children": [
                {
                  "name": "Great Great Grandparent",
                  "gender": "female",
                  "children": [
                    {
                      "name": "Great Great Great Grandparent",
                      "gender": "",
                      "children": [],
                    }
                  ],
                }
              ],
            }
          ],
        },
      ],
    },
  ],
};
const data_parentAsRoot = {
  'name': 'God',
  'gender': '',
  'children': [
    {'name': 'Chaos', 'gender': 'male', 'children': [
        {'name': 'Gaea', 'gender': 'female', 'children': [
            {'name': 'Uranus', 'gender': 'male', 'children': [
                {'name': 'Oceanus', 'gender': 'male', 'children': []},
                {'name': 'Thethys', 'gender': 'female', 'children': []}
            ]}
        ]}
    ]},
    {'name': 'Rhea', 'gender': 'female', 'children': [
        {'name': 'Cronus', 'gender': 'male', 'children': [
            {'name': 'Demeter', 'gender': 'female', 'children': []},
            {'name': 'Hades', 'gender': 'male', 'children': []},
            {'name': 'Hera', 'gender': 'female', 'children': [
                {'name': 'Hephaestus', 'gender': 'male', 'children': []},
                {'name': 'Hebe', 'gender': 'female', 'children': []}
            ]},
            {'name': 'Zeus', 'gender': 'male', 'children': [
                {'name': 'Athena', 'gender': 'female', 'children': []},
                {'name': 'Apollo', 'gender': 'male', 'children': []},
                {'name': 'Artemis', 'gender': 'female', 'children': []}
            ]}
        ]}
    ]},
    {'name': 'Doris', 'gender': 'female', 'children': [
        {'name': 'Neures', 'gender': 'male', 'children': []}
    ]},
    {'name': 'Poseidon', 'gender': 'male', 'children': [
        {'name': 'Triton', 'gender': 'male', 'children': []},
        {'name': 'Pegasus', 'gender': 'male', 'children': []},
        {'name': 'Orion', 'gender': 'male', 'children': []},
        {'name': 'Polyphemus', 'gender': 'male', 'children': []}
    ]},
    {'name': 'Achilles', 'gender': 'male', 'children': [
        {'name': 'Neoptolemus', 'gender': 'male', 'children': []}
    ]},
    {'name': 'Aeneas', 'gender': 'male', 'children': [
        {'name': 'Aeneas Jr.', 'gender': 'male', 'children': [
            {'name': 'Pompilius', 'gender': 'male', 'children': []}
        ]},
        {'name': 'Lavinia', 'gender': 'female', 'children': [
            {'name': 'Iulus', 'gender': 'male', 'children': []}
        ]}
    ]},
    {'name': 'Helen', 'gender': 'female', 'children': [
        {'name': 'Hermione', 'gender': 'female', 'children': []}
    ]}
  ]
};

console.log(treeData)

// Create the representation
const root = d3.hierarchy(treeData);

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

// A circle icon to represent each entry in the tree
// node.append("circle")
//     .attr("fill", d => d.children ? "black" : "lightgray") // fill color #999 if the entry has children, and #555 if it does not
//     .attr("r", 3); // radius of the circle

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
    nodes[i].addEventListener("click", (event) => {
      alert(event.target.__data__.data.name)
    })
  }
});

const tree_container = d3.select(document.getElementById('tree_container')).node()
tree_container.appendChild(svg.node());

// Bounding for zoom
const containerRect = tree_container.getBoundingClientRect();