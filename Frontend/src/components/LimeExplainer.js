import React, { useEffect, useRef, useState } from "react";
import * as d3 from "d3";

const LimeExplainer = ({ imageUrl, maskData, containerSize }) => {
  const containerRef = useRef(null);

  const [showBlue, setShowBlue] = useState(true);
  const [showRed, setShowRed] = useState(true);
  const [showYellow, setShowYellow] = useState(true);
  const positiveColor = "rgba(237, 71, 74, 0.8)";
  const negativeColor = "rgba(104, 116, 232, 0.8)";
  const boundaryColor = "rgba(255, 255, 0, 1)";

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
      svg
        .append("image")
        .attr("xlink:href", imageUrl)
        .attr("width", scaledImgWidth)
        .attr("height", scaledImgHeight)
        .attr("x", offsetX)
        .attr("y", offsetY)
        .style("image-rendering", "pixelated");
        // .style("opacity", "0.8");

      // Scale the mask data to match the scaled image dimensions
      const maskScaleX = scaledImgWidth / maskData[0].length;
      const maskScaleY = scaledImgHeight / maskData.length;

      // Add the mask to the SVG
      for (var j = 0; j < maskData[0].length; ++j) {
        for (var i = 0; i < maskData.length; ++i) {
          let value = maskData[j][i];
          let colour = null;

          if (value === 1 && showRed) {
            colour = positiveColor;
          } else if (value === -1 && showBlue) {
            colour = negativeColor;
          }

          // Check for boundary conditions
          let isBoundary = false;
          if (i > 0 && maskData[j][i - 1] !== value) isBoundary = true; // Left neighbor
          if (i < maskData.length - 1 && maskData[j][i + 1] !== value)
            isBoundary = true; // Right neighbor
          if (j > 0 && maskData[j - 1][i] !== value) isBoundary = true; // Top neighbor
          if (j < maskData[0].length - 1 && maskData[j + 1][i] !== value)
            isBoundary = true; // Bottom neighbor

          if (isBoundary && showYellow) {
            colour = boundaryColor; // Yellow color for boundary
          }

          if (colour) {
            svg
              .append("rect")
              .attr("x", offsetX + i * maskScaleX)
              .attr("y", offsetY + j * maskScaleY)
              .attr("width", maskScaleX)
              .attr("height", maskScaleY)
              .attr("fill", colour);
          }
        }
      }
    };

    loadImageAndMask();
  }, [imageUrl, maskData, showBlue, showRed, showYellow]);

  return (
    <div className="flex flex-col items-center">
      <svg ref={containerRef}></svg>
      <div className="flex flex-row justify-center mt-4 space-x-4">
        <div className="flex items-center">
          <input
            type="checkbox"
            checked={showRed}
            onChange={() => setShowRed(!showRed)}
            className="mr-2"
          />
          <div
            className="w-4 h-4 mr-2"
            style={{ backgroundColor: positiveColor }}
          ></div>
          <span>Positive Region</span>
        </div>
        <div className="flex items-center">
          <input
            type="checkbox"
            checked={showBlue}
            onChange={() => setShowBlue(!showBlue)}
            className="mr-2"
          />
          <div
            className="w-4 h-4 mr-2"
            style={{ backgroundColor: negativeColor }}
          ></div>
          <span>Negative Region</span>
        </div>
        <div className="flex items-center">
          <input
            type="checkbox"
            checked={showYellow}
            onChange={() => setShowYellow(!showYellow)}
            className="mr-2"
          />
          <div
            className="w-4 h-4 mr-2"
            style={{ backgroundColor: boundaryColor }}
          ></div>
          <span>Boundary</span>
        </div>
      </div>
    </div>
  );
};

export default LimeExplainer;
