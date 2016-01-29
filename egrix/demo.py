import flask, flask.views
import calc_staj

app = flask.Flask(__name__)
# Don't do this!
app.secret_key = "bacon"

class View(flask.views.MethodView):
    def get(self):
        return flask.render_template('index_calc.html')
        # return flask.render_template('index.html')
        
    def post(self):
        output_list = []

        data = dict((key, flask.request.form.getlist(key)) for key in flask.request.form.keys())
        data_keys = [key for key in flask.request.form.keys()]
        data_vals = [flask.request.form.getlist(key) for key in  data_keys]
        # data_vals = []
        # (data_vals.append(flask.request.form.getlist(key)) for key in  data_keys)

        flask.flash(data_keys)
        flask.flash(data_vals)

        return self.get()
    
app.add_url_rule('/', view_func=View.as_view('main'), methods=['GET', 'POST'])

app.debug = True
app.run()