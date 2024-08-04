import React, { useState } from 'react';
import Canvas from './Canvas';

const LeftHalf = ({ fetchData }) => {
    const [image, setImage] = useState(null);
    const [imageFile, setImageFile] = useState(null);
    const [selectedModel, setSelectedModel] = useState("M1");

    const uploadImage = (event) => {
        if (event.target.files == 0) return;
        const file = event.target.files[0];
        setImageFile(file);
        setImage(URL.createObjectURL(file));
    };

    const handleModelChange = (event) => {
        setSelectedModel(event.target.value);
    };

    const handleImageChange = (event) => {
        uploadImage(event);
    };

    const handleDataFetch = () => {
        console.log(imageFile);
        fetchData(imageFile, selectedModel);
    };

    return (
      <div className="bottom-half py-5 px-5 bg-slate-200 h-full min-h-screen overflow-hidden" style={{height: '820px'}}>
        <div className="flex flex-col items-center h-full">
          <div className="w-full mb-4">
            <label htmlFor="model-select" className="block text-lg mb-2">CHOOSE ML MODEL:</label>
            <select
              id="model-select"
              defaultValue={"M1"}
              onChange={handleModelChange}
              className="rounded-md text-sm font-semibold bg-white text-pink-700 shadow-md border border-gray-300 focus:ring focus:ring-pink-200 focus:border-pink-500 w-full"
              style={{ height: '40px', fontSize: '16px', padding: '8px' }}
            >
              <option value="M1">Fully trained CNN Model</option>
              <option value="M2">Half trained CNN Model</option>
            </select>
          </div>

          <div className="flex w-full mb-4 space-x-4">
            <div className="flex-1">
              <input
                type="file"
                accept="image/*"
                onChange={handleImageChange}
                id="file-upload"
                hidden
              />
              <label
                htmlFor="file-upload"
                className="flex items-center justify-center py-2 px-4 rounded-md text-sm font-semibold bg-white text-pink-700 hover:bg-pink-100 cursor-pointer shadow-md w-full text-center"
                style={{ height: '40px', fontSize: '16px' }}
              >
                UPLOAD IMAGE
              </label>
            </div>
            <div className="flex-1">
              <input
                type="button"
                accept="image/*"
                onClick={handleDataFetch}
                id="predict-class"
                hidden
              />
              <label
                htmlFor="predict-class"
                className="flex items-center justify-center py-2 px-4 rounded-md text-sm font-semibold bg-white text-pink-700 hover:bg-pink-100 cursor-pointer shadow-md w-full text-center"
                style={{ height: '40px', fontSize: '16px' }}
              >
                PREDICT CLASS
              </label>
            </div>
          </div>

          <div className="mt-8 shadow-xl rounded-md px-5 py-5 bg-white relative">
            <Canvas
              imgUrl={image}
              width={400}
              height={400}
              alpha={100}
              isPaintable={true}
              onExport={(url) => setImageFile(url)}
            />
          </div>
        </div>
      </div>
    );
};

export default LeftHalf;
