from flask import Flask, request, jsonify, render_template, send_file
import joblib
import matplotlib
import matplotlib.pyplot as plt
import io
import numpy as np
import os
import plotly
import plotly.graph_objs as go
import json

# Set Matplotlib to use a non-interactive backend
matplotlib.use('Agg')

app = Flask(__name__)

# Sample data for visualization
months = ["January", "February", "March", "April"]
carbon_footprint = [120, 110, 130, 115]

@app.route('/plot/carbon_footprint')
def plot_carbon_footprint():
    # Matplotlib Plot
    plt.figure()
    plt.plot(months, carbon_footprint, marker='o', color='b', label='Carbon Footprint')
    plt.title("Monthly Carbon Footprint")
    plt.xlabel("Months")
    plt.ylabel("Carbon Footprint (kg CO₂)")
    plt.legend()

    # Save plot to a BytesIO object and return as response
    img = io.BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)
    plt.close()
    return send_file(img, mimetype='image/png')

@app.route('/plot/plotly_carbon_footprint')
def plotly_carbon_footprint():
    # Plotly Plot
    plotly_fig = go.Figure(data=[
        go.Scatter(x=months, y=carbon_footprint, mode='lines+markers', name='Carbon Footprint', line=dict(color='blue'))
    ])
    plotly_fig.update_layout(
        title="Monthly Carbon Footprint (Interactive)",
        xaxis_title="Months",
        yaxis_title="Carbon Footprint (kg CO₂)"
    )

    # Convert Plotly figure to JSON using PlotlyJSONEncoder
    plotly_json = json.loads(json.dumps(plotly_fig, cls=plotly.utils.PlotlyJSONEncoder))
    return jsonify(plotly_json)


# Load the model if it exists, otherwise return an error.
model_path = 'carbon_footprint_model.pkl'
if os.path.exists(model_path):
    model = joblib.load(model_path)
else:
    model = None

# Route to serve the HTML file at the root
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    global model
    if model is None:
        return jsonify({'error': 'Model not found. Train the model by running train_model.py'}), 500

    data = request.json
    user_input = np.array([[data.get('distance', 0),
                            data.get('energy', 0),
                            data.get('food', 0),
                            data.get('flights', 0),
                            data.get('water', 0),
                            data.get('waste', 0),
                            data.get('household', 0),
                            data.get('dairy', 0),
                            data.get('fish', 0),
                            data.get('plant_based', 0)]])
    prediction = model.predict(user_input)
    return jsonify({'carbon_footprint': prediction[0]})

if __name__ == '__main__':
    app.run(debug=True)
