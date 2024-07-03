import React, { useRef, useEffect, useState } from 'react';
import '../CSS/TopHalf.css';

function TopHalf() {
    const canvasRef = useRef(null);
    const [isPainting, setIsPainting] = useState(false);
    const [tool, setTool] = useState('brush');
    const [lineWidth, setLineWidth] = useState(5);
    const [lineColor, setLineColor] = useState('#000000');
    const [context, setContext] = useState(null);

    // Set up the canvas context once on mount
    useEffect(() => {
        const canvas = canvasRef.current;
        canvas.width = 560;
        canvas.height = 200;
        setContext(canvas.getContext('2d'));
    }, []);

    // Adjust context properties based on the current tool
    useEffect(() => {
        if (context) {
            context.lineWidth = lineWidth;
            context.strokeStyle = tool === 'eraser' ? '#FFFFFF' : lineColor; // Eraser uses white color
        }
    }, [context, lineWidth, lineColor, tool]);

    const startPaint = (event) => {
        if (!context) return;
        const rect = canvasRef.current.getBoundingClientRect();
        const x = event.clientX - rect.left;
        const y = event.clientY - rect.top;
        context.beginPath();
        context.moveTo(x, y);
        setIsPainting(true);
    };

    const paint = (event) => {
        if (!isPainting) return;
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
        <div className="top-half">
            <div className="card card1">
                <h3>Card 1</h3>
                <p>Details for Card 1</p>
            </div>
            <div className="card card2">
                <h3>Card 2</h3>
                <p>Details for Card 2</p>
            </div>
            <div className="card card3">
                <h3>Card 3 - Paint Tool</h3>
                <canvas ref={canvasRef} style={{ border: '2px solid black' }} onMouseDown={startPaint} onMouseMove={paint} onMouseUp={stopPaint} onMouseLeave={stopPaint}></canvas>
                <div>
                    <button className={tool === 'brush' ? 'active' : ''} onClick={() => setTool('brush')}>Brush</button>
                    <button className={tool === 'eraser' ? 'active' : ''} onClick={() => setTool('eraser')}>Eraser</button>
                    <label>Size:</label>
                    <input type="range" min="1" max="20" value={lineWidth} onChange={e => setLineWidth(e.target.value)} />
                    <label>Color:</label>
                    <input type="color" value={lineColor} onChange={e => setLineColor(e.target.value)} />
                    <button onClick={clearCanvas}>Clear Screen</button>
                </div>
            </div>
        </div>
    );
}

export default TopHalf;
