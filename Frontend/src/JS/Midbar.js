import React, { useState } from 'react';
import '../CSS/Midbar.css'; 

function Midbar() {
    const [image, setImage] = useState(null);
    const [prediction, setPrediction] = useState('');

    const handleUpload = (event) => {
        setImage(URL.createObjectURL(event.target.files[0]));
    };

    const handlePredict = () => {
        setPrediction('Error404'); // Placeholder for actual prediction logic
    };

    return (
        <div className="midbar">
            <div className="upload-section">
                <input type="file" accept="image/*" onChange={handleUpload} id="file-upload" className="file-input" />
                <label htmlFor="file-upload" className="upload-button">Upload Image</label>
                {image && <span className="file-status">File Uploaded</span>}
            </div>
            <div className="predict-section">
                <button onClick={handlePredict} className="predict-button">Predict</button>
                {prediction && <span className="prediction-result">{prediction}</span>}
            </div>
        </div>
    );
}

export default Midbar;
