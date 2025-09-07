from fastapi import FastAPI, HTTPException,status
import pandas as pd
from schemas import WeatherForecast,CurrentWeather,ForecastDay
import numpy as np
import requests,dotenv
from model import df,load_model,train_model

app=FastAPI()
model=load_model()

api_key=dotenv.dotenv_values('.env')['WEATHER_API_KEY']

@app.get("/forecast/{city}", response_model=WeatherForecast, status_code=status.HTTP_200_OK)
def get_weather_forecast(city: str, days: int = 7):
    model = load_model()
    city_df = df.copy()

    if city:
        city_df = df[df["Station.City"].str.lower() == city.lower()]
        if city_df.empty:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="City not found in dataset")

    last_date = pd.to_datetime(city_df["Date.Full"]).max()

    future_dates = pd.date_range(start=last_date + pd.Timedelta(days=1), periods=days)

    future_df = pd.DataFrame({
        "Data.Precipitation": city_df["Data.Precipitation"].mean(),
        "Date.Month": future_dates.month,
        "Date.Week of": future_dates.isocalendar().week.astype(int),
        "Date.Year": future_dates.year,
        "Data.Temperature.Max Temp": city_df["Data.Temperature.Max Temp"].mean(),
        "Data.Temperature.Min Temp": city_df["Data.Temperature.Min Temp"].mean(),
        "Data.Wind.Direction": city_df["Data.Wind.Direction"].mean(),
        "Data.Wind.Speed": city_df["Data.Wind.Speed"].mean(),
    })

    future_df["Day_Sin"] = np.sin(2 * np.pi * future_dates.dayofyear / 365)
    future_df["Day_Cos"] = np.cos(2 * np.pi * future_dates.dayofyear / 365)


    future_df = future_df[model.feature_names_in_]

    preds = model.predict(future_df)

    results = []
    for date, temp in zip(future_dates, preds.flatten()):
        results.append({
            "date": str(date.date()),
            "predicted_avg_temp": round(float(temp), 2),
            "city": city if city else "Unknown"
        })

    forecast = WeatherForecast(
        city=city if city else "Unknown",
        forecast=[ForecastDay(**res) for res in results]
    )
    return forecast
