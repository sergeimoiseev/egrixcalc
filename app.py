# -*- coding: utf-8 -*-
import flask, flask.views
import egrix_calc
import calc_tools as ct
import logging
import transliterate 
# transliterate.translit(u"Лорем ипсум долор сит амет", 'ru', reversed=True)
def tr(string):
    return transliterate.translit(string,'ru',reversed=True)

logger = logging.getLogger(__name__)

app = flask.Flask(__name__)
# Don't do this!
app.secret_key = "bacon"

class View(flask.views.MethodView):
    def get(self):
        return flask.render_template('index.html')
        
    def post(self):
        output_list = []

        data = dict((key, flask.request.form.getlist(key)) for key in flask.request.form.keys())
        data_keys = [key for key in data.keys()]
        data_vals = [flask.request.form.getlist(key) for key in  data_keys]
        # flask.flash(data_keys)
        # flask.flash(data_vals)
        logger.info("data_keys\n%s" % (data_keys,))
        logger.info("data_vals\n%s" % (data_vals,))

        params_dict = ct.get_and_store_params()
        # params_keys = [key for key in params_dict.keys() if key in params_dict]
        # params_vals = [params_dict[key] for key in  params_keys if key in params_dict]

        if 'firm.cars_quantity' in data.keys():
            if data['firm.cars_quantity'][0] != '':
                params_dict['cars_quantity'] =  int(data['firm.cars_quantity'][0])

        if 'firm.average_run_time' in data.keys():
            if data['firm.average_run_time'][0] != '':
                motorhours_per_day = float(data['firm.average_run_time'][0])
                params_dict['motorhours_per_day'] =  float(data['firm.average_run_time'][0])
                if motorhours_per_day > 24:
                    flask.flash(['Неверно заданы параметры.'])
                    flask.flash(['Введите параметры верно.'])
                    return self.get()

        if 'equip.dut' in data.keys():
            if data['equip.dut'][0] == 'on':
                params_dict['flagDut'] = 1.
        if 'firm.fridge' in data.keys():
            if data['firm.fridge'][0] == 'on':
                params_dict['flagFrLoss'] = 1.
                if 'equip.temp' in data.keys():
                    if data['equip.temp'][0] == 'on':
                        params_dict['flagThermo'] = 1.
        if 'firm.passengers' in data.keys():
            if data['firm.passengers'][0] == 'on':
                params_dict['flag_passengers'] = 1.
                if 'equip.pp' in data.keys():
                    if data['equip.pp'][0] == 'on':
                        params_dict['flagPP'] = 1.
        if 'equip.pp' in data.keys():
            if data['equip.pp'][0] == 'on':
                params_dict['flagPP'] = 1.
        if 'equip.block_eng' in data.keys():
            if data['equip.block_eng'][0] == 'on':
                params_dict['flag_block_eng'] = 1.
        if 'equip.alarm_btn' in data.keys():
            if data['equip.alarm_btn'][0] == 'on':
                params_dict['flag_alarm_btn'] = 1.


        results_dict = egrix_calc.compare(params_dict)
        results_keys = [key for key in results_dict.keys() if key in results_dict]
        results_vals = [results_dict[key] for key in results_keys if key in results_dict]

        headers = ['','','','','','','']
        values = [0.,0.,0.,0.,0.,0.,0.]
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
            if key == 'workout_profit_per_month':
                values[3] = "%.1f" % (results_dict['monitoring__additional_profit_per_month'])
                headers[3] = 'Экономия за счет мониторинга в месяц, руб'
            if key == 'car_efficiency':
                values[4] = "%.3f" % (results_dict['car_efficiency'])
                headers[4] = 'Эффективность ТС'
            if key == 'monitoring__setup_cost':
                values[5] = "%.1f" % (results_dict['monitoring__setup_cost'])
                headers[5] = 'Стоимость установки системы, руб'
            if key == 'monitoring__recoupment':
                values[6] = "%.1f" % (results_dict['monitoring__recoupment'])
                headers[6] = 'Срок окупаемости системы, мес'

# cant print in russian on jinja2
        # headers = [tr(item) for item in headers]
        # values = [tr(item) for item in values]
        # results_keys = [tr(item) for item in results_keys]
        # results_vals = [tr(item) for item in results_vals]

        # headers = [str(bytes(item,'utf-8'),encoding='utf-8') for item in headers]
        # values = [str(bytes(item,'utf-8'),encoding='utf-8') for item in values]
        # results_keys = [str(bytes(item,'utf-8'),encoding='utf-8') for item in results_keys]
        # results_vals = [str(bytes(item,'utf-8'),encoding='utf-8') for item in results_vals]


        # flask.flash([str(bytes('Русский язык', 'utf-8'),encoding = 'utf-8')])
        # flask.flash(['test output'])

        # flask.flash(headers)
        flask.flash(values)

        # flask.flash(results_keys)
        # flask.flash(results_vals)


        return self.get()
    
app.add_url_rule('/', view_func=View.as_view('main'), methods=['GET', 'POST'])

if __name__ == '__main__':
    ct.setup_logging()
    app.debug = True
    app.run()