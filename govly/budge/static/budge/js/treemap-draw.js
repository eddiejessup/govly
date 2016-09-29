/*global $, jQuery, d3*/

var timeTreemapDraw = (function () {

  var tooltipOffset = {x: -150, y: 10};
  var color = d3.scale.category20c();
  var $div;
  var width, height;
  var div;
  var treemap;
  var number;
  var unit;

  var initialize = function() {
    $div = $("#treemap-container");
    width = $div.width();
    height = $div.height();
    div = d3.select("#treemap-container");
    treemap = d3.layout.treemap()
      .size([width, height])
      .sticky(false)
      .value(function(d) { return d.data.fraction; });
  };

  var _mousemove = function(d) {
    var xPosition = d3.event.pageX + tooltipOffset.x;
    var yPosition = d3.event.pageY + tooltipOffset.y;
    // Cache this DOM at some point
    d3.select("#tooltip")
      .style("left", xPosition + "px")
      .style("top", yPosition + "px");
    d3.select("#tooltip #name")
      .text(d.data.name);
    d3.select("#tooltip #quantification")
      .text((d.data.fraction * number) + ' ' + unit);
    d3.select("#tooltip #description")
      .text(d.data.description);
    d3.select("#tooltip").classed("hidden", false);
  };

  var _mouseout = function() {
    d3.select("#tooltip").classed("hidden", true);
  };

  var _position = function() {
    this
      .style("left", function(d) { return d.x + "px"; })
      .style("top", function(d) { return d.y + "px"; })
      .style("width", function(d) { return Math.max(0, d.dx - 1) + "px"; })
      .style("height", function(d) { return Math.max(0, d.dy - 1) + "px"; });
  };

  var renderInitial = function(data) {
    number = data.number;
    unit = data.unit;

    var nodes = treemap.nodes;
    var node = div.datum(data.treemap_data).selectAll(".node")
      .data(nodes)
      .enter()
      .append("div")
      .attr("class", "node")
      .call(_position)
      .style("background", function(d) {
        return d.children ? color(d.data.name) : null;
      })
      .on("mousemove", _mousemove)
      .on("mouseout", _mouseout)
      .text(function(d) { return d.children ? null : d.data.name; });
    this.node = node;
  };

  var renderExisting = function(data) {
    number = data.number;
    unit = data.unit;

    var nodes = treemap.nodes(data.treemap_data);
    this.node
      .data(nodes)
      .transition()
      .duration(500)
      .call(_position);
  };

  return {
    initialize: initialize,
    renderInitial: renderInitial,
    renderExisting: renderExisting,
  };
}());
