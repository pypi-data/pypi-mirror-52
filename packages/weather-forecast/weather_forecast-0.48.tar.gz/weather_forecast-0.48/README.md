# weather_forecast 



The pip package provides weather forecasting information based on location or address. Using address, the weather_forecast provides location specific forecast. Currently only one function is included i.e forecast. 



### Install 
```
pip install weather_forecast
```

### Code Usage 
```
import weather_forecast as wf
wf.forecast(place = "Bangalore" , time="23:15:00" , date="2019-09-12" , forecast)
```



### Command Line usage 

- Navigate to **./weather_forecast/** and then execute the below command.



```
python forecast.py -p Bangalore
```

```
python forecast.py -p Bangalore -d 2019-09-12
```
