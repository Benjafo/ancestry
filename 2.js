

treeData = [{
  "name": "Niclas Superlongsurname",
  "class": "man",
  "textClass": "emphasis",
  "marriages": [{
    "spouse": {
      "name": "Iliana",
      "class": "woman"
    },
    "children": [{
      "name": "James",
      "class": "man",
      "marriages": [{
        "spouse": {
          "name": "Alexandra",
          "class": "woman"
        },
        "children": [{
          "name": "Eric",
          "class": "man",
          "marriages": [{
            "spouse": {
              "name": "Eva",
              "class": "woman"
            }
          }]
        }, {
          "name": "Jane",
          "class": "woman"
        }, {
          "name": "Jasper",
          "class": "man"
        }, {
          "name": "Emma",
          "class": "woman"
        }, {
          "name": "Julia",
          "class": "woman"
        }, {
          "name": "Jessica",
          "class": "woman"
        }]
      }]
    }]
  }]
}]

tree = dTree.init(treeData, {
  target: "#graph",
  debug: true,
  height: 800,
  width: 1200,
  callbacks: {
      nodeClick: function(name, extra) {
          console.log(name);
      }
  }
});

console.log(treeData, dTree, tree)
d3.select(document.getElementById('tree_container')).append(tree)