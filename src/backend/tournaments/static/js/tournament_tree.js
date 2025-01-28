function renderTournamentTree(nodes, links) {
    console.log("Rendering nodes:", nodes);
    console.log("Rendering links:",links);

    if (window.diagram) {
        window.diagram.model = new go.TreeModel([]);
    }
    const filteredNodes = nodes.filter(node => {
        const keepNode = node.round !== 1 || node.player_one || node.player_two;
        if (!keepNode) {
            console.log("Removing node:", node); // Debug log for removed nodes
        }
        return keepNode;
    });


    const $ = go.GraphObject.make;

    const diagram = $(go.Diagram, "myDiagramDiv", {
        layout: $(go.TreeLayout, {
            angle: 180,}),
        "undoManager.isEnabled": true
    });

    diagram.nodeTemplateMap.add("match", $(go.Node, "Auto", { selectable: false },
        $(go.Shape, "Rectangle", { fill:"lightyellow", stroke: null}),
            new go.Binding("fill", "color"),
        $(go.Panel, "Table")
            .addColumnDefinition(0, { separatorStroke: "black"})
            .addColumnDefinition(1, { separatorStroke: "black", background: "#BABABA"})
            .addRowDefinition(0, { separatorStroke: "black"})
            .addRowDefinition(1, { separatorStroke: "black"})
            .add($(go.TextBlock, {
                    margin: 5,
                    font: "10pt Segoe UI, sans-serif",
                    row: 0,
                    wrap: go.Wrap.None,
                    width: 90,
                    isMultiline: false,
                    textAlign: "left",
                    stroke: "black",
                }, new go.Binding("text", "player_one")),
                $(go.TextBlock, {
                    row: 1,
                    wrap: go.Wrap.None,
                    margin: 5,
                    width: 90,
                    isMultiline: false,
                    textAlign: "left",
                    font: "10pt Segoe UI, sans-serif",
                    stroke: "black",
                }, new go.Binding("text", "player_two")),
                $(go.TextBlock, {
                    row: 0,
                    column: 1,
                    wrap: go.Wrap.None,
                    margin: 2,
                    width: 25,
                    isMultiline: false,
                    textAlign: "center",
                    font: "10pt Segoe UI, sans-serif",
                    stroke: "black",
                }, new go.Binding("text", "score_one")),
                $(go.TextBlock, {
                    row: 1,
                    column: 1,
                    wrap: go.Wrap.None,
                    margin: 2,
                    width: 25,
                    isMultiline: false,
                    textAlign: "center",
                    font: "10pt Segoe UI, sans-serif",
                    stroke: "black",
                }, new go.Binding("text", "score_two"))
            )
    ));

    diagram.linkTemplate = $(go.Link, { routing : go.Routing.Orthogonal , selectable: false },
        $(go.Shape, { stroke: "red", strokeWidth: 2 })
    );

    diagram.model = new go.TreeModel(filteredNodes);

    diagram.model.nodeCategoryProperty = "category";

    window.diagram = diagram;
}