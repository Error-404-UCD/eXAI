import React, { useEffect, useState } from "react";
import Canvas from "./Canvas.js";

function RightHalf() {

    return (
      <div className="bottom-half py-5 px-5 bg-slate-200">
        {/* Show canvas and options */}
        <div className="flex flex-col items-center h-screen">
          <div className="flex flex-none justify-start w-full py-4">
            <div className="flex flex-row mr-4 text-lg">
              <div className="">EXPLAINER</div>
              <div className="px-5">
                <select value="Option 1">
                  <option value="Option 1">LIME</option>
                  <option value="Option 2">SHAP</option>
                </select>
              </div>
            </div>
          </div>

          <div className="mt-7 shadow-xl rounded-md px-5 py-5 bg-white">
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
            {/* {<HeatMap heatData={data} />} */}
          </div>
        </div>
      </div>
    );
}

export default RightHalf;