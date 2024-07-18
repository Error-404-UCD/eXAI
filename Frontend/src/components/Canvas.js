import React, { useRef, useEffect, useState } from 'react';

const Canvas = ({ imgUrl, width, height, imgWidth, imgHeight, posX, posY, count, alpha, useGrayScale, heatData }) => {
    const myCanvas = useRef();
    const [isPainting, setIsPainting] = useState(false);
    const [isPaintEnabled, setIsPaintEnabled] = useState(false);
    const [tool, setTool] = useState('brush');
    const [lineWidth, setLineWidth] = useState(5);
    const [lineColor, setLineColor] = useState('#FF0000');
    const [context, setContext] = useState(null);

    useEffect(() => {
        const canvas = myCanvas.current;
        canvas.width = width;
        canvas.height = height;
        const ctx = canvas.getContext('2d');
        setContext(ctx);

        const image = new Image();
        if (imgUrl) image.src = imgUrl;

        image.onload = () => {
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
            ctx.imageSmoothingEnabled = false;
            ctx.drawImage(image, offsetX, offsetY, drawWidth, drawHeight);

            if (useGrayScale) {
                let imgData = ctx.getImageData(0, 0, width, height);
                for (let j = 0; j < imgData.data.length; j += 4) {
                    const avg = (imgData.data[j] + imgData.data[j + 1] + imgData.data[j + 2]) / 3;
                    imgData.data[j] = 255 - avg;
                    imgData.data[j + 1] = 255 - avg;
                    imgData.data[j + 2] = 255 - avg;
                    imgData.data[j + 3] = alpha;
                }
                ctx.putImageData(imgData, 0, 0);
            }

            if (heatData != null) {
                var heatDataPoints = [];
                var ndata = heatData.shaparray[0][0];
                for (var i = 0; i < ndata.length; ++i) {
                    for (var j = 0; j < ndata[i].length; ++j) {
                        for (var k = 0; k < ndata[i][j].length; ++k) {
                            const newVal = ndata[i][j][k];
                            heatDataPoints.push({
                                col: i,
                                row: k * ndata[i].length + j,
                                value: newVal,
                            });
                        }
                    }
                }
                const getColor = (value) => {
                    if (value < 0) {
                        const blueIntensity = 255 * (1 + value / 0.1);
                        return 'red';
                    } else if (value > 0) {
                        const redIntensity = 255 * (value / 0.1);
                        return 'blue';
                    } else {
                        return 'white';
                    }
                };
                heatDataPoints.forEach(point => {
                    const { col, row, value } = point;
                    const radius = 1;
                    context.fillStyle = getColor(value);
                    context.beginPath();
                    context.arc(row * 5, col * 5, radius, 0, 2 * Math.PI);
                    context.fill();
                });
            }
        };
    }, [imgUrl, width, height, useGrayScale, alpha, heatData]);

    useEffect(() => {
        if (context) {
            context.lineWidth = lineWidth;
            context.strokeStyle = tool === 'eraser' ? '#FFFFFF' : lineColor;
            context.lineCap = 'round';
        }
    }, [context, lineWidth, lineColor, tool]);

    const startPaint = (event) => {
        if (!isPaintEnabled || !context) return;
        const rect = myCanvas.current.getBoundingClientRect();
        const x = event.clientX - rect.left;
        const y = event.clientY - rect.top;
        context.beginPath();
        context.moveTo(x, y);
        setIsPainting(true);
    };

    const paint = (event) => {
        if (!isPainting || !isPaintEnabled) return;
        const rect = myCanvas.current.getBoundingClientRect();
        const x = event.clientX - rect.left;
        const y = event.clientY - rect.top;
        context.lineTo(x, y);
        context.stroke();
    };

    const stopPaint = () => {
        if (isPainting) {
            context.closePath();
            setIsPainting(false);
        }
    };

    const clearCanvas = () => {
        if (context) {
            context.clearRect(0, 0, myCanvas.current.width, myCanvas.current.height);
        }
    };

    return (
        <div>
            <div className="flex items-center justify-center mb-4">
                <span className="mr-4 text-xl font-bold">Paint Tool</span>
                <label className="flex items-center">
                    <input type="checkbox" className="sr-only" checked={isPaintEnabled} onChange={() => setIsPaintEnabled(!isPaintEnabled)} />
                    <div className="w-12 h-6 bg-gray-200 rounded-full peer-focus:ring-4 peer-focus:ring-blue-300 dark:peer-focus:ring-blue-800 dark:bg-gray-700">
                        <div className={`w-6 h-6 bg-white rounded-full shadow-md transform transition-transform duration-300 ${isPaintEnabled ? 'translate-x-6' : ''}`}></div>
                    </div>
                </label>
            </div>
            <canvas ref={myCanvas} width={width} height={height} onMouseDown={startPaint} onMouseMove={paint} onMouseUp={stopPaint} onMouseLeave={stopPaint} className="border-2 border-gray-300 mb-4" />
            {isPaintEnabled && (
                <div>
                    <div className="flex justify-start items-center mb-2">
                        <button className={`mr-2 px-4 py-2 rounded cursor-pointer ${tool === 'brush' ? 'bg-blue-500 text-white' : 'bg-gray-200'}`} onClick={() => setTool('brush')}>Brush</button>
                        <button className={`mr-2 px-4 py-2 rounded cursor-pointer ${tool === 'eraser' ? 'bg-blue-500 text-white' : 'bg-gray-200'}`} onClick={() => setTool('eraser')}>Eraser</button>
                        <label className="ml-2 mr-1">Size:</label>
                        <input type="range" min="1" max="20" value={lineWidth} className="w-24" onChange={e => setLineWidth(e.target.value)} />
                    </div>
                    <div className="flex justify-start items-center">
                        <label className="mr-1">Color:</label>
                        <input type="color" value={lineColor} className="w-16 p-1 border-2 border-gray-300 mr-4" onChange={e => setLineColor(e.target.value)} />
                        <button className="bg-red-500 px-4 py-2 rounded text-white cursor-pointer" onClick={clearCanvas}>Clear</button>
                    </div>
                </div>
            )}
        </div>
    );
};

export default Canvas;
