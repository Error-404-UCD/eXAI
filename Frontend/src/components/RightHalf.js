import React, { useEffect, useState } from "react";
import Canvas from "./Canvas.js";
import LimeExplainer from "./LimeExplainer.js";
import ShapExplainer from "./ShapExplainer.js";

const RightHalf = ({imageUrl, data}) => {

    const [explainer, setExplainer] = useState("SHAP");

    const setExplanation = (event) => {
        
        setExplainer(event.target.value);
        // console.log(explainer);
    //   setPrediction("Error404"); // Placeholder for actual prediction logic
    };

    if(data != null) {
        console.log(data); 
    }


    return (
      <div className="bottom-half py-5 px-5 bg-slate-200">
        {/* Show canvas and options */}
        <div className="flex flex-col items-center h-screen">
          <div className="flex flex-none justify-start w-full py-4">
            <div className="flex flex-row mr-4 text-lg">
              <div className="">EXPLAINER</div>
              <div className="px-5">
                <select defaultValue="SHAP" onChange={setExplanation}>
                  <option value="LIME">LIME</option>
                  <option value="SHAP">SHAP</option>
                </select>
              </div>
            </div>
          </div>

          <div className="flex mt-7 shadow-xl rounded-md px-5 py-5 bg-white">
            {data ? (
              explainer == "LIME" ? (
                <LimeExplainer
                  className="flex"
                  imageUrl={imageUrl}
                  maskData={data.data.limearray.mask}
                  containerSize={500}
                />
              ) : explainer == "SHAP" ? (
                <ShapExplainer
                  imageUrl={imageUrl}
                  shapValues={data.data.shaparray[0]}
                  containerSize={500}
                  classNames={data.data.classes}
                />
              ) : (
                <Canvas
                  width={500}
                  height={500}
                  imgWidth={140}
                  imgHeight={140}
                  posX={0}
                  posY={0}
                  count={1}
                  alpha={100}
                  // heatData={data}
                />
              )
            ) : (
              <Canvas
                width={500}
                height={500}
                imgWidth={140}
                imgHeight={140}
                posX={0}
                posY={0}
                count={1}
                alpha={100}
                // heatData={data}
              />
            )}

            {/* {<HeatMap heatData={data} />} */}
          </div>
          {data ? (
            <div className="py-10">
              <label className="py-5 px-10 rounded-md text-lg font-bold bg-blue-400 text-white shadow-md">
                PREDICTION: {data.data.prediction}
              </label>
            </div>
          ) : null}
        </div>
      </div>
    );
}

export default RightHalf;