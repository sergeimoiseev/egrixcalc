# -*- coding: utf-8 -*-
import flask, flask.views
import egrix_calc, calc_tools

app = flask.Flask(__name__)
# Don't do this!
app.secret_key = "bacon"

class View(flask.views.MethodView):
    def get(self):
        return flask.render_template('index.html')
        
    def post(self):
        output_list = []

        data = dict((key, flask.request.form.getlist(key)) for key in flask.request.form.keys())
        data_keys = [key for key in flask.request.form.keys()]
        data_vals = [flask.request.form.getlist(key) for key in  data_keys]

        flask.flash(data_keys)
        flask.flash(data_vals)

        params_dict = calc_tools.get_and_store_params()
        params_keys = [key for key in params_dict.keys()]
        params_vals = [params_dict[key] for key in  params_keys]

        flask.flash(params_keys)
        flask.flash(params_vals)

        return self.get()
    
app.add_url_rule('/', view_func=View.as_view('main'), methods=['GET', 'POST'])

if __name__ == '__main__':
    app.debug = True
    app.run()