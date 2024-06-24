import * as d3 from "d3";
import { useEffect, useRef } from "react";

const HeatMap = (data) => {
  	const ref = useRef();
    	const outputWidth = 1400;
  	const outputHeight = 140;
	var max = 0.1;
  	var min = -0.1;
  function remapData(data) {

    // console.log(data.heatData.array[0][0][0][0][0]);

   
    var mapped_data = []


    var ndata = data.heatData.array[0][0];
    // Loop through all row pixels i
    for (var i = 0; i < ndata.length; ++i) {
      // Loop through all col pixels j
      for (var j = 0; j < ndata[i].length; ++j) {
        // For each number value 0...9 k
        for (var k = 0; k < ndata[i][j].length; ++k) {
          // Set new row = i
          // Set new col = k * count_of_cols + j
          // Set new val = data[i][j][k]
          const newVal = ndata[i][j][k];
          mapped_data.push({
            col: i,
            row: k * ndata[i].length + j,
            value: newVal,
          });

          if (newVal < min) {
            // min = newVal;
          }
          if (newVal > max) {
            // max = newVal
          }
        }
      }
    }
        
    return mapped_data;
            
                
  }

  useEffect(() => {

    	// set the dimensions and margins of the graph
    	const margin = { top: 0, right: 0, bottom: 0, left: 0 },
      	width = outputWidth - margin.left - margin.right,
      	height = outputHeight - margin.top - margin.bottom;

    	// append the svg object to the body of the page
    const svg = d3
      .select(ref.current)
      .append("svg")
      .attr("width", width + margin.left + margin.right)
      .attr("height", height + margin.top + margin.bottom)
      .append("g")
      .attr("transform", `translate(${margin.left},${margin.top})`);

    // var data = {}

    // Labels of row and columns
    var myGroups = [...Array(280).keys()].map((i) => i + 1);
    var myVars = [...Array(28).keys()].map((i) => i + 1);

    // Build X scales and axis:
    var x = d3.scaleBand().range([0, width]).domain(myGroups).padding(0.01);
    svg
      .append("g")
      .attr("transform", "translate(0," + height + ")")

      //console.log(data);
    var mapped_data = remapData(data);
    console.log(mapped_data);

    // Build X scales and axis:
    var y = d3.scaleBand().range([height, 0]).domain(myVars).padding(0.01);
    svg
      .append("g")
      .call(d3.axisLeft(y).tickValues([]))
      .call(d3.axisTop(x).tickValues([]))
      .call(d3.axisBottom(x).tickValues([]));
      //.call(d3.axisTop(x).tickValues([]))
      //.call(d3.axisTop(y).tickValues([]));

    // Build color scale
    var myColor = d3
      .scaleLinear()
      .range(["#005acd", "rgba(255, 255, 255, 0)", "#f8f8f8"])
      .domain([min, 0.0, max]);

    //Read the data
    // Reference: https://kamibrumi.medium.com/getting-started-with-react-d3-js-d86ccea05f08
    // Heatmap Reference: https://d3-graph-gallery.com/graph/heatmap_basic.html
    // var data = {};


    svg
      .selectAll()
      .data(mapped_data, function (d) {
        return d.row + ":" + d.col;
      })
      .enter()
      .append("rect")
      .attr("x", function (d) {
        return x(d.row);
      })
      .attr("y", function (d) {
        return y(d.col);
      })
      .attr("width", 10)
      .attr("height", 10)
      .style("fill", function (d) {
        return myColor(d.value);
      });

   // eslint-disable-next-line react-hooks/exhaustive-deps 
  }, []);

  return <svg width={outputWidth} height={outputHeight} id="heatmap" ref={ref} />;
};

export default HeatMap;
