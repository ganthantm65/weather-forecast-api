from sklearn.ensemble import RandomForestRegressor
import os,numpy as np
from sklearn.model_selection import train_test_split
import joblib
import pandas as pd

df=pd.read_csv('weather.csv')

df['Date.Full'] = pd.to_datetime(df['Date.Full'])

df['Day_Sin'] = np.sin(2 * np.pi * df['Date.Full'].dt.dayofyear / 365)
df['Day_Cos'] = np.cos(2 * np.pi * df['Date.Full'].dt.dayofyear / 365)


def train_model():
    X = df.drop(columns=[
        "Data.Temperature.Avg Temp",
        "Date.Full",
        "Station.City",
        "Station.Code",
        "Station.Location",
        "Station.State"
    ])
    Y=df['Data.Temperature.Avg Temp'].values.reshape(-1,1)

    X_train,X_test,Y_train,Y_test=train_test_split(X,Y,test_size=0.2,random_state=42)

    model=RandomForestRegressor(n_estimators=100,random_state=42)
    model.fit(X_train,Y_train)
    y_pred=model.predict(X_test)
    print("Model trained successfully")
    joblib.dump(model, "weather_model.joblib")

    return model

def load_model():
    if os.path.exists("weather_model.joblib"):
        return joblib.load("weather_model.joblib")
    else:
        return train_model()