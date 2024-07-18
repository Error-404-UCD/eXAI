import React, { useEffect, useRef, useState } from "react";
import * as d3 from "d3";

import ColorScaleLegend from "./ColorScaleLegend";


const ShapExplainer = ({ imageUrl, shapValues, containerSize, classNames }) => {
  const containerRef = useRef(null);
  const [activeClass, setActiveClass] = useState(classNames[0]); // Initial class name
//   const [colorScaleMin, setColorScaleMin] = useState(null);
//   const [colorScaleMax, setColorScaleMax] = useState(null);
  const [tooltipContent, setTooltipContent] = useState(0);
  const [showToolTip, setShowToolTip] = useState(false);
  const [mousePosition, setMousePosition] = useState({ x: 0, y: 0 });

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

    //   console.log("scaledImgWidth: " + scaledImgWidth);
    //   console.log("scaledImgHeight: " + scaledImgHeight);
    //   console.log("classes: " + classes);

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
        const imageData = ctx.getImageData(
          0,
          0,
          scaledImgWidth,
          scaledImgHeight
        );
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

        const flattenedShapValues = shapValues.flat(4);
        const minShapValue = d3.min(flattenedShapValues);
        const maxShapValue = d3.max(flattenedShapValues);

        // setColorScaleMin(minShapValue);
        // setColorScaleMax(maxShapValue);

        // Create a color scale
        const colorScale = d3
          .scaleSequential(d3.interpolatePRGn)
          .domain([minShapValue, maxShapValue]);
        // console.log(shapValues);
        // Draw the SHAP values overlay
        for (let y = 0; y < shapHeight; y++) {
          for (let x = 0; x < shapWidth; x++) {
            let total = 0;
            for (let px = 0; px < 3; px++) {
              total += shapValues[y][x][px][classIndex];
            }

            // console.log(total);
            // if (total < 0) {
            //   ctx.fillStyle = "white";
            // } else {
            //   ctx.fillStyle = "blue";
            // }

            ctx.fillStyle = colorScale(total);
            let offset = 1
            ctx.fillRect(x * scaleX + offset, y * scaleY, scaleX - offset, scaleY - offset);
          }
        }

        return canvas.toDataURL();
      };

      const handleMouseMove = (event, classIndex) => {
        const mouseX = event.pageX;
        const mouseY = event.pageY;

        setMousePosition({ x: mouseX, y: mouseY });

        const shapValue = getShapValueAtPosition(mouseX, mouseY, classIndex);
        // console.log(shapValue);
        setTooltipContent(shapValue);
        // console.log(tooltipContent);
      };

      const getShapValueAtPosition = (mouseX, mouseY, classIndex) => {
        const container = containerRef.current;
        const imgElements = container.querySelectorAll("img");
      
        const imgElement = imgElements[classIndex];
        //  console.log(imgElement);
        // console.log();
        let rect = imgElement.getBoundingClientRect();

        const imgTop = rect.top + window.scrollY;
        const imgLeft = rect.left + window.scrollX;

        const yLen = shapValues.length;
        const xLen = shapValues[0].length;

        const scaleX = imgElement.clientWidth / yLen;
        const scaleY = imgElement.clientHeight / xLen;
        // console.log(`scaleY: ${scaleY}`);
        // console.log(`imgLeft: ${imgLeft}`);
        const shapX = Math.floor((mouseX - imgLeft) / scaleX);
        const shapY = Math.floor((mouseY - imgTop) / scaleY);
        // console.log(`shapX: ${shapX}`);
        // console.log(`mouseX: ${mouseX}`);
        // console.log(`shapY: ${shapY}`);
        // console.log(`mouseY: ${mouseY}`);
        // console.log(`classIndex: ${classIndex}`);
        // console.log(
        //   `shapValues[${shapY}][${shapX}][0][${classIndex}]: ${shapValues[shapY][shapX][0][classIndex]}`
        // );


        if (shapX < 0 || shapY < 0 || shapValues == null || shapY >= yLen || shapX >= xLen) return -1;

        let total = 0;
        for (let px = 0; px < 3; px++) {
          total += shapValues[shapY][shapX][px][classIndex];
        }

        return total;
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
          .attr("id", i)
          .style("display", "inline-block")
          .style("width", scaledImgWidth + "px")
          .style("height", scaledImgHeight + "px")
          .style("margin-bottom", "15px")
          .on("mousemove", (event) => handleMouseMove(event, i))
          .on("mouseenter", (event) => { setShowToolTip(true); })
          .on("mouseleave", (event) => { setShowToolTip(false); });
      }

      // Add scroll event listener
      containerRef.current.addEventListener("scroll", handleScroll);

      return () => {
        containerRef.current.removeEventListener("scroll", handleScroll);
      };
    };

    const handleScroll = () => {
        const container = containerRef.current;
        const images = container.querySelectorAll("img");
        
        const containerScrollTop = container.scrollTop;


        images.forEach((img, index) => {
        const imgTop = img.offsetTop;
        const imgHeight = img.clientHeight;
        const halfImgHeight = imgHeight / 2;

        if (containerScrollTop >= imgTop - halfImgHeight && containerScrollTop < imgTop + halfImgHeight) {
            const name = classNames[index];
            if (name != null) {
                setActiveClass(name);
                // console.log(classNames[index]);
            }
            
        }
        });
    };

    loadImageAndCreateOverlays();
  }, [imageUrl, shapValues, containerSize, classNames]);

  return (
    <div>
      <div className="relative w-[500px] h-[500px]">
        <div className="absolute top-0 left-0 p-2 bg-transparent text-black text-lg text-center z-10">
          Class: {activeClass}
        </div>
        <div
          className="w-full h-full overflow-y-scroll"
          ref={containerRef}
        ></div>
      </div>
      <div className="py-2 bg-white">
        <ColorScaleLegend
          min={-0.1}
          max={0.1}
          colorInterpolator={d3.interpolatePRGn}
          width={containerSize}
          height={20}
          textHeight={40}
        />
      </div>
      { showToolTip && tooltipContent != -1 ? (
        <div
          className="absolute bg-white border border-gray-300 p-2"
          style={{
            top: mousePosition.y + 10,
            left: mousePosition.x + 10,
            zIndex: 999,
          }}
        >
          {tooltipContent.toFixed(5)}
        </div>
      ) : null}
    </div>
  );
};

export default ShapExplainer;