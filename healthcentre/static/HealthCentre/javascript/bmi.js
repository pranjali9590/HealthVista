function calculateBMI() {
    var height = parseFloat(document.getElementById("height").value);
    var weight = parseFloat(document.getElementById("weight").value);
    var heightUnit = document.getElementById("heightUnit").value;
    var weightUnit = document.getElementById("weightUnit").value;
    
    // Clear any previous error messages
    var resultElement = document.getElementById("result");
    resultElement.innerHTML = ""; // Clear the result element
    resultElement.style.color = "#1ec5e5"; // Reset the color
    
    // Check if height and weight are valid numbers
    if (isNaN(height) || isNaN(weight)) {
        resultElement.innerHTML = "Please enter valid values for height and weight.";
        resultElement.style.color = "red"; // Set error color
        return;
    }

    // Additional checks for negative or zero values
    if (height <= 0 || weight <= 0) {
        resultElement.innerHTML = "Height and weight must be positive values.";
        resultElement.style.color = "red"; // Set error color
        return;
    }

    // Convert height and weight to metric units if necessary
    if (heightUnit === "feet") {
        height *= 30.48; // Convert inches to centimeters
    }
    if (weightUnit === "pounds") {
        weight *= 0.453592; // Convert pounds to kilograms
    }

    // Calculate BMI
    var bmi = weight / ((height / 100) * (height / 100));
    bmi = bmi.toFixed(2);

    resultElement.innerHTML = "Your BMI: " + bmi;

    // Determine BMI range and set result color
    if (bmi < 18.5) {
        resultElement.style.color = "red";
    } else if (bmi >= 18.5 && bmi < 24.9) {
        resultElement.style.color = "green";
    } else if (bmi >= 25 && bmi < 29.9) {
        resultElement.style.color = "orange";
    } else {
        resultElement.style.color = "red";
    }
}

function clearForm() {
    // Clear the form and result elements
    document.getElementById("height").value = "";
    document.getElementById("weight").value = "";
    var resultElement = document.getElementById("result");
    resultElement.innerHTML = "";
    resultElement.style.color = "#1ec5e5";
}