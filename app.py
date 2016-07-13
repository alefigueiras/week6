from flask import Flask, render_template, request, redirect
from first_module_risk import get_indicator, plot_ind, create_dataframes, get_mean, plot_score
from bokeh.resources import INLINE
from bokeh.embed import components

app = Flask(__name__)

@app.route('/')
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
    
    c1 = request.args['country1']
    
    c2 = request.args['country2']
    
    countries = [c1, c2]
        
    i1 = request.args['indicator'].upper()

    indicators = [i1]
    
    performance = create_dataframe(countries,indicators)
    
    chart = create_plot(performance)
    
    script,div = components(chart)
    
    return render_template('showind.html',
                           js_resources=INLINE.render_js(),
                           css_resources=INLINE.render_css(),
                           script=script,
                           div=div)

@app.route('/showscore')
def showscore():
    countries = request.args['country']
    
    indicator = request.args['indicator'].upper()

    performance = create_dataframe(countries,indicator)
    
    chart = create_plot(performance)
    
    script,div = components(chart)
    
    return render_template('showscore.html',
                           js_resources=INLINE.render_js(),
                           css_resources=INLINE.render_css(),
                           script=script,
                           div=div)

if __name__ == '__main__':
    app.debug = True
    app.run(port=33507)
