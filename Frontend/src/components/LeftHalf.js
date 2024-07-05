
import React, { useEffect, useState } from "react";

import axios from "axios";
import HeatMap from "./HeatMap";
import Canvas from "./Canvas.js";

function LeftHalf() {


    const [image, setImage] = useState(null);
    const [data, setData] = useState(null);
    const [heatmapState, setHeatmapState] = useState(false);
    const uploadLink = "http://127.0.0.1:5000/limeshapexplain";

    const handleUpload = (event) => {
      setHeatmapState(false);
 
      const file = event.target.files[0];
      
      // create a new FormData object and append the file to it
      const formData = new FormData();
      formData.append("file", file);
      setImage(URL.createObjectURL(file));
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
          // console.log("Got data :)");
          console.log(response);
          setData(response.data);
          setHeatmapState(true);
	        
        })
        .catch((error) => {
          // handle errors
          console.log(error);
        })
      

      // console.log("Request sent!");
     
    };

    const handlePredict = () => {
    //   setPrediction("Error404"); // Placeholder for actual prediction logic
    };


    return (
      <div className="bottom-half py-5 px-5 bg-slate-200">
        {/* Show canvas and top buttons */}
        <div className="flex flex-col items-center h-screen">
          <div className="flex flex-none justify-start w-full px-4">
            <div className="upload-section mr-4">
              <input
                type="file"
                accept="image/*"
                onChange={handleUpload}
                id="file-upload"
                hidden
              />
              <label
                htmlFor="file-upload"
                className="py-5 px-10 rounded-md text-sm font-semibold bg-pink-50 text-pink-700 hover:bg-pink-100 cursor-pointer shadow-md"
              >
                UPLOAD IMAGE
              </label>
            </div>

            <div className="predict-section">
              <input type="button" accept="image/*" id="predict-class" hidden />
              <label
                htmlFor="predict-class"
                className="py-5 px-10 rounded-md text-sm font-semibold bg-pink-50 text-pink-700 hover:bg-pink-100 cursor-pointer shadow-md"
              >
                PREDICT CLASS
              </label>
            </div>
          </div>

          <div className="mt-8 shadow-xl rounded-md px-5 bg-pink-50">
            <Canvas
              imgUrl={image}
              width={400}
              height={400}
              imgWidth={140}
              imgHeight={140}
              posX={0}
              posY={0}
              count={1}
              alpha={100}
              // heatData={data}
            />
            {/* {<HeatMap heatData={data} />} */}
          </div>
        </div>
      </div>
    );
}

export default LeftHalf;
