document.getElementById('upload-form').onsubmit = async function (e) {
    e.preventDefault();

    const formData = new FormData(this);
    const resultText = document.getElementById('result');
    resultText.innerText = "Processing...";

    try {
        const response = await fetch('/predict', {
            method: 'POST',
            body: formData
        });

        const result = await response.json();

        if (result.prediction) {
            resultText.innerText = `Prediction: ${result.prediction}\nConfidence: ${result.confidence}`;
        } else {
            resultText.innerText = `Error: ${result.error}`;
        }

    } catch (error) {
        resultText.innerText = `Error: ${error.message}`;
    }
};
