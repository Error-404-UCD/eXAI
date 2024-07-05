import React, { useRef, useEffect } from 'react';

const Canvas = (data) => {
	const myCanvas = useRef();

	useEffect(() => {
	
			const context = myCanvas.current.getContext("2d");

	    	const image = new Image();
			if (data.imgUrl) image.src = data.imgUrl;
			const width = data.width
			const height = data.height;
	
		image.onload = () => {

			const imgAspectRatio = image.width / image.height;
			const canvasAspectRatio = width / height;
			let drawWidth, drawHeight;

			if (imgAspectRatio > canvasAspectRatio) {
				// Image is wider than canvas
				drawWidth = width;
				drawHeight = width / imgAspectRatio;
			} else {
				// Image is taller than canvas
				drawHeight = height;
				drawWidth = height * imgAspectRatio;
			}

			// Calculate the position to center the image
			const offsetX = (width - drawWidth) / 2;
			const offsetY = (height - drawHeight) / 2;

			// Clear the canvas
			context.clearRect(0, 0, width, height);

			// Draw the image

			context.drawImage(image, offsetX, offsetY, drawWidth, drawHeight);

			

			if(data.useGrayScale) {
				let imgData = context.getImageData(0, 0, data.width, data.height);
				for (let j = 0; j < imgData.data.length; j += 4) {
				const avg = (imgData.data[j] + imgData.data[j + 1] + imgData.data[j + 2]) / 3;
				imgData.data[j] = 255 - avg;
				imgData.data[j + 1] = 255 - avg;
				imgData.data[j + 2] = 255 - avg;
				imgData.data[j + 3] = data.alpha;
				}
				context.putImageData(imgData, 0, 0);
			}
			

			if (data.heatData != null) {
				var heatData = [];
				var ndata = data.heatData.shaparray[0][0];
					// Loop through all row pixels i
					for (var i = 0; i < ndata.length; ++i) {
					// Loop through all col pixels j
					for (var j = 0; j < ndata[i].length; ++j) {
					// For each number value 0...9 k
					for (var k = 0; k < ndata[i][j].length; ++k) {
					// Set new row = i
					// Set new col = k * count_of_cols + j
					// Set new val = data[i][j][k]
					const newVal = ndata[i][j][k];
					heatData.push({
						col: i,
						row: k * ndata[i].length + j,
						value: newVal,
					});

					}
					}
					}
					const getColor = (value) => {
						if (value < 0) {
							const blueIntensity = 255 * (1 + value / 0.1); // Map value from -0.1 to 0 to blue to white
							return 'red';
						} else if (value > 0) {
							const redIntensity = 255 * (value / 0.1); // Map value from 0 to 0.1 to white to red
							return 'blue';

						} else {
							return 'white';
						}
					};
					// console.log(heatData);
					heatData.forEach(point => {
					const { col, row, value } = point;
					const radius = 1; // Adjust radius as needed
					const color = "red";
					//console.log(row, col);
					context.fillStyle = getColor(value);
					context.beginPath();
					context.arc(row * 5, col * 5, radius, 0, 2 * Math.PI);
					context.fill();
				});
				

			} 

			// console.log(context.getImageData(0, 0, data.width, data.height));
	    	};
	  }, [data]);

  return <canvas ref={myCanvas} width={data.width} height={data.height} />;
};

export default Canvas;

