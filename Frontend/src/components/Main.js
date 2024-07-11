import React, { useState } from "react";
import axios from "axios";

import LeftHalf from "./LeftHalf";
import RightHalf from "./RightHalf";

const Main = () => {

    const [data, setData] = useState(null);
    const [imgUrl, setImgUrl] = useState(null);
    const uploadLink = "http://127.0.0.1:5000/limeshapexplain/False";

    const fetchData = async () => {
      try {
        const response = await fetch(uploadLink);
        const result = await response.json();
        setData(result);
      } catch (error) {
        console.error("Error fetching data:", error);
      }
    };

    const handleUpload = (event) => {

        const file = event.target.files[0];
        // setImage(URL.createObjectURL(file));
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
          // console.log("Got data :)");
            // console.log(response);
            setData(response);
            setImgUrl(URL.createObjectURL(file));
        //   setData(response.data);
        //   setHeatmapState(true);
        })
        .catch((error) => {
          // handle errors
          console.log(error);
        });

      // console.log("Request sent!");
    };

    return (
      <div className="flex flex-row">
        <LeftHalf fetchData={handleUpload} />
        <RightHalf imageUrl={imgUrl} data={data} />
      </div>
    );
};

export default Main;