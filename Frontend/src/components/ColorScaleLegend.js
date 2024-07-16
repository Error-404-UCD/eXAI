import React, { useRef, useEffect } from "react";
import * as d3 from "d3";

const ColorScaleLegend = ({ min, max, colorInterpolator, width, height, textHeight }) => {
  const legendRef = useRef(null);

  useEffect(() => {
    if (min == null || max == null || !colorInterpolator) return;

    // Create the color scale
    const colorScale = d3.scaleSequential(colorInterpolator).domain([min, max]);

    d3.select(legendRef.current).selectAll("*").remove();

    const svg = d3
      .select(legendRef.current)
      .attr("width", width)
      .attr("height", height + textHeight);

    const gradient = svg
      .append("defs")
      .append("linearGradient")
      .attr("id", "gradient")
      .attr("x1", "0%")
      .attr("x2", "100%");

    gradient
      .append("stop")
      .attr("offset", "0%")
      .attr("stop-color", "rgb(75,0,130)");

    gradient
    .append("stop")
    .attr("offset", "50%")
    .attr("stop-color", colorScale(0));

    gradient
      .append("stop")
      .attr("offset", "100%")
      .attr("stop-color", "rgb(0,100,0)");

    svg
      .append("rect")
      .attr("width", width)
      .attr("height", height)
      .style("fill", "url(#gradient)");

    svg
      .append("text")
      .attr("x", 0)
      .attr("y", height + 15)
      .text(min);

    svg
    .append("text")
    .attr("x", width / 2 - 15)
    .attr("y", height + 15)
    .text("0.0");

    svg
      .append("text")
      .attr("x", width)
      .attr("y", height + 15)
      .attr("text-anchor", "end")
      .text(max);

    svg
      .append("text")
      .attr("x", width / 2 - 45)
      .attr("y", height + 35)
      .text("SHAP values");
  }, [min, max, colorInterpolator]);

  return <svg ref={legendRef}></svg>;
};

export default ColorScaleLegend;
