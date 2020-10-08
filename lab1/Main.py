import pandas as pd
import matplotlib.pyplot as plt
import Secondary


def convert_wind(value):
    new_value = value.replace(' mph', '')
    return int(new_value)


def convert_data(value):
    new_value = (value + ".2019").replace('.', '-')
    return str(new_value)


def convert_pressure(value):
    new_value = value.replace(',', '.')
    return float(new_value)


def parser(data_frame):
    data_frame.rename(columns={'day/month': 'year/month/day'}, inplace=True)

    data_frame['Wind Speed'] = data_frame['Wind Speed'].apply(convert_wind)
    data_frame['Wind Gust'] = data_frame['Wind Gust'].apply(convert_wind)

    data_frame['year/month/day'] = data_frame['year/month/day'].apply(convert_data)
    data_frame['year/month/day'] = pd.to_datetime(data_frame['year/month/day'], format='%d-%b-%Y')

    data_frame['Time'] = pd.to_datetime(data_frame['Time']).dt.strftime('%H:%M')
    data_frame['Time'] = pd.to_datetime(data_frame['Time'], format='%H:%M') - pd.to_datetime(data_frame['Time'],
                                                                                   format='%H:%M').dt.normalize()

    data_frame['Pressure'] = data_frame['Pressure'].apply(convert_pressure)

    data_frame['Humidity'] = data_frame['Humidity'].str.rstrip('%').astype('float') / 100.0

    return data_frame


data_frame = pd.read_csv('DATABASE.csv', delimiter=';')
data_frame = parser(data_frame)
data_frame.set_index('year/month/day', inplace=True)
print(data_frame.to_string())

dictionary = {"Temperature": "Line",
     "Dew Point": "Pie",
     "Humidity": "BoxPlot",
     "Wind": "Pie",
     "Wind Speed": "Hist",
     "Wind Gust": "Bar",
     "Pressure": "Line",
     "Precip.": "Hist",
     "Precip Accum": "Line",
     "Condition": "Pie"
     }

for k, v in zip(dictionary.keys(), dictionary.values()):
    Secondary.show_graphics_by_name_and_type(k, v, data_frame)
    plt.show()

Secondary.show_graphics_by_name("Temperature", data_frame)
plt.show()
