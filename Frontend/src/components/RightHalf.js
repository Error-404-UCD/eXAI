
import React, { useEffect, useState } from "react";
import Canvas from "./Canvas.js";
import LimeExplainer from "./LimeExplainer.js";
import ShapExplainer from "./ShapExplainer.js";
import { AiOutlineInfoCircle } from "react-icons/ai"; // Import the icon
import Modal from "./Modal"; // Import the modal component

const RightHalf = ({ imageUrl, data, isFetching }) => {
  const [explainer, setExplainer] = useState("SHAP");
  const [isModalOpen, setIsModalOpen] = useState(false); // State to control modal visibility

  const setExplanation = (event) => {
    setExplainer(event.target.value);
  };

  if (data != null) {
    console.log(data);
  }

  return (
    <div className="bottom-half py-5 px-5 bg-slate-200 h-full min-h-screen overflow-hidden" style={{ height: '820px' }}>
      {/* Show canvas and options */}
      <div className="flex flex-col items-center h-screen">
        <div className="flex flex-none justify-start w-full items-center mb-4">
          <div className="w-full relative">
            <label htmlFor="explanation-select" className="block text-lg mb-2">
              CHOOSE EXPLAINER:
            </label>
            <select
              id="explanation-select"
              defaultValue="SHAP"
              onChange={setExplanation}
              className="rounded-md text-sm font-semibold bg-white text-pink-700 shadow-md border border-gray-300 focus:ring focus:ring-pink-200 focus:border-pink-500 w-full"
              style={{ height: "40px", fontSize: "16px" }}
            >
              <option value="LIME">LIME</option>
              <option value="SHAP">SHAP</option>
            </select>
            <AiOutlineInfoCircle
              onClick={() => setIsModalOpen(true)}
              className="absolute top-0 right-0 transform -translate-y-1/2 text-4xl cursor-pointer text-blue-500 hover:text-blue-700"
            />
          </div>
        </div>

        {data ? (
          <div className="relative w-full">
            <div
              className="py-2 px-4 rounded-md text-sm font-semibold bg-white text-pink-700 hover:bg-pink-100 cursor-pointer shadow-md w-full text-center"
              style={{ height: "40px", fontSize: "16px" }}
            >
              PREDICTION: {data.data.prediction}
            </div>
          </div>
        ) : null}

        <div className="flex mt-7 shadow-xl rounded-md px-5 py-5 bg-white w-full">
          {data ? (
            explainer === "LIME" ? (
              <LimeExplainer
                className="flex"
                imageUrl={imageUrl}
                maskData={data.data.limearray.mask}
                containerSize={500}
              />
            ) : explainer === "SHAP" ? (
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
        </div>
      </div>
      {isFetching && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
          <div className="bg-white p-4 rounded-lg shadow-lg flex items-center">
            <div className="loader mr-3 border-4 border-t-4 border-t-blue-500 border-gray-200 rounded-full w-8 h-8 animate-spin"></div>
            <p>Fetching data, please wait...</p>
          </div>
        </div>
      )}
      <Modal isOpen={isModalOpen} onClose={() => setIsModalOpen(false)} />
    </div>
  );
};

export default RightHalf;

