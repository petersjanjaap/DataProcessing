//width and height for svg containing graph
var w = 800;
var h = 500;
var padding = 60;
var xWidth = w - 2 * padding;
var yHeight = h - 1.5 * padding;

// source: https://beta.observablehq.com/@mbostock/d3-pie-chart
// width and height for svg containing pie
var width = 520;
var height = 400;
var r = 160;

/*
contains all functions for html page
*/
// merges arrays to array of objects
function parseData(var1, var2) {
   var arr = [];

   for (var i = 0; i < var1.length; i++) {
      arr.push(
         {
            date: var1[i],
            value: var2[i]
         });
   }
   return arr;
};

// uses object to return dictionary of price, date and returns variables
function getVars(stockInfo) {
  var dates = [];
  var price = [];
  var returns = [];

  for (var key in stockInfo) {
    if (stockInfo.hasOwnProperty(key)) {
      dates.push(new Date(stockInfo[key].Date));
      price.push(stockInfo[key].Close);
    }
  };

  for (var i = 1; i < price.length; i++) {
    returns.push(((price[i] - price[i - 1]) / price[i - 1]) * 100);
  }

  // drop first date and price element since no return then is available
  dates.splice(0, 1);
  price.splice(0, 1);

  var vars = {
                "date": dates,
                "price": price,
                "returns": returns
              };
  return vars;
};

// returns the return domain
function rDomain(returns) {
  var maxReturn = Math.max(...returns);
  var minReturn = Math.min.apply(null, returns);
  var returnDomain = [minReturn, maxReturn];
  return returnDomain;
};

// returns the date domain
function dDomain(date) {
  var maxDate = new Date(Math.max.apply(null, date));
  var minDate = new Date(Math.min.apply(null, date));
  var dateDomain = [minDate, maxDate];
  return dateDomain;
};

// use functions on opening screen
window.onload = function() {

  // obtain datasets
  var goog = d3.json("GOOG.json");
  var msft = d3.json("MSFT.json");
  var aapl = d3.json("AAPL.json");

  // retrieve datasets from files
  Promise.all([goog, msft, aapl]).then(response => {

    // store datasets
    var sets = {
                  "GOOG": response[0],
                  "MSFT": response[1],
                  "AAPL": response[2]
                };

    // contains latest market capitalisation in billions for all companies
    // source investing.com
    var marketcap = [{"label":"GOOG", "value":727.44},
                    {"label":"MSFT", "value":814.05},
                    {"label":"AAPL", "value":785.27}];

    // create SVG element for pie
    var svg = d3.select("body")
                .append("svg")
                .attr("class", "pie")
                .data([marketcap])
                .attr("width", width)
                .attr("height", height);


    // create SVG element for graph
    var svgChart = d3.select("body")
                     .append("svg")
                     .attr("class", "chart")
                     .attr("width", w)
                     .attr("height", h);

    /*
    This is the start of the pie chart
    */

    // source pie chart: http://bl.ocks.org/enjalot/1203641
    // create group for pie chart center coordinates based on radius
    var g = svg.append("g")
               .attr("transform", "translate(" + r + "," + r * 1.4 + ")");

    var arc = d3.arc()
        .innerRadius(0)
        .outerRadius(r);

    var pie = d3.pie()
        .value(function(d) { return d.value; });

    var arcs =  pie(marketcap);

    // color scales for companies
    var color = {
                  "GOOG": 0,
                  "MSFT": 1,
                  "AAPL": 2
                };

    // set colorscaler function
    var colorScale = d3.scaleQuantize()
                       .range(colorbrewer.Set1[3])
                       .domain([0, marketcap.length]);

    // source interactivity https://blog.risingstack.com/d3-js-tutorial-bar-charts-with-javascript/
    g.selectAll("path")
      .data(arcs)
      .enter().append("path")
      .attr("fill", (d, i) => colorScale(i))
      .attr("stroke", "white")
      .attr("d", arc)

      // use opacity to show over which arc user's mouse is hovering
      .on('mouseenter', function (actual, i) {
        d3.select(this).attr('opacity', 0.5)
      })
      .on('mouseleave', function (actual, i) {
          d3.select(this).attr('opacity', 1)
      })

      // click function updates graph to selected company in pie chart
      .on("click", function(d){

        // source: http://bl.ocks.org/d3noob/7030f35b72de721622b8
        // get new stockinfo and returns
        var title = d.data.label
        var stockInfo = sets[d.data.label];
        var vars = getVars(stockInfo);
        var data = parseData(vars.date, vars.returns);

        // adjust line
        svgChart.select(".line")
                .attr("stroke", () => colorScale(color[d.data.label]))
                .transition()  // change the line
                .duration(750)
                .attr("d", line(data));

        // adjust scale
        var y = d3.scaleLinear()
                  .domain(rDomain(vars.returns))
                  .rangeRound([yHeight, padding * 0.75]);

        // adjust axis
        svgChart.select(".y_axis")
                .transition()
                .duration(750)
                .call(d3.axisLeft(y));

        // add title, source: https://stackoverflow.com/questions/21843667/d3-change-text-label-when-data-updates
        svgChart.select(".title")
                .data(title)
                .style("opacity", 0)
                .transition().duration(500)
                .style("opacity", 1)
                .text( () => `${title} stock returns november-december`)
        });

  // source pie chart: http://bl.ocks.org/enjalot/1203641
  // add text to pies
  var pieText = g.selectAll("text")
                  .data(arcs)
                  .enter().append("text")
                    .attr("transform", d => `translate(${arc.centroid(d)})`)
                    .attr("dy", "0.35em");

  // text to fill arc with
  pieText.append("tspan")
          .attr("x", -40)
          .attr("y", 0)
          .attr("fill-opacity", 0.7)
          .text(d => `$${d.data.value} bln`);

  // source legends: https://www.youtube.com/watch?v=L5GXOdt2uOc
  var legends = svg.append("g")
                   .attr("transform", "translate(230, 20)")
                   .selectAll(".legends")
                   .data(marketcap);

  // add legend
  var legend = legends.enter()
                      .append("g")
                      .classed("legends", true)
                      .attr("transform", function(d,i)
                      {return "translate("+ r * 0.9 +"," + (i + 1) / 3 * r+ ")";});

  // add blocks to legend
  legend.append("rect")
        .attr("width", 34)
        .attr("height",34)
        .attr("fill", (d, i) => colorScale(i));

  // add text to legend
  legend.append("text")
        .style("font-size", "34px")
        .text(d => d.label)
        .attr("fill", (d, i) => colorScale(i))
        .attr("x", 40)
        .attr("y", 30);

  // creates a title
  svg.append("text")
          .attr("class", "title")
          .attr("x", (width / 2))
          .attr("y", padding * 0.4)
          .attr("text-anchor", "middle")
          .attr("fill", "lightblue")
          .style("font-size", "34px")
          .text("Market Capitalisation in $ Billions");

  /*
  This is the start of the graph
  */

  // source linechart: https://medium.freecodecamp.org/learn-to-create-a-line-chart-using-d3-js-4f43f1ee716b
  //  get data, use google as default
  var stockInfo = sets.GOOG;
  var vars = getVars(stockInfo);
  var data = parseData(vars.date, vars.returns);

  // set scales
  var x = d3.scaleTime()
            .domain(dDomain(vars.date))
            .rangeRound([padding, xWidth]);

  var y = d3.scaleLinear()
            .domain(rDomain(vars.returns))
            .rangeRound([yHeight, padding * 0.75]);

  // draw x axis
  svgChart.append("g")
          .attr("transform", "translate(0," + yHeight + ")")
          .call(d3.axisBottom(x))
          .select(".domain");

   // draw y axis
   svgChart.append("g")
           .attr("class", "y_axis")
           .attr("transform", "translate(" + padding * 0.97 + ", 0)")
           .call(d3.axisLeft(y))
           .append("text")
           .attr("transform", "rotate(-90)")
           .attr("x", - padding)
           .attr("y", 6)
           .attr("dy", "0.71em")
           .attr("fill", "black")
           .attr("text-anchor", "end")
           .text("Returns (%)");

   // creates a title
   svgChart.append("text")
           .attr("class", "title")
           .attr("x", (w / 2))
           .attr("y", padding * 0.4)
           .attr("text-anchor", "middle")
           .attr("fill", "lightblue")
           .style("font-size", "34px")
           .text("GOOG stock returns november-december");

    // set line variable
    var line = d3.line()
                 .x(function(d) { return x(d.date)})
                 .y(function(d) { return y(d.value)});
                 x.domain(d3.extent(data, function(d) { return d.date }));
                 y.domain(d3.extent(data, function(d) { return d.value }));

    // draw path for graph
     svgChart.append("path")
             .attr("class", "line")
             .datum(data)
             .attr("fill", "none")
             .attr("stroke", () => colorScale(color.GOOG))
             .attr("stroke-linejoin", "round")
             .attr("stroke-linecap", "round")
             .attr("stroke-width", 3)
             .attr("d", line);

  }).catch(function(e){
      throw(e);
  });
};
