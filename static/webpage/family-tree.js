// Set up the SVG canvas dimensions
const width = 800;
const height = 600;

// Create the SVG element
const svg = d3.select("#family-tree").append("svg")
    .attr("width", width)
    .attr("height", height);

// Create a tree layout
const treeLayout = d3.tree()
    .size([width, height - 100]);

// Fetch JSON data using fetch()
fetch("family-data.json")
    .then(response => response.json())
    .then(familyData => {
        // Convert the data to a hierarchical structure
        const root = d3.hierarchy(familyData);

        // Assigns the position of each node
        treeLayout(root);

        // Draw the links between nodes
        svg.selectAll(".link")
            .data(root.links())
            .enter().append("path")
            .attr("class", "link")
            .attr("d", d3.linkHorizontal()
                .x(d => d.y)
                .y(d => d.x));

        // Draw the nodes
        const nodes = svg.selectAll(".node")
            .data(root.descendants())
            .enter().append("g")
            .attr("class", "node")
            .attr("transform", d => `translate(${d.y},${d.x})`);

        nodes.append("circle")
            .attr("r", 4.5);

        nodes.append("text")
            .attr("dy", "0.31em")
            .attr("x", d => d.children ? -6 : 6)
            .attr("text-anchor", d => d.children ? "end" : "start")
            .text(d => d.data.name);
    })
    .catch(error => {
        console.error("Error loading family data:", error);
    });
