import React, { useState } from 'react';
import axios from 'axios';

import LeftHalf from './LeftHalf';
import RightHalf from './RightHalf';

const Main = () => {
    const [data, setData] = useState(null);
    const [imgUrl, setImgUrl] = useState(null);
    const [isFetching, setIsFetching] = useState(false);
    const uploadLink = "http://127.0.0.1:5000/limeshapexplain/gradient=False&&background=100&&mlModel=";

    let busy = false;
    const fetchData = (imgFile, mlModel) => {
        if (imgFile == null) return;
        const file = imgFile;

        console.log("Model type received: " + mlModel);
        let routeLink = uploadLink + mlModel;

        const formData = new FormData();
        formData.append("file", file);

        if (!busy) {
            busy = true;
            setIsFetching(true);
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
              })
              .finally(() => { 
                busy = false; 
                setIsFetching(false);
              });
        } else {
            console.log("Wait! I am busy ;)")
        }
    };

    return (
        <div className="flex flex-row justify-center h-screen overflow-auto">
            <LeftHalf fetchData={fetchData} />
            <RightHalf imageUrl={imgUrl} data={data} isFetching={isFetching} />
        </div>
    );
};

export default Main;
