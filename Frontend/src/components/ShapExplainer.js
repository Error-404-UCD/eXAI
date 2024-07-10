import React, { useEffect, useRef } from "react";
import * as d3 from "d3";


const ShapExplainer = ({ imageUrl, shapValues, containerSize }) => {
  const containerRef = useRef(null);

//   console.log(shapValues);

  useEffect(() => {
    if (shapValues == null) return;

    const loadImageAndCreateOverlays = async () => {
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

      
        scaledImgWidth = containerSize;
        scaledImgHeight = containerSize / imageAspectRatio;
     

      const shapWidth = shapValues.length;
      const shapHeight = shapValues[0].length;
      const classes = shapValues[0][0][0].length;

      console.log("scaledImgWidth: " + scaledImgWidth);
      console.log("scaledImgHeight: " + scaledImgHeight);
      console.log("classes: " + classes);

      // Clear any previous content
      d3.select(containerRef.current).selectAll("*").remove();

      const createOverlay = (classIndex, shapValues) => {
        // Create a canvas to draw the image
        const canvas = document.createElement("canvas");
        const ctx = canvas.getContext("2d");
        canvas.width = scaledImgWidth;
        canvas.height = scaledImgHeight;

        // Draw the image as grayscale
        ctx.filter = "grayscale(100%)";
        ctx.globalAlpha = 0.5;
        ctx.imageSmoothingEnabled = false;

        ctx.drawImage(image, 0, 0, scaledImgWidth, scaledImgHeight);

        // Get the image data
        const imageData = ctx.getImageData(0, 0, scaledImgWidth, scaledImgHeight);
        const data = imageData.data;

        // Convert to grayscale and invert the colors
        for (let i = 0; i < data.length; i += 4) {
          const avg = (data[i] + data[i + 1] + data[i + 2]) / 3; // Grayscale
          data[i] = 255 - avg; // Invert Red
          data[i + 1] = 255 - avg; // Invert Green
          data[i + 2] = 255 - avg; // Invert Blue
        }

        // Put the manipulated data back onto the canvas
        ctx.putImageData(imageData, 0, 0);

        // Remove grayscale filter for SHAP overlay
        ctx.filter = "none";
        ctx.globalAlpha = 1.0;

        // Scale SHAP values to image size

        const scaleX = scaledImgWidth / shapWidth;
        const scaleY = scaledImgHeight / shapHeight;

        // Create a color scale
        const colorScale = d3
          .scaleSequential(d3.interpolateRdBu)
          .domain([d3.min(shapValues.flat(4)), d3.max(shapValues.flat(3))]);
        // console.log(shapValues);
        // Draw the SHAP values overlay
        for (let y = 0; y < shapHeight; y++) {
          for (let x = 0; x < shapWidth; x++) {
            let total = 0;
            for (let px = 0; px < 3; px++) {
              total += shapValues[y][x][px][classIndex];
            }

            // console.log(total);
            if (total < 0) {
              ctx.fillStyle = "white";
            } else {
              ctx.fillStyle = "blue";
            }

            // ctx.fillStyle = colorScale(total);
            ctx.fillRect(x * scaleX, y * scaleY, 2, 2);
            
          
        
          }
        }

        return canvas.toDataURL();
      };

      // Clear any previous content
      d3.select(containerRef.current).selectAll("*").remove();

      // Create a scrollable container
      const container = d3.select(containerRef.current);

      // Create and append the three overlay images
      for (let i = 0; i < classes; i++) {
        const overlayDataUrl = createOverlay(i, shapValues);
        container
          .append("img")
          .attr("src", overlayDataUrl)
          .style("display", "inline-block")
          .style("width", scaledImgWidth + "px")
          .style("height", scaledImgHeight + "px")
          .style("margin-bottom", "15px");
      }
    };

    loadImageAndCreateOverlays();
  }, [imageUrl, shapValues, containerSize]);

  return <div className="w-[500px] h-[500px] overflow-y-scroll" ref={containerRef}></div>;
};

export default ShapExplainer;