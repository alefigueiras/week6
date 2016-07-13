import pandas
import requests
import datetime
from bokeh.charts import Bar, output_file, show, TimeSeries, Scatter

def get_indicator(countries, indicator):
    url = 'http://api.worldbank.org/countries/%s/indicators/%s?per_page=300&date=2014:2014&format=json' % (';'.join(countries), ';'.join(indicator))
    assert isinstance(countries, list)
    assert isinstance(indicator, list)
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

def plot_ind(performance):
    p = Bar(performance, label='Country', values='Value', color='Country', xlabel="Country", 
            ylabel=performance['Indicator'][0], title='Performance of %s' % performance['Indicator'][0], legend='top_right')
    return p

def create_dataframes(countries, indicators):
    dataframes = [get_indicator(countries, i) for i in indicators]
    return pandas.concat(dataframes)

def get_mean(dataframes):
    score = dataframes.groupby('Country')['Value'].mean().reset_index()
    return score

def plot_score(score):
    p = Bar(score, label='Country', values='Value', xlabel="Country", 
    color='Country', title='Title', legend='top_right')
    return p