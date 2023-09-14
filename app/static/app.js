const canvas = document.getElementById('canvas');
const context = canvas.getContext('2d');
const submitBtn = document.getElementById('submitBtn');
const clearBtn = document.getElementById('clearBtn');
const predictionDiv = document.getElementById('prediction');


const hiragana = {
    0: "お",
    1: "き",
    2: "す",
    3: "つ",
    4: "な",
    5: "は",
    6: "ま",
    7: "や",
    8: "れ",
    9: "を"
};


let isDrawing = false;

canvas.addEventListener('mousedown', () => {
    isDrawing = true;
    context.beginPath();
});

canvas.addEventListener('mousemove', (event) => {
    if (!isDrawing) return;
    context.lineWidth = 10;
    context.lineCap = 'round';
    context.strokeStyle = 'black';
    context.lineTo(event.clientX - canvas.offsetLeft, event.clientY - canvas.offsetTop);
    context.stroke();
});

canvas.addEventListener('mouseup', () => {
    isDrawing = false;
    context.closePath();
});

clearBtn.addEventListener('click', () => {
    context.clearRect(0, 0, canvas.width, canvas.height);
});


submitBtn.addEventListener('click', async () => {
    const imageData = canvas.toDataURL('image/png');
    const link = document.createElement('a');
    link.href = imageData;
    //link.download = 'drawing.png'; // save image to check whats being sent
    link.click();
    const response = await fetch('http://localhost:8000/predict', {
        method: 'POST',
        body: JSON.stringify({ image_data: imageData }),
        headers: {
            'Content-Type': 'application/json'
        }
    });
    const result = await response.json();

    const predictedCharacter = hiragana[result["prediction"]];
    console.log("Result isssssssssssssssssss:", predictedCharacter);
    predictionDiv.textContent = `Prediction: ${predictedCharacter}`;


});
