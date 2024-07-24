import React, { useEffect, useRef } from "react";
import * as d3 from "d3";

const LimeExplainer = ({ imageUrl, maskData, containerSize }) => {
  const containerRef = useRef(null);

  useEffect(() => {
    const loadImageAndMask = async () => {
      // Load the image
      const image = new Image();
      image.src = imageUrl;
      await new Promise((resolve) => {
        image.onload = resolve;
      });

      // Get image dimensions
      const { width: originalImgWidth, height: originalImgHeight } = image;

      // Calculate the scaling factors to maintain aspect ratio
      const imageAspectRatio = originalImgWidth / originalImgHeight;
      let scaledImgWidth, scaledImgHeight;

      if (imageAspectRatio > 1) {
        scaledImgWidth = containerSize;
        scaledImgHeight = containerSize / imageAspectRatio;
      } else {
        scaledImgWidth = containerSize * imageAspectRatio;
        scaledImgHeight = containerSize;
      }

      // Calculate the offsets to center the image in the container
      const offsetX = (containerSize - scaledImgWidth) / 2;
      const offsetY = (containerSize - scaledImgHeight) / 2;

      // Clear any previous content
      d3.select(containerRef.current).selectAll("*").remove();

      // Create an SVG container
      const svg = d3
        .select(containerRef.current)
        .attr("width", containerSize)
        .attr("height", containerSize)
        .style("shape-rendering", "crispEdges")
        .style("image-rendering", "pixelated");

      // Add the image to the SVG
      // svg
      //   .append("image")
      //   .attr("xlink:href", imageUrl)
      //   .attr("width", scaledImgWidth)
      //   .attr("height", scaledImgHeight)
      //   .attr("x", offsetX)
      //   .attr("y", offsetY)
      //   .style("image-rendering", "pixelated"); // Ensure the image rendering is also set

      // Scale the mask data to match the scaled image dimensions
      const maskScaleX = scaledImgWidth / maskData[0].length;
      const maskScaleY = scaledImgHeight / maskData.length;

      // console.log("offsetX: " + offsetX);
      // console.log("offsetY: " + offsetY);
      // console.log("maskScaleX: " + maskScaleX);
      // console.log("maskScaleY: " + maskScaleY);

      // Add the mask to the SVG

      for (var j = 0; j < maskData[0].length; ++j) {
        for (var i = 0; i < maskData.length; ++i) {
          let value = maskData[j][i];
          if (value === 1) {
            svg
              .append("rect")
              .attr("x", offsetX + i * maskScaleX)
              .attr("y", offsetY + j * maskScaleY)
              .attr("width", maskScaleX)
              .attr("height", maskScaleY)
              .attr("fill", "rgba(255, 0, 0, 0.5)");
          }
        }
      }
    };

    loadImageAndMask();
  }, [imageUrl, maskData]);

  return <svg ref={containerRef}></svg>;
};

export default LimeExplainer;