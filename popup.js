document.getElementById("analyzeBtn").addEventListener("click", () => {
    const text = document.getElementById("inputText").value;
  
    fetch("http://127.0.0.1:5000/predict_json", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ text })  // <-- correct key
    })
    .then(response => response.json())
    .then(data => {
      document.getElementById("result").textContent = `Prediction: ${data.prediction} (Confidence: ${data.confidence}%)`;
    })
    .catch(error => {
      document.getElementById("result").textContent = "Error connecting to API.";
      console.error("Error:", error);
    });
});
