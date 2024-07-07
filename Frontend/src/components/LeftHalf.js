
import React, { useEffect, useState } from "react";


import HeatMap from "./HeatMap";
import Canvas from "./Canvas.js";

const LeftHalf = ({fetchData}) => {


    const [image, setImage] = useState(null);
    const [data, setData] = useState(null);
    const [heatmapState, setHeatmapState] = useState(false);
    

    const uploadImage = (event) => {
        const file = event.target.files[0];
        setImage(URL.createObjectURL(file));
    }
    

    const handlePredict = () => {
    //   setPrediction("Error404"); // Placeholder for actual prediction logic
    };


    return (
      <div className="bottom-half py-5 px-5 bg-slate-200">
        {/* Show canvas and top buttons */}
        <div className="flex flex-col items-center h-screen">
          <div className="flex flex-none justify-start w-full py-4">
            <div className="upload-section mr-4">
              <input
                type="file"
                accept="image/*"
                onChange={(event) => {fetchData(event); uploadImage(event);}}
                id="file-upload"
                hidden
              />
              <label
                htmlFor="file-upload"
                className="py-5 px-10 rounded-md text-sm font-semibold bg-white text-pink-700 hover:bg-pink-100 cursor-pointer shadow-md"
              >
                UPLOAD IMAGE
              </label>
            </div>

            {/* <div className="predict-section">
              <input type="button" accept="image/*" id="predict-class" hidden />
              <label
                htmlFor="predict-class"
                className="py-5 px-10 rounded-md text-sm font-semibold bg-white text-pink-700 hover:bg-pink-100 cursor-pointer shadow-md"
              >
                PREDICT CLASS
              </label>
            </div> */}
          </div>

          <div className="mt-8 shadow-xl rounded-md px-5 py-5 bg-white">
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

          <div className="flex flex-row mr-4 text-lg py-5">
            <div className="">DATASET</div>
            <div className="px-5">
              <select onChange={console.log("Dataset changed")}>
                <option value="Astro">Astronomy</option>
                <option value="BM">Bone Marrow</option>
              </select>
            </div>
          </div>

          
          
        </div>
      </div>
    );
}

export default LeftHalf;
