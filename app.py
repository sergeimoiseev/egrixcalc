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

        # flask.flash(data_keys)
        # flask.flash(data_vals)

        params_dict = calc_tools.get_and_store_params()
        # params_keys = [key for key in params_dict.keys() if key in params_dict]
        # params_vals = [params_dict[key] for key in  params_keys if key in params_dict]

        # flask.flash(params_keys)
        # flask.flash(params_vals)

        results_dict = egrix_calc.calc(params_dict)
        results_keys = [key for key in results_dict.keys() if key in results_dict]
        results_vals = [results_dict[key] for key in results_keys if key in results_dict]

        headers = ['','','','']
        values = [0.,0.,0.,0.]
        for key in results_keys:
            if key == 'workout_expenditure_per_month':
                values[0] = "%.1f" % (results_dict['workout_expenditure_per_month'])
                headers[0] = 'Затраты на эксплуатацию в мес, руб'
            if key == 'work__cost_by_workout':
                values[1] = "%.1f" % (results_dict['work__cost_by_workout'])
                headers[1] = 'Доходы от эксплуатации в мес, руб'
            if key == 'workout_profit_per_month':
                values[2] = "%.1f" % (results_dict['workout_profit_per_month'])
                headers[2] = 'Чистая прибыль в мес, руб'
            if key == 'car_efficiency':
                values[3] = "%.3f" % (results_dict['car_efficiency'])
                headers[3] = 'Эффективность ТС'

        flask.flash(headers)
        flask.flash(values)


        return self.get()
    
app.add_url_rule('/', view_func=View.as_view('main'), methods=['GET', 'POST'])

if __name__ == '__main__':
    app.debug = True
    app.run()