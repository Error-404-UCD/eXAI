import React, { useRef, useEffect } from 'react';

const Canvas = (data) => {
	const myCanvas = useRef();

	useEffect(() => {
		const context = myCanvas.current.getContext("2d");
	    	const image = new Image();
	    	image.src = data.imgUrl;
	
		image.onload = () => {
			for(let i = 0; i < data.count; ++i) {
	      			context.drawImage(image, data.posX + i * data.imgWidth, data.posY, data.imgWidth, data.imgHeight);
			}
			let imgData = context.getImageData(0, 0, data.width, data.height);
			for (let j = 0; j < imgData.data.length; j += 4) {
				const avg = (imgData.data[j] + imgData.data[j + 1] + imgData.data[j + 2]) / 3;
                  		imgData.data[j] = 255 - avg;
                		imgData.data[j + 1] = 255 - avg;
                		imgData.data[j + 2] = 255 - avg;
				imgData.data[j + 3] = data.alpha;
            		}
			context.putImageData(imgData, 0, 0);
			// console.log(context.getImageData(0, 0, data.width, data.height));
	    	};
	  }, [data]);

  return <canvas ref={myCanvas} width={data.width} height={data.height} />;
};

export default Canvas;

