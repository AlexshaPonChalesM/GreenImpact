function displaySection(sectionId) {
    document.querySelectorAll('.section').forEach(section => {
        section.style.display = 'none';
    });
    document.getElementById(sectionId).style.display = 'block';
}

async function calculateImpact() {
    const data = {
        distance: parseFloat(document.getElementById('distance').value),
        energy: parseFloat(document.getElementById('energy').value),
        food: parseFloat(document.getElementById('food').value),
        flights: parseFloat(document.getElementById('flights').value),
        water: parseFloat(document.getElementById('water').value),
        waste: parseFloat(document.getElementById('waste').value),
        household: parseFloat(document.getElementById('household').value),
        dairy: parseFloat(document.getElementById('dairy').value),
        fish: parseFloat(document.getElementById('fish').value),
        plant_based: parseFloat(document.getElementById('plant_based').value)
    };

    const response = await fetch('/predict', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(data)
    });

const result = await response.json();
    document.getElementById('carbonOutput').textContent = `${result.carbon_footprint.toFixed(2)} kg CO₂`;
}
