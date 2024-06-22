
import '../CSS/BottomHalf.css';
import React, { useEffect, useState } from "react";
import "../CSS/Midbar.css";
import axios from "axios";
import HeatMap from "./HeatMap";


function BottomHalf() {


    const [image, setImage] = useState(null);
    const [data, setData] = useState(null);
    const [testState, setState] = useState(false);
    const uploadLink = "http://127.0.0.1:5000/upload";

    const handleUpload = (event) => {
        setState(false);
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
        //   console.log(response);
          setData(response.data);
          setState(true);
        })
        .catch((error) => {
          // handle errors
          console.log(error);
        });

      // console.log("Request sent!");
      //setImage();
    };

    const handlePredict = () => {
    //   setPrediction("Error404"); // Placeholder for actual prediction logic
    };


    return (
      <div className="bottom-half">
        <div className="midbar">
          <div className="upload-section">
            <input
              type="file"
              accept="image/*"
              onChange={handleUpload}
              id="file-upload"
              className="file-input"
            />
            <label htmlFor="file-upload" className="upload-button">
              Upload Image
            </label>
            {image && <span className="file-status">File Uploaded</span>}
          </div>
          <div className="predict-section">
            <button onClick={handlePredict} className="predict-button">
              Predict
            </button>
            {/* {prediction && (
              <span className="prediction-result">{prediction}</span>
            )} */}
          </div>
        </div>
        <div className="card card1">
          <h3>Card 1</h3>
          {/* {data} */}
          <p>Details for Card 1</p>

          {testState ? <HeatMap heatData={data} /> : null}
        </div>
        {/* <div className="card card2">
                <h3>Card 2</h3>
                <p>Details for Card 2</p>
            </div> */}
      </div>
    );
}

export default BottomHalf;
