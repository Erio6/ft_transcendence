function renderTournamentTree(nodes, links) {
    const $ = go.GraphObject.make;

    const diagram = $(go.Diagram, "myDiagramDiv", {
        layout: $(go.LayeredDigraphLayout, {
            direction: 90, layerSpacing: 50})
    });

    diagram.nodeTemplateMap.add("player", $(go.Node, "Auto",
        $(go.Shape, "Rectangle", {fill:"lightblue", stroke: null},
            new go.Binding("fill", "color")),
        $(go.TextBlock, {margin: 5, font: "bold 12px sans-serif"},
            new go.Binding("text", "text"))
    ));

    diagram.nodeTemplateMap.add("", $(go.Node, "Auto",
        $(go.Shape, "Rectangle", { fill:"lightyellow", stroke: null}),
        $(go.TextBlock, { margin: 5, font: "bold 12px sans-serif"},
            new go.Binding("text", "text"))
    ));

    diagram.model = new go.GraphLinksModel(nodes, links);

    diagram.model.nodeCategoryProperty = "isPlayer";
}