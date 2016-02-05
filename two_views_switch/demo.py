import flask, flask.views
import os
import functools
app = flask.Flask(__name__)
app.secret_key = "bacon"
class Main(flask.views.MethodView):
    def get(self):
        return flask.render_template('index.html')
    
    def post(self):
        return flask.redirect(flask.url_for('index'))

class Remote(flask.views.MethodView):
    def get(self):
        return flask.render_template('remote.html')
        
    def post(self):
        result = str(flask.request.form['expression'])
        flask.flash(result)
        return flask.redirect(flask.url_for('remote'))
    
app.add_url_rule('/',
                 view_func=Main.as_view('index'),
                 methods=["GET", "POST"])
app.add_url_rule('/remote/',
                 view_func=Remote.as_view('remote'),
                 methods=['GET', 'POST'])

app.debug = True
app.run()