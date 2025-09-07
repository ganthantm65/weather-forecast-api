# Weather Forecast API

## Overview
The **Weather Forecast API** is an AI-powered application that predicts daily average temperatures using historical weather data and seasonal features. Built with **FastAPI** and **scikit-learn**, it provides current weather and multi-day forecasts for any city in the dataset. The model incorporates sinusoidal features to capture seasonal trends, giving more dynamic predictions compared to simple linear regression.

## Features
- Get **current weather** for a city.
- Get **7-day (or N-day) forecasts** with predicted average temperatures.
- Seasonal feature handling (\`Day_Sin\`, \`Day_Cos\`) to improve prediction accuracy.
- Uses **Random Forest Regressor** for better variance in predictions.
- Handles missing cities gracefully with proper error responses.

## Tech Stack
- **Backend:** Python, FastAPI  
- **Data Processing:** pandas, numpy  
- **Machine Learning:** scikit-learn (RandomForestRegressor)  
- **Model Persistence:** joblib  
- **API Requests:** requests  
- **Environment Variables:** python-dotenv  

## Dataset
The dataset (\`weather.csv\`) includes:
- \`Date.Full\` – Full date
- \`Station.City\` – City name
- \`Data.Temperature.Avg Temp\`, \`Max Temp\`, \`Min Temp\` – Temperature features
- \`Data.Precipitation\` – Precipitation
- \`Data.Wind.Direction\`, \`Data.Wind.Speed\` – Wind features
- Seasonal features (\`Day_Sin\`, \`Day_Cos\`) are added for modeling

## Installation

1. Clone the repository:
\`\`\`bash
git clone <repo-url>
cd weather_api
\`\`\`

2. Install dependencies:

\`\`\`bash
pip install -r requirements.txt
\`\`\`

3. Add \`.env\` file in the project root with your Weather API key:

\`\`\`
WEATHER_API_KEY=your_api_key_here
\`\`\`

4. Run the API:

\`\`\`bash
uvicorn main:app --reload
\`\`\`

## API Endpoints

### 1. Current Weather

**Endpoint:**

\`\`\`
GET /current/{city}
\`\`\`

**Response:**

\`\`\`json
{
  "temperature": 28.5,
  "description": "Partly cloudy",
  "humidity": 65,
  "city": "Birmingham"
}
\`\`\`

### 2. Forecast

**Endpoint:**

\`\`\`
GET /forecast/{city}?days=N
\`\`\`

**Response:**

\`\`\`json
{
  "city": "Birmingham",
  "forecast": [
    {
      "date": "2017-01-02",
      "predicted_avg_temp": 65.78,
      "city": "Birmingham"
    },
    {
      "date": "2017-01-03",
      "predicted_avg_temp": 66.15,
      "city": "Birmingham"
    }
  ]
}
\`\`\`

## Model Explanation

* **Model Used:** Random Forest Regressor
* **Input Features:**

  * \`Data.Precipitation\`
  * \`Data.Temperature.Max Temp\`
  * \`Data.Temperature.Min Temp\`
  * \`Data.Wind.Direction\`
  * \`Data.Wind.Speed\`
  * \`Date.Year\`
  * \`Date.Month\`
  * \`Date.Week of\`
  * Seasonal features: \`Day_Sin\`, \`Day_Cos\`
* **Output:** Predicted average temperature (\`Data.Temperature.Avg Temp\`)
* **Why Random Forest:** Provides non-linear modeling, captures seasonal patterns better, avoids predicting the same temperature for all future dates (unlike linear regression).

## How it Works

1. Historical data is read from \`weather.csv\`.
2. Seasonal features (\`Day_Sin\`, \`Day_Cos\`) are added to capture yearly temperature cycles.
3. The Random Forest model is trained on historical data.
4. For forecasts:

   * Future dates are generated.
   * Seasonal features are calculated.
   * Model predicts average temperatures for each future date.
5. Results are returned in a structured JSON response.

## License

This project is licensed under the MIT License.
" > README.md
