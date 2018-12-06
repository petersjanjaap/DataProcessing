//width and height for svg and bar chart
var w = 800;
var h = 500;
var padding = 60;
var xWidth = w - 2 * padding;
var yHeight = h - 1.5 * padding;

/*
contains all functions for html page
*/

// returns x and y observations for a given json object
function fillXY(jsonObj){
  var xAxis = [];
  var yAxis = [];
  for (var key in jsonObj) {
    if (jsonObj.hasOwnProperty(key)) {

      // add x and y observations for each key to lists
      xAxis.push(jsonObj[key].time);
      yAxis.push(Math.round(parseFloat(jsonObj[key].datapoint)));
    }
  }
  return [xAxis, yAxis];
};

// returns minimum and maximum values for given variable
function minMax(variable) {

  // domain is an array of the data bounds [minimum, maximum]
  domain = [Math.min.apply(null, variable), Math.max.apply(null, variable)];
  return domain;
};

// generates linear scale for variable's minimum and maximum
function linearScaling(varBounds, axisType) {

  // obtains scales for axes
  var rangeBound;
  var domainBounds;

  // x and y axis have different ranges
  if (axisType == 'y') {
    rangeBound = [yHeight, padding];
    domainBounds = [varBounds[0], varBounds[1]];
  } else {
    rangeBound = [padding, xWidth];
    domainBounds = [varBounds[0], varBounds[1]];
  }

  linearScaler = d3.scaleLinear()
         .domain(domainBounds)
         .range(rangeBound);
  return linearScaler;
};

// obtains country names from json object otherwise uses varname
function colorDomain (aDataset){
  var countryNames = [];
  for (var key in aDataset) {
    if (aDataset[key].hasOwnProperty('Country')) {
      var present = false;
      for (var i = 0; i < countryNames.length; i++) {
          if (countryNames[i] == aDataset[key].Country) {
              present = true;
          }
      }
      if (present == false) {
        countryNames.push(aDataset[key].Country);
      }
    } else {
      countryNames = ["Women In Science"];
      break;
    }
  }
  return countryNames;
};

// obtains the scaled value of an observation for color usage
function colorScaler(colorDomain, datapoint) {
  if (datapoint.hasOwnProperty('Country')) {
    for (var i = 0; i < colorDomain.length; i++) {
      if (datapoint.Country == colorDomain[i]) {

        return i;
      }
    }
  } else {
    return 0;
  }
};

// generate a legend
function legend(aDataset, svg, cDomain, colorScale) {

  // source: https://stackoverflow.com/questions/42009622/how-to-create-a-horizontal-legend
  var legendGroup = svg.append("g")
                       .attr("transform", "translate("+(w-padding * 1.8)+",30)");

  var legend = legendGroup.selectAll(".legend")
        .data(cDomain)
        .enter()
        .append("g")
        .attr("transform", (d,i)=>"translate(0," + (yHeight / cDomain.length) * i + ")");

  var legendRects = legend.append("rect")
                          .attr("width", 20)
                          .attr("height", 20)
                          .attr("fill", (d,i)=> colorScale(i));

  var legendText = legend.append("text")
                         .attr("x", 20)
                         .attr("y", 18)
                         .style("font-size", "11px")
                         .text(d=>d);
}

// generates a scatterplot based on input data
function scatterPlot(aDataset, svg, titleToUse) {

  // creates a title
  svg.append("text")
        .attr("x", (w / 2))
        .attr("y", padding * 0.8)
        .attr("text-anchor", "middle")
        .style("font-size", "16px")
        .text(titleToUse);

  // obtains axes and relative scale
  axes = fillXY(aDataset);
  var x = axes[0];
  var y = axes[1];

  xScale = linearScaling(minMax(x), 'x');
  yScale = linearScaling(minMax(y), 'y');

  // draw y axis
  svg.append("g")
     .attr("class", "y axis")
     .attr("transform", "translate(" + padding + ", 0)")
     .call(d3.axisLeft(yScale));

  // draw x axis
  svg.append("g")
    .attr("class", "x axis")
    .attr("transform", "translate(0," + yHeight + ")")
    .call(d3.axisBottom(xScale));

   // add label to x axis
   svg.append("text")
      .attr("class", "label")
      .attr("x", xWidth / 2 )
      .attr("y", h - (h - yHeight) / 7 )
      .text("Year");

   // add label to y axis
   svg.append("text")
      .attr("class", "label")
      .attr("transform", "rotate(-90)")

      /*
      x and y coordinates are rotated, so x and y coordinates are vice
      versa entered
      */
      .attr("y", 10)
      .attr("x", 0 - yHeight / 2)
      .attr("dy", ".35em")
      .style("text-anchor", "middle")
      .text("Observation values in percentage %");

   // obtains domain of values to assign colors to
   cDomain = colorDomain(aDataset);

   // color brewer color scheme: https://stackoverflow.com/questions/40328984/how-to-use-a-colorbrewer-scale
   var colorScale = d3.scaleQuantize()
                      .range(colorbrewer.YlGn[9])
                      .domain([0, cDomain.length]);

   // draw scatterplot (based on Scott Murray d3)
   svg.selectAll("circle")
      .data(aDataset)
      .enter()
      .append("circle")
      .attr("cx", function(d) {
         return xScale(d.time);
      })
      .attr("cy", function(d) {
         return yScale(d.datapoint);
       })
      .attr("r", 5)
      .attr("fill", function(d) {
        return colorScale(colorScaler(cDomain, d));
      });

  // add legend to scatterPlot
  legend(aDataset, svg, cDomain, colorScale);
};

// updates scatter after user uses dropdown menu
function updateScatter(aDataset, svg, titleToUse) {

    // remove title
    svg.selectAll('text').remove()

    // remove old circles
    svg.selectAll("circle")
      .remove();

    // remove axes
    svg.selectAll("g")
       .remove();

    // create new scatterplot
    scatterPlot(aDataset, svg, titleToUse);
}

/*
start of main function
*/

// use functions on opening screen
window.onload = function() {

  //create SVG element
  var svg = d3.select("body")
              .append("svg")
              .attr("width", w)
              .attr("height", h);

  // obtain datasets
  var womenInScience = d3.json("msti.json");
  var consConf = d3.json("consconf.json");
  var datasets = [womenInScience, consConf];

  // retrieve datasets from files
  Promise.all(datasets).then(response => {

    // replace datasets as response json objects
    womenInScience = response[0];
    consConf = response[1];

    // titles
    var titles = ["Women in Science", "Consumer Confidence"];

    // start with scatterplot for womenInScience
    scatterPlot(womenInScience, svg, titles[0]);

    // prepare drop down menu. Source: http://bl.ocks.org/jfreels/6734823
    var select = d3.select('p')
                   .append('select')
                	 .attr('class','select')
                   .on('change', onchange);

    // add options based on title names
    var options = select
      .selectAll('option')
    	.data(titles)
      .enter()
    	.append('option')
    	.text(function (d) { return d; });

    // functions selects dataset to use based on drop down menu
    function onchange() {
    	var selectValue = d3.select('select').property('value');
      var dataToUse;
      var titleToUse;
    	if (selectValue == "Consumer Confidence") {
        dataToUse = consConf;
        titleToUse = titles[1];
      } else {
        dataToUse = womenInScience;
        titleToUse = titles[0];
      }
      updateScatter(dataToUse, svg, titleToUse);
    };

  }).catch(function(e){
      throw(e);
  });
};
