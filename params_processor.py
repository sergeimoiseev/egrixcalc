# -*- coding: utf-8 -*-
import flask, flask.views
import collections
import egrix_calc
import calc_tools as ct
import logging
logger = logging.getLogger(__name__)

class EgrixCalcView(flask.views.MethodView):

    def process_params(self,page_name):
        data = dict((key, flask.request.form.getlist(key)[0]) for key in flask.request.form.keys())
        autopark_type = flask.request.form['submit']
        logger.info("autopark_type\n%s" % (autopark_type,))
        # logger.info("data\n%s" % (data,))
        params_dict, comments_dict = ct.get_and_store_params(load_from_dropbox=False)

        for key in params_dict.keys():
            try:
                if key in data.keys():
                    params_dict[key] = float(data[key])
                else:
                    params_dict[key] = float(params_dict[key])
            except Exception as e:
                logger.info("ERROR on params_dict['%s']\n%s" % (key,params_dict[key],))
                logger.info("ERROR: %s" % (e))
                logger.info("type(params_dict[key])\n%s" % (type(params_dict[key])))
                logger.info("type(data[key])\n%s" % (type(data[key])))

        results_dict = egrix_calc.compare(params_dict, autopark_type)
        results_keys = [key for key in results_dict.keys() if key in results_dict]
        results_vals = [results_dict[key] for key in results_keys if key in results_dict]

        res_d = collections.OrderedDict([])
        res_d['workout_expenditure_per_month']=u'Затраты на эксплуатацию в мес, руб'
        res_d['work__cost_by_workout_per_month']=u'Доходы от эксплуатации в мес, руб'
        res_d['workout_profit_per_month']=u'Чистая прибыль в мес, руб'
        res_d['monitoring__additional_profit_per_month']=u'Экономия за счет мониторинга в месяц, руб'
        res_d['car_efficiency']=u'Эффективность ТС'
        res_d['monitoring__setup_cost']=u'Стоимость установки системы, руб'
        res_d['monitoring__recoupment']=u'Срок окупаемости системы, мес'
        res_d['monitoring__dut_additional_profit_per_month']=u'Экономия за счет ДУТ-а в мес, руб'
        res_d['monitoring__monitoring_additional_profit']=u'Экономия за счет контроля перемещений и моточасов в мес, руб'
        res_d['monitoring__pp_additional_profit']=u'Экономия за счет контроля пассажиропотока в мес, руб'
        res_d['flagDut']=u'Отлдка'
        headers = [res_d[key] for key in res_d.keys() if key in results_dict.keys()]
        values = [results_dict[key] for key in res_d.keys() if key in results_dict.keys()]

        full_messages_list = [headers,values]
        return full_messages_list, ''