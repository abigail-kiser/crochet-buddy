from flask import Flask
from flask import render_template

# Flask constructor takes the name of 
# current module (__name__) as argument.
app = Flask(__name__)


@app.route('/')
# ‘/’ URL is bound with hello_world() function.
def library():
    return render_template("library.html")


@app.route('/discover/')
def discover():
    return render_template("discover.html")


@app.route('/settings/')
def settings():
    return render_template("settings.html")






# main driver function
if __name__ == '__main__':

    # run() method of Flask class runs the application 
    # on the local development server.
    app.run()