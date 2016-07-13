from flask import Flask, render_template, request, redirect
from first_module_risk import get_indicator, plot_ind, create_dataframes, get_mean, plot_score
from bokeh.resources import INLINE
from bokeh.embed import components

app = Flask(__name__)


@app.route('/')
def main():
    return redirect('/index')

@app.route('/index')
def index():
    return render_template('index.html')


@app.route('/getinputind')
def getinputind():
    return render_template('inputind.html')

@app.route('/getinputscore')
def getinputscore():
    return render_template('inputscore.html')

@app.route('/showind')
def showind():
        
    c = {}
    
    countries = [value for key, value in c.items() if key.startswith('country') and value]
    
    i0 = request.args['indicator']

    indicator = [i0]
    
    performance = get_indicator(countries,indicator)
    
    chartind = plot_ind(performance)
    
    script,div = components(chartind)
    
    return render_template('showind.html',
                           js_resources=INLINE.render_js(),
                           css_resources=INLINE.render_css(),
                           script=script,
                           div=div)

@app.route('/showscore')
def showscore():
    
    c = {}
    
    countries = [value for key, value in c.items() if key.startswith('country') and value]
    
    i0 = request.args['i0']
    
    i1 = request.args['i1']
    
    i2 = request.args['i2']
    
    i3 = request.args['i3']
    
    i4 = request.args['i4']

    indicators = [i0, i1, i2, i3, i4]
    
    dataframes = create_dataframes(countries,indicators)
    
    score = get_mean(dataframes)
    
    chartsco = plot_score(score)
    
    script,div = components(chartsco)
    
    return render_template('showscore.html',
                           js_resources=INLINE.render_js(),
                           css_resources=INLINE.render_css(),
                           script=script,
                           div=div)

if __name__ == '__main__':
    app.debug = True
    app.run(port=33507)
