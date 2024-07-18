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
        // console.log(imageFile);
        fetchData(imageFile, selectedModel);
    };

    return (
        <div className="bottom-half py-5 px-5 bg-slate-200">
            <div className="flex flex-col items-center h-screen">
                <div className="flex flex-none justify-start w-full py-4">
                    <div className="upload-section mr-4">
                        <input
                            type="file"
                            accept="image/*"
                            onChange={handleImageChange}
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

                    <div className="predict-section">
                        <input
                            type="button"
                            accept="image/*"
                            onClick={handleDataFetch}
                            id="predict-class"
                            hidden
                        />
                        <label
                            htmlFor="predict-class"
                            className="py-5 px-10 rounded-md text-sm font-semibold bg-white text-pink-700 hover:bg-pink-100 cursor-pointer shadow-md"
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
                        
                        
                    />
                </div>

                <div className="flex flex-row mr-4 text-lg py-5">
                    <div className="px-5">DATASET</div>
                    <select
                        // onChange={console.log("Dataset changed")}
                        defaultValue={"MNIST"}
                    >
                        <option value="MNIST">MNIST</option>
                        <option value="Astro">Astronomy</option>
                        <option value="BM">Bone Marrow</option>
                    </select>
                </div>
                <div className="flex flex-row mr-4 text-lg">
                    <div className="px-5">ML Model</div>
                    <select defaultValue={"M1"} onChange={handleModelChange}>
                        <option value="M1">Super_CNN</option>
                        <option value="M2">Tiny_CNN</option>
                    </select>
                </div>
            </div>
        </div>
    );
};

export default LeftHalf;
