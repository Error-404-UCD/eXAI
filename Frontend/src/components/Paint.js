import React, { useRef, useEffect, useState } from 'react';

const Paint = ({ width, height }) => {
    const canvasRef = useRef(null);
    const [isPainting, setIsPainting] = useState(false);
    const [isPaintEnabled, setIsPaintEnabled] = useState(false);
    const [tool, setTool] = useState('brush');
    const [lineWidth, setLineWidth] = useState(5);
    const [lineColor, setLineColor] = useState('#FF0000');
    const [context, setContext] = useState(null);

    useEffect(() => {
        const canvas = canvasRef.current;
        canvas.width = width;
        canvas.height = height;
        const ctx = canvas.getContext('2d');
        setContext(ctx);
    }, [width, height]);

    useEffect(() => {
        if (context) {
            context.lineWidth = lineWidth;
            context.strokeStyle = tool === 'eraser' ? '#FFFFFF' : lineColor;
            context.lineCap = 'round';
        }
    }, [context, lineWidth, lineColor, tool]);

    const startPaint = (event) => {
        if (!isPaintEnabled || !context) return;
        const rect = canvasRef.current.getBoundingClientRect();
        const x = event.clientX - rect.left;
        const y = event.clientY - rect.top;
        context.beginPath();
        context.moveTo(x, y);
        setIsPainting(true);
    };

    const paint = (event) => {
        if (!isPainting || !isPaintEnabled) return;
        const rect = canvasRef.current.getBoundingClientRect();
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
            context.clearRect(0, 0, canvasRef.current.width, canvasRef.current.height);
        }
    };

    return (
        <div className="p-4 shadow-lg rounded-lg bg-white text-center">
            <div className="flex items-center justify-center mb-4">
                <span className="mr-4 text-xl font-bold">Paint Tool</span>
                <label className="flex items-center">
                    <input type="checkbox" className="sr-only" checked={isPaintEnabled} onChange={() => setIsPaintEnabled(!isPaintEnabled)} />
                    <div className="w-12 h-6 bg-gray-200 rounded-full peer-focus:ring-4 peer-focus:ring-blue-300 dark:peer-focus:ring-blue-800 dark:bg-gray-700">
                        <div className={`w-6 h-6 bg-white rounded-full shadow-md transform transition-transform duration-300 ${isPaintEnabled ? 'translate-x-6' : ''}`}></div>
                    </div>
                </label>
            </div>
            <canvas ref={canvasRef} className="border-2 border-gray-300 mb-4" onMouseDown={startPaint} onMouseMove={paint} onMouseUp={stopPaint} onMouseLeave={stopPaint}></canvas>
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

export default Paint;
