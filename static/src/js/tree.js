
// constructTangleLayout = (levels, options={}) => {
//     // precompute level depth
//     levels.forEach((l, i) => l.forEach(n => (n.level = i)));
  
//     var nodes = levels.reduce((a, x) => a.concat(x), []);
//     var nodes_index = {};
//     nodes.forEach(d => (nodes_index[d.id] = d));
  
//     // objectification
//     nodes.forEach(d => {
//       d.parents = (d.parents === undefined ? [] : d.parents).map(
//         p => nodes_index[p]
//       );
//     });
  
//     // precompute bundles
//     levels.forEach((l, i) => {
//       var index = {};
//       l.forEach(n => {
//         if (n.parents.length == 0) {
//           return;
//         }
  
//         var id = n.parents
//           .map(d => d.id)
//           .sort()
//           .join('-X-');
//         if (id in index) {
//           index[id].parents = index[id].parents.concat(n.parents);
//         } else {
//           index[id] = { id: id, parents: n.parents.slice(), level: i, span: i - d3.min(n.parents, p => p.level) };
//         }
//         n.bundle = index[id];
//       });
//       l.bundles = Object.keys(index).map(k => index[k]);
//       l.bundles.forEach((b, i) => (b.i = i));
//     });
  
//     var links = [];
//     nodes.forEach(d => {
//       d.parents.forEach(p =>
//         links.push({ source: d, bundle: d.bundle, target: p })
//       );
//     });
  
//     var bundles = levels.reduce((a, x) => a.concat(x.bundles), []);
  
//     // reverse pointer from parent to bundles
//     bundles.forEach(b =>
//       b.parents.forEach(p => {
//         if (p.bundles_index === undefined) {
//           p.bundles_index = {};
//         }
//         if (!(b.id in p.bundles_index)) {
//           p.bundles_index[b.id] = [];
//         }
//         p.bundles_index[b.id].push(b);
//       })
//     );
  
//     nodes.forEach(n => {
//       if (n.bundles_index !== undefined) {
//         n.bundles = Object.keys(n.bundles_index).map(k => n.bundles_index[k]);
//       } else {
//         n.bundles_index = {};
//         n.bundles = [];
//       }
//       n.bundles.sort((a,b) => d3.descending(d3.max(a, d => d.span), d3.max(b, d => d.span)))
//       n.bundles.forEach((b, i) => (b.i = i));
//     });
  
//     links.forEach(l => {
//       if (l.bundle.links === undefined) {
//         l.bundle.links = [];
//       }
//       l.bundle.links.push(l);
//     });
  
//     // layout
//     const padding = 8;
//     const node_height = 22;
//     const node_width = 70;
//     const bundle_width = 14;
//     const level_y_padding = 16;
//     const metro_d = 4;
//     const min_family_height = 22;
    
//     options.c ||= 16;
//     const c = options.c;
//     options.bigc ||= node_width+c;
  
//     nodes.forEach(
//       n => (n.height = (Math.max(1, n.bundles.length) - 1) * metro_d)
//     );
  
//     var x_offset = padding;
//     var y_offset = padding;
//     levels.forEach(l => {
//       x_offset += l.bundles.length * bundle_width;
//       y_offset += level_y_padding;
//       l.forEach((n, i) => {
//         n.x = n.level * node_width + x_offset;
//         n.y = node_height + y_offset + n.height / 2;
  
//         y_offset += node_height + n.height;
//       });
//     });
  
//     var i = 0;
//     levels.forEach(l => {
//       l.bundles.forEach(b => {
//         b.x =
//           d3.max(b.parents, d => d.x) +
//           node_width +
//           (l.bundles.length - 1 - b.i) * bundle_width;
//         b.y = i * node_height;
//       });
//       i += l.length;
//     });
  
//     links.forEach(l => {
//       l.xt = l.target.x;
//       l.yt =
//         l.target.y +
//         l.target.bundles_index[l.bundle.id].i * metro_d -
//         (l.target.bundles.length * metro_d) / 2 +
//         metro_d / 2;
//       l.xb = l.bundle.x;
//       l.yb = l.bundle.y;
//       l.xs = l.source.x;
//       l.ys = l.source.y;
//     });
    
//     // compress vertical space
//     var y_negative_offset = 0;
//     levels.forEach(l => {
//       y_negative_offset +=
//         -min_family_height +
//           d3.min(l.bundles, b =>
//             d3.min(b.links, link => link.ys - 2*c - (link.yt + c))
//           ) || 0;
//       l.forEach(n => (n.y -= y_negative_offset));
//     });
  
//     links.forEach(l => {
//       l.yt =
//         l.target.y +
//         l.target.bundles_index[l.bundle.id].i * metro_d -
//         (l.target.bundles.length * metro_d) / 2 +
//         metro_d / 2;
//       l.ys = l.source.y;
//       l.c1 = l.source.level - l.target.level > 1 ? Math.min(options.bigc, l.xb-l.xt, l.yb-l.yt)-c : c;
//       l.c2 = c;
//     });
  
//     var layout = {
//       width: d3.max(nodes, n => n.x) + node_width + 2 * padding,
//       height: d3.max(nodes, n => n.y) + node_height / 2 + 2 * padding,
//       node_height,
//       node_width,
//       bundle_width,
//       level_y_padding,
//       metro_d
//     };
  
//     return { levels, nodes, nodes_index, links, bundles, layout };
//   }
  
//   renderChart = (data, options={}) => {
//     options.color ||= (d, i) => color(i)
    
//     const tangleLayout = constructTangleLayout(data, options);
  
//     svg = document.createElementNS("http://www.w3.org/2000/svg", "svg");
//     svg.setAttributeNS("http://www.w3.org/2000/xmlns/", "xmlns:xlink", "http://www.w3.org/1999/xlink");
//     svg.setAttribute('width', tangleLayout.layout.width)
//     // svg.setAttribute('height', tangleLayout.layout.height)
//     svg.setAttribute('height', 450) // this is bad

//     const container = document.createElementNS("http://www.w3.org/2000/svg", "g");
//     container.setAttribute("transform", "translate(0, 0) scale(1)");

//     container.innerHTML = `
//         <style>
//             text {
//                 font-family: sans-serif;
//                 font-size: 10px;
//             }
//             .node {
//                 stroke-linecap: round;
//             }
//             .link {
//                 fill: none;
//             }
//         </style>
  
//         ${tangleLayout.bundles.map((b, i) => {
//             let d = b.links
//                 .map(
//                 l => `
//                 M${l.xt} ${l.yt}
//                 L${l.xb - l.c1} ${l.yt}
//                 A${l.c1} ${l.c1} 90 0 1 ${l.xb} ${l.yt + l.c1}
//                 L${l.xb} ${l.ys - l.c2}
//                 A${l.c2} ${l.c2} 90 0 0 ${l.xb + l.c2} ${l.ys}
//                 L${l.xs} ${l.ys}`
//                 )
//                 .join("");
//             return `
//                 <path class="link" d="${d}" stroke="gray" stroke-width="5"/>
//                 <path class="link" d="${d}" stroke="purple" stroke-width="2"/>
//             `;
//             })}
  
//         ${tangleLayout.nodes.map(
//             n => `
//             <path class="selectable node" data-id="${
//                 n.id
//             }" stroke="black" stroke-width="8" d="M${n.x} ${n.y - n.height / 2} L${
//                 n.x
//             } ${n.y + n.height / 2}"/>
//             <path class="node" stroke="white" stroke-width="4" d="M${n.x} ${n.y -
//                 n.height / 2} L${n.x} ${n.y + n.height / 2}"/>
        
//             <text class="selectable" data-id="${n.id}" x="${n.x + 4}" y="${n.y -
//                 n.height / 2 -
//                 4}" stroke="green" stroke-width="2">${n.id}</text>
//             <text x="${n.x + 4}" y="${n.y -
//                 n.height / 2 -
//                 4}" style="pointer-events: none;">${n.id}</text>
//             `
//         )}
//     `
//     svg.appendChild(container);
//     return svg;
//   }


// // Retrieve json data from the document
// const fam_data = [
// [{ id: 'Chaos' }],
// [{ id: 'Gaea', parents: ['Chaos'] }, { id: 'Uranus' }],
// [
//     { id: 'Oceanus', parents: ['Gaea', 'Uranus'] },
//     { id: 'Thethys', parents: ['Gaea', 'Uranus'] },
//     { id: 'Pontus' },
//     { id: 'Rhea', parents: ['Gaea', 'Uranus'] },
//     { id: 'Cronus', parents: ['Gaea', 'Uranus'] },
//     { id: 'Coeus', parents: ['Gaea', 'Uranus'] },
//     { id: 'Phoebe', parents: ['Gaea', 'Uranus'] },
//     { id: 'Crius', parents: ['Gaea', 'Uranus'] },
//     { id: 'Hyperion', parents: ['Gaea', 'Uranus'] },
//     { id: 'Iapetus', parents: ['Gaea', 'Uranus'] },
//     { id: 'Thea', parents: ['Gaea', 'Uranus'] },
//     { id: 'Themis', parents: ['Gaea', 'Uranus'] },
//     { id: 'Mnemosyne', parents: ['Gaea', 'Uranus'] }
// ],
// [
//     { id: 'Doris', parents: ['Oceanus', 'Thethys'] },
//     { id: 'Neures', parents: ['Pontus', 'Gaea'] },
//     { id: 'Dionne' },
//     { id: 'Demeter', parents: ['Rhea', 'Cronus'] },
//     { id: 'Hades', parents: ['Rhea', 'Cronus'] },
//     { id: 'Hera', parents: ['Rhea', 'Cronus'] },
//     { id: 'Alcmene' },
//     { id: 'Zeus', parents: ['Rhea', 'Cronus'] },
//     { id: 'Eris' },
//     { id: 'Leto', parents: ['Coeus', 'Phoebe'] },
//     { id: 'Amphitrite' },
//     { id: 'Medusa' },
//     { id: 'Poseidon', parents: ['Rhea', 'Cronus'] },
//     { id: 'Hestia', parents: ['Rhea', 'Cronus'] }
// ],
// [
//     { id: 'Thetis', parents: ['Doris', 'Neures'] },
//     { id: 'Peleus' },
//     { id: 'Anchises' },
//     { id: 'Adonis' },
//     { id: 'Aphrodite', parents: ['Zeus', 'Dionne'] },
//     { id: 'Persephone', parents: ['Zeus', 'Demeter'] },
//     { id: 'Ares', parents: ['Zeus', 'Hera'] },
//     { id: 'Hephaestus', parents: ['Zeus', 'Hera'] },
//     { id: 'Hebe', parents: ['Zeus', 'Hera'] },
//     { id: 'Hercules', parents: ['Zeus', 'Alcmene'] },
//     { id: 'Megara' },
//     { id: 'Deianira' },
//     { id: 'Eileithya', parents: ['Zeus', 'Hera'] },
//     { id: 'Ate', parents: ['Zeus', 'Eris'] },
//     { id: 'Leda' },
//     { id: 'Athena', parents: ['Zeus'] },
//     { id: 'Apollo', parents: ['Zeus', 'Leto'] },
//     { id: 'Artemis', parents: ['Zeus', 'Leto'] },
//     { id: 'Triton', parents: ['Poseidon', 'Amphitrite'] },
//     { id: 'Pegasus', parents: ['Poseidon', 'Medusa'] },
//     { id: 'Orion', parents: ['Poseidon'] },
//     { id: 'Polyphemus', parents: ['Poseidon'] }
// ],
// [
//     { id: 'Deidamia' },
//     { id: 'Achilles', parents: ['Peleus', 'Thetis'] },
//     { id: 'Creusa' },
//     { id: 'Aeneas', parents: ['Anchises', 'Aphrodite'] },
//     { id: 'Lavinia' },
//     { id: 'Eros', parents: ['Hephaestus', 'Aphrodite'] },
//     { id: 'Helen', parents: ['Leda', 'Zeus'] },
//     { id: 'Menelaus' },
//     { id: 'Polydueces', parents: ['Leda', 'Zeus'] }
// ],
// [
//     { id: 'Andromache' },
//     { id: 'Neoptolemus', parents: ['Deidamia', 'Achilles'] },
//     { id: 'Aeneas(2)', parents: ['Creusa', 'Aeneas'] },
//     { id: 'Pompilius', parents: ['Creusa', 'Aeneas'] },
//     { id: 'Iulus', parents: ['Lavinia', 'Aeneas'] },
//     { id: 'Hermione', parents: ['Helen', 'Menelaus'] }
// ]
// ]
// treeData = JSON.parse(document.getElementById('loaded_data').innerHTML.replaceAll("\'", "\"").replaceAll("False", "\"\""));

// // Create tree layout and add it to the container
// svg = renderChart(fam_data);


// In this representation, 'children' does not refer to a human parent-child relationship, 
// but rather the position of the tree entry relative to the others
data = {
  "name": "Grandchild 1",
  "children": [
    {
      "name": "Parent 1",
      "children": [
        {
          "name": "Grandparent 1",
          "children": [],
        },
        {
          "name": "Grandparent 2",
          "children": [],
        },
      ],
    },
    {
      "name": "Parent 2",
      "children": [
        {
          "name": "Grandparent 3",
          "children": [],
        },
        {
          "name": "Grandparent 4",
          "children": [
            {
              "name": "Great Grandparent",
              "children": [
                {
                  "name": "Great Great Grandparent",
                  "children": [
                    {
                      "name": "Great Great Great Grandparent",
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
}

const width = document.getElementById("tree_container").clientWidth;

// Compute the tree height; this approach will allow the height of the
// SVG to scale according to the breadth (width) of the tree layout.
const root = d3.hierarchy(data);
const dx = 50;
const dy = width / (root.height + 1) ;

// Create a tree layout.
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
// The circle is color #999 if the entry has children, and #555 if it does not
node.append("circle")
    .attr("fill", d => d.children ? "black" : "lightgray")
    .attr("r", 2.5);

// The text associated with each entry, in this case each entry's name
// Each entry is given class 'node' for css purposes
node.append("text")
    .attr("dy", "0.31em") //specifies vertical offset of text to circle
    .attr("x", 6) //specifies horizontal offset of text to circle
    .attr("text-anchor", "start") //specifies where text is in relation to the circle
    .text(d => d.data.name) //the text that is displayed on the page
  .clone(true).lower()
    .attr("stroke", "white");

// Add an action listener to each node to handle
const nodes = document.getElementsByClassName("node")
console.log(nodes)
console.log(nodes.item(0))
for (n of nodes) {
  console.log(n)
  n.addEventListener("click", (event) => {
    console.log(event)
  })
}

tree_container = d3.select(document.getElementById('tree_container')).node()
tree_container.appendChild(svg.node());

// Bounding for zoom
const containerRect = tree_container.getBoundingClientRect();
