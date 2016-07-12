import pandas
import requests
import datetime
from bokeh.charts import Bar, Line, output_file, show, TimeSeries

def create_dataframe(countries, indicator):
    url = 'http://api.worldbank.org/countries/%s/indicators/%s?per_page=300&date=2014:2014&format=json' % (''.join(countries), ''.join(indicator))
    response = requests.get(url)
    json = response.json()
    dataset = json[1]
    data = {
        'Date': [x['date'] for x in dataset],
        'Country': [x['country']['value'] for x in dataset],
        'Indicator': [x['indicator']['value'] for x in dataset],
        'Value': [x['value'] for x in dataset],
    }
    df = pandas.DataFrame(data)
    df['Value'] = pandas.to_numeric(df['Value'], errors='coerce')
    df['Date'] = pandas.to_datetime(df['Date'])
    df = df.round(2)
    return df


def create_plot(performance):
    p = Bar(performance, label='Country', values='Value', color='Country', xlabel="Country", 
            legend='top_right')
    return p