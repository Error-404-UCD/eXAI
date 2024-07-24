import React, { useRef, useEffect, useState } from "react";

const Canvas = ({
  imgUrl,
  width,
  height,
  alpha,
  useGrayScale,
  isPaintable,
  onExport,
}) => {
  const myCanvas = useRef();
  const [isPainting, setIsPainting] = useState(false);
  const [isPaintEnabled, setIsPaintEnabled] = useState(false);
  const [brushSize, setBrushSize] = useState(3);
  const [lineColor, setLineColor] = useState("#FFFFFF");
  const [context, setContext] = useState(null);
  const [uploadedImage, setUploadedImage] = useState(null);

  useEffect(() => {
    const canvas = myCanvas.current;
    canvas.width = width;
    canvas.height = height;
    const ctx = canvas.getContext("2d");
    ctx.fillStyle = "white";
    ctx.fillRect(0, 0, width, height);
    setContext(ctx);

    if (imgUrl) {
      const image = new Image();
      image.src = imgUrl;
      setUploadedImage(image);

      image.onload = () => {
        drawImageOnCanvas(ctx, image);
      };
    }
  }, [imgUrl, width, height, alpha, useGrayScale]);

  const drawImageOnCanvas = (ctx, image) => {
    const imgAspectRatio = image.width / image.height;
    const canvasAspectRatio = width / height;
    let drawWidth, drawHeight;

    if (imgAspectRatio > canvasAspectRatio) {
      drawWidth = width;
      drawHeight = width / imgAspectRatio;
    } else {
      drawHeight = height;
      drawWidth = height * imgAspectRatio;
    }

    const offsetX = (width - drawWidth) / 2;
    const offsetY = (height - drawHeight) / 2;

    ctx.clearRect(0, 0, width, height);
    ctx.fillStyle = "white";
    ctx.fillRect(0, 0, width, height);
    ctx.imageSmoothingEnabled = false;
    ctx.drawImage(image, offsetX, offsetY, drawWidth, drawHeight);

    if (useGrayScale) {
      let imgData = ctx.getImageData(0, 0, width, height);
      for (let j = 0; j < imgData.data.length; j += 4) {
        const avg =
          (imgData.data[j] + imgData.data[j + 1] + imgData.data[j + 2]) / 3;
        imgData.data[j] = 255 - avg;
        imgData.data[j + 1] = 255 - avg;
        imgData.data[j + 2] = 255 - avg;
        imgData.data[j + 3] = alpha;
      }
      ctx.putImageData(imgData, 0, 0);
    }
  };

  const getGridCoords = (event) => {
    const rect = myCanvas.current.getBoundingClientRect();
    const x = event.clientX - rect.left;
    const y = event.clientY - rect.top;
    const cellWidth = width / 28;
    const cellHeight = height / 28;
    const gridX = Math.floor(x / cellWidth) * cellWidth;
    const gridY = Math.floor(y / cellHeight) * cellHeight;
    return { gridX, gridY, cellWidth, cellHeight };
  };

  const drawBrush = (x, y, size, color) => {
    const cellWidth = width / 28;
    const cellHeight = height / 28;

    for (let i = -1; i <= 1; i++) {
      for (let j = -1; j <= 1; j++) {
        if (size === 1 && (i !== 0 || j !== 0)) continue;
        if (size === 2 && (Math.abs(i) > 1 || Math.abs(j) > 1)) continue;

        const offsetX = i * cellWidth;
        const offsetY = j * cellHeight;

        let finalOpacity = 1;
        if (size === 3) {
          if (i === 0 && j === 0) {
            finalOpacity = 1;
          } else if (Math.abs(i) === 1 && Math.abs(j) === 1) {
            finalOpacity = 0.2;
          } else {
            finalOpacity = 0.5;
          }
        }

        context.fillStyle = `${color}${Math.floor(finalOpacity * 255)
          .toString(16)
          .padStart(2, "0")}`;
        context.fillRect(x + offsetX, y + offsetY, cellWidth, cellHeight);
      }
    }
  };

  const startPaint = (event) => {
    if (!isPaintEnabled || !context) return;
    const { gridX, gridY } = getGridCoords(event);
    drawBrush(gridX, gridY, brushSize, lineColor);
    setIsPainting(true);
  };

  const paint = (event) => {
    if (!isPainting || !isPaintEnabled) return;
    const { gridX, gridY } = getGridCoords(event);
    drawBrush(gridX, gridY, brushSize, lineColor);
  };

  const stopPaint = () => {
    if (isPainting) {
      setIsPainting(false);
      exportCanvasAsJPEG(); // Export after painting is done
    }
  };

  const clearCanvas = () => {
    if (context) {
      context.clearRect(0, 0, myCanvas.current.width, myCanvas.current.height);
      if (uploadedImage) {
        drawImageOnCanvas(context, uploadedImage);
      } else {
        context.fillStyle = "white";
        context.fillRect(0, 0, width, height);
      }
       exportCanvasAsJPEG();
    }
  };

  const exportCanvasAsJPEG = () => {
    const canvas = myCanvas.current;
    const tempCanvas = document.createElement("canvas");
    tempCanvas.width = 28;
    tempCanvas.height = 28;
    const tempCtx = tempCanvas.getContext("2d");

    // Draw the scaled content onto the temporary canvas
    tempCtx.drawImage(canvas, 0, 0, width, height, 0, 0, 28, 28);

    // Convert the temporary canvas to a data URL (JPEG format)
    const dataURL = tempCanvas.toDataURL("image/jpeg");

    // Convert the data URL to a Blob
    fetch(dataURL)
      .then((res) => res.blob())
      .then((blob) => {
        // Create a File from the Blob
        const file = new File([blob], "exported-image.jpg", {
          type: "image/jpeg",
        });

        // Call the onExport callback with the File object
        if (onExport) {
          onExport(file);
        }
      });
  };

  return (
    <div>
      {isPaintable && uploadedImage ? (
        <div className="flex items-center justify-center mb-4">
          <span className="mr-4 text-xl font-bold">Edit Image</span>
          <label className="flex items-center">
            <input
              type="checkbox"
              className="sr-only"
              checked={isPaintEnabled}
              onChange={() => setIsPaintEnabled(!isPaintEnabled)}
            />
            <div className="w-12 h-6 bg-gray-200 rounded-full peer-focus:ring-4 peer-focus:ring-blue-300 dark:peer-focus:ring-blue-800 dark:bg-gray-700">
              <div
                className={`w-6 h-6 bg-white rounded-full shadow-md transform transition-transform duration-300 ${
                  isPaintEnabled ? "translate-x-6" : ""
                }`}
              ></div>
            </div>
          </label>
        </div>
      ) : null}

      <canvas
        ref={myCanvas}
        width={width}
        height={height}
        onMouseDown={startPaint}
        onMouseMove={paint}
        onMouseUp={stopPaint}
        onMouseLeave={stopPaint}
      />
      {isPaintEnabled && (
        <div>
          <div className="flex justify-center items-center mb-2 py-3">
            <label className="mr-1">Color:</label>
            <input
              type="color"
              value={lineColor}
              className="w-16 p-1 border-2 border-gray-300 mr-4"
              onChange={(e) => setLineColor(e.target.value)}
            />
            <button
              className="bg-red-500 px-4 py-2 rounded text-white cursor-pointer"
              onClick={clearCanvas}
            >
              Reset
            </button>
          </div>
        </div>
      )}
    </div>
  );
};

export default Canvas;
