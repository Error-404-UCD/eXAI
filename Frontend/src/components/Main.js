import React, { useState } from 'react';
import axios from 'axios';

import LeftHalf from './LeftHalf';
import RightHalf from './RightHalf';

const Main = () => {
    const [data, setData] = useState(null);
    const [imgUrl, setImgUrl] = useState(null);
    const uploadLink = "http://127.0.0.1:5000/limeshapexplain/gradient=False&&background=100&&mlModel=";

    const fetchData = (imgFile, mlModel) => {
        if (imgFile == null) return;
        const file = imgFile;

        console.log("Model type received: " + mlModel);
        let routeLink = uploadLink + mlModel;

        const formData = new FormData();
        formData.append("file", file);

        axios
            .post(routeLink, formData, {
                headers: {
                    "Content-Type": "multipart/form-data",
                },
            })
            .then((response) => {
                setData(response);
                setImgUrl(URL.createObjectURL(file));
            })
            .catch((error) => {
                console.log(error);
            });
    };

    return (
        <div className="flex flex-row justify-center">
            <LeftHalf fetchData={fetchData} />
            <RightHalf imageUrl={imgUrl} data={data} />
        </div>
    );
};

export default Main;
