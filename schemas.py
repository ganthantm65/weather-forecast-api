from pydantic import BaseModel

class CurrentWeather(BaseModel):
    temperature:float
    description:str
    humidity:int
    city:str
class ForecastDay(BaseModel):
    date:str
    predicted_avg_temp:float
    city:str
class WeatherForecast(BaseModel):
    city:str
    forecast:list[ForecastDay]