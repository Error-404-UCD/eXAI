import React, { useState } from 'react';
import '../CSS/Midbar.css'; 
import axios from "axios";
import BottomHalf from "./BottomHalf";

function Midbar() {
    const [image, setImage] = useState(null);
    const [prediction, setPrediction] = useState('');
    const uploadLink = "http://127.0.0.1:5000/upload";

    const handleUpload = (event) => {
      const file = event.target.files[0];
      // create a new FormData object and append the file to it
      const formData = new FormData();
      formData.append("file", file);

      // make a POST request to the File Upload API with the FormData object and Rapid API headers
      // Reference: https://www.npmjs.com/package/axios
      axios
        .post(uploadLink, formData, {
          headers: {
            "Content-Type": "multipart/form-data",
          },
        })
        .then((response) => {
          // handle the response
          console.log("Got data :)");
          console.log(response);
        })
        .catch((error) => {
          // handle errors
          console.log(error);
        });

      console.log("Request sent!");
      //setImage();
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
